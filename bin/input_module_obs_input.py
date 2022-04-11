# encoding = utf-8
import gzip
import hashlib
import re

from modinput_wrapper.base_modinput import BaseModInput
from obs import ObsClient, GetObjectHeader, LogConf
from splunklib.modularinput import EventWriter


def validate_input(helper, definition):
    retry_times = definition.parameters.get('retry_times')
    try:
        int(retry_times)
    except ValueError:
        raise ValueError(f"retry_times is wrong, {retry_times} is not a number! ")
    part_size_str = definition.parameters.get('part_size', None)
    try:
        int(part_size_str)
    except ValueError:
        raise ValueError(f"part_size_str is wrong, {part_size_str} is not a number! ")
    enable_obs_log = definition.parameters.get('enable_obs_log', None)
    log_config_path = definition.parameters.get('log_config_path', None)

    if enable_obs_log is True:
        endpoint = definition.parameters.get_arg('endpoint')
        ak = definition.parameters.get_arg('ak')
        sk = definition.parameters.get_arg('sk')
        test_client = ObsClient(ak, sk, server=endpoint)
        try:
            test_client.initLog(LogConf(log_config_path), 'obs_logger')
        except ValueError:
            raise ValueError(f"Some values in the settings file [{log_config_path}] are incorrect. Please check again.")
        except Exception as e:
            raise e


def collect_events(helper, ew):
    proxy_settings = helper.get_proxy()
    loglevel = helper.get_log_level()
    helper.set_log_level(loglevel)

    endpoint = helper.get_arg('endpoint')
    ak = helper.get_arg('ak')
    sk = helper.get_arg('sk')
    bucket = helper.get_arg('bucket')
    prefix = helper.get_arg('prefix')
    part_size = int(helper.get_arg('part_size'))
    retry_times = int(helper.get_arg('retry_times'))
    using_https = helper.get_arg('using_https')
    unpack_gz_file = helper.get_arg('unpack_gz_file')

    enable_obs_log = helper.get_arg('enable_obs_log')
    log_config_path = helper.get_arg('log_config_path')

    helper.log_info(f"Initialization Parameters: endpoint:{endpoint}, ak:{ak}, bucket:{bucket}, prefix:{prefix}, "
                    f"using_https:{using_https}, part_size: {part_size}, retry_times: {retry_times},"
                    f"enable_log: {enable_obs_log}, log_config_path: {log_config_path}, "
                    f"unpack_gz_file: {unpack_gz_file}")
    if "proxy_url" in proxy_settings:
        helper.log_info(f"Using Proxy, proxy info: proxy_host: {proxy_settings['proxy_host']}, "
                        f"proxy_port: {proxy_settings['proxy_port']}, "
                        f"proxy_username: {proxy_settings['proxy_username']}")
        obs_client = ObsClient(ak, sk, server=endpoint, is_secure=using_https,
                               proxy_host=proxy_settings["proxy_url"], proxy_port=int(proxy_settings["proxy_port"]),
                               proxy_username=proxy_settings["proxy_username"],
                               proxy_password=proxy_settings["proxy_password"])
    else:
        obs_client = ObsClient(ak, sk, server=endpoint, is_secure=using_https)

    if enable_obs_log:
        obs_client.initLog(LogConf(log_config_path), 'obs_logger')
    next_marker = None
    page_number = 1
    while True:
        helper.log_info(f"Listing page {page_number}")
        resp = obs_client.listObjects(bucket, marker=next_marker, prefix=prefix, encoding_type="url")
        helper.log_info(f"List result: {resp}")
        for content in resp.body.contents:
            object_key = content.key
            md5 = hashlib.md5()
            md5.update(f"{bucket}/{object_key}".encode("utf-8"))
            checkpoint_key = md5.hexdigest()
            if helper.get_check_point(checkpoint_key) is not None:
                helper.log_info(f"{bucket}/{object_key} has been indexed before")
                continue
            helper.log_info(f"Start to get content of {bucket}/{object_key}")
            download_object_with_retry(obs_client, bucket, object_key, helper, ew,
                                       part_size, retry_times, unpack_gz_file)
            helper.save_check_point(checkpoint_key, "Indexed")

        if not resp.body.is_truncated:
            helper.log_info(f"Finish listing, total page number is {page_number}")
            break
        page_number += 1
        next_marker = resp.body.next_marker


def download_object_with_retry(obs_client: ObsClient, bucket: str, object_key: str, helper: BaseModInput,
                               ew: EventWriter, part_size: int = 4 * 1024 * 1024,
                               retry_times: int = 3, unpack_gz_file=False):
    start = 0
    object_info = obs_client.headObject(bucket, object_key)
    if object_info.status != 200:
        helper.log_info(f"Head object {object_key} failed")
        return False

    content_length = int(dict(object_info.header)["content-length"])
    helper.log_info(f"Total length of {object_key} is {content_length}, start to download object")
    part_end = min(content_length, start + part_size)
    last_event = None
    n = 0
    while n < retry_times:
        if start > content_length:
            break
        if last_event is not None:
            ew.write_event(last_event)
            last_event = None
        try:
            part_end = min(content_length, start + part_size)
            helper.log_debug(f"Getting {bucket}/{object_key} from {start} to {part_end}")
            header = GetObjectHeader(range=f"{start}-{part_end}")
            part_content = obs_client.getObject(bucket, object_key, headers=header, loadStreamInMemory=True)
            if unpack_gz_file and object_key.endswith(".gz"):
                need_data = gzip.decompress(part_content.body.buffer)
            else:
                need_data = part_content.body.buffer
            last_event = helper.new_event(data=need_data.decode("utf-8"),
                                          source=f"{bucket}/{object_key}", index=helper.get_output_index(),
                                          sourcetype=helper.get_sourcetype(), done=False)

            start = part_end + 1
        except Exception as e:
            helper.log_error(e)
            helper.log_warning(f"Getting object {object_key} from {start} to {part_end} failed, "
                               f"retry for {n}/{retry_times}")
            n += 1
    # 重试三次后还不成功直接放弃
    if last_event is not None:
        last_event.done = True
        ew.write_event(last_event)
    if content_length < part_end:
        helper.log_error(f"Getting object {object_key} failed")

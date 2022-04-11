[obs_input://<name>]
endpoint = 
ak = Make sure you have the ListBucket permission and GetObject permission
sk = 
bucket = 
prefix = The prefix of the target object, after specifying this value, only objects starting with this prefix will be listed
part_size = The block size when getting the object, the unit is bytes, the default value is 4M
retry_times = Number of retries when getting object content fails
using_https = Whether to use HTTPS
unpack_gz_file = Whether to automatically decompress files ending in `.gz`, when set to False, the content of `.gz` files will not be recognized
enable_obs_log = Whether to enable the log of OBS SDK. If this option is enabled, the path to the log configuration file must be specified.
log_config_path = The path of the log configuration file, you can get the template from https://github.com/huaweicloud/huaweicloud-sdk-python-obs/blob/master/log.conf
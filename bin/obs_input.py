import splunk_obs_connector_declare

import os
import sys
import time
import datetime
import json

import modinput_wrapper.base_modinput
from splunklib import modularinput as smi



import input_module_obs_input as input_module

bin_dir = os.path.basename(__file__)

'''
    Do not edit this file!!!
    This file is generated by Add-on builder automatically.
    Add your modular input logic to file input_module_obs_input.py
'''
class ModInputobs_input(modinput_wrapper.base_modinput.BaseModInput):

    def __init__(self):
        if 'use_single_instance_mode' in dir(input_module):
            use_single_instance = input_module.use_single_instance_mode()
        else:
            use_single_instance = False
        super(ModInputobs_input, self).__init__("splunk_obs_connector", "obs_input", use_single_instance)
        self.global_checkbox_fields = None

    def get_scheme(self):
        """overloaded splunklib modularinput method"""
        scheme = super(ModInputobs_input, self).get_scheme()
        scheme.title = ("obs-input")
        scheme.description = ("Go to the add-on\'s configuration UI and configure modular inputs under the Inputs menu.")
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True

        scheme.add_argument(smi.Argument("name", title="Name",
                                         description="",
                                         required_on_create=True))

        """
        For customized inputs, hard code the arguments here to hide argument detail from users.
        For other input types, arguments should be get from input_module. Defining new input types could be easier.
        """
        scheme.add_argument(smi.Argument("endpoint", title="Endpoint",
                                         description="",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("ak", title="AK",
                                         description="Make sure you have the ListBucket permission and GetObject permission",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("sk", title="SK",
                                         description="",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("bucket", title="Bucket",
                                         description="",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("prefix", title="Prefix",
                                         description="The prefix of the target object, after specifying this value, only objects starting with this prefix will be listed",
                                         required_on_create=False,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("part_size", title="Part Size",
                                         description="The block size when getting the object, the unit is bytes, the default value is 4M",
                                         required_on_create=False,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("retry_times", title="Retry Times",
                                         description="Number of retries when getting object content fails",
                                         required_on_create=False,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("using_https", title="Using HTTPS",
                                         description="Whether to use HTTPS",
                                         required_on_create=False,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("unpack_gz_file", title="Unpack GZ File",
                                         description="Whether to automatically decompress files ending in `.gz`, when set to False, the content of `.gz` files will not be recognized",
                                         required_on_create=False,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("enable_obs_log", title="Enable OBS Log",
                                         description="Whether to enable the log of OBS SDK. If this option is enabled, the path to the log configuration file must be specified.",
                                         required_on_create=False,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("log_config_path", title="Log Config Path",
                                         description="The path of the log configuration file, you can get the template from https://github.com/huaweicloud/huaweicloud-sdk-python-obs/blob/master/log.conf",
                                         required_on_create=False,
                                         required_on_edit=False))
        return scheme

    def get_app_name(self):
        return "splunk-obs-connector"

    def validate_input(self, definition):
        """validate the input stanza"""
        input_module.validate_input(self, definition)

    def collect_events(self, ew):
        """write out the events"""
        input_module.collect_events(self, ew)

    def get_account_fields(self):
        account_fields = []
        return account_fields

    def get_checkbox_fields(self):
        checkbox_fields = []
        checkbox_fields.append("using_https")
        checkbox_fields.append("unpack_gz_file")
        checkbox_fields.append("enable_obs_log")
        return checkbox_fields

    def get_global_checkbox_fields(self):
        if self.global_checkbox_fields is None:
            checkbox_name_file = os.path.join(bin_dir, 'global_checkbox_param.json')
            try:
                if os.path.isfile(checkbox_name_file):
                    with open(checkbox_name_file, 'r') as fp:
                        self.global_checkbox_fields = json.load(fp)
                else:
                    self.global_checkbox_fields = []
            except Exception as e:
                self.log_error('Get exception when loading global checkbox parameter names. ' + str(e))
                self.global_checkbox_fields = []
        return self.global_checkbox_fields

if __name__ == "__main__":
    exitcode = ModInputobs_input().run(sys.argv)
    sys.exit(exitcode)
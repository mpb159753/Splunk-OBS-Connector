# Interconnect Splunk with HUAWEI CLOUD OBS Plug-in
[简体中文](https://github.com/mpb159753/Splunk-OBS-Connector/blob/master/README.md) |English

## Installation Method

### Download the source code from Github and install it.
1. Installing the [Splunk Add-on Builder](https://splunkbase.splunk.com/app/2962/)
2. Download `OBS Connector` from Github `https://github.com/mpb159753/Splunk-OBS-Connector.git`
3. Choose Splunk Add-on Builder and click `Import Project` to import the compressed package.


### Installing Using Splunkbase
1. Downloading the Installation Package Through the [Splunk OBS Connector](https://splunkbase.splunk.com/app/24484/)
2. Go to the Splunk application installation page and select `install from file`.
3. Select the installation package downloaded in step 1.

### Installation Dependency
This plug-in depends on Huawei OBS SDK. The SDK's third-party library `pycryptodome` cannot be used across platforms. The dependency of the `Unix` operating system in the `x86_64` architecture has been preconfigured in the software packages of Github and SplunkBase. If the version does not match your version or is abnormal after installation, Install the plug-in of the corresponding platform by referring to this section.

1. Install Python3 pip on the server where Splunk is deployed. If Python3 pip has been installed, skip this step.
2. Install the OBS Python SDK to the temporary directory `pip install esdk-obs-python --root /tmp/obs`.
3. Go to the dependency installation directory and run `cd /tmp/obs/`.
4. Go to the subdirectory to the `site-packages` directory (possibly `usr/lib64/python3.7/site-packages/`).
5. Run the `zip -rq obs.zip *` command to pack the files.
6. Decompress the dependency package in step 5 to `$SPLUNK_HOME/etc/apps/splunk-obs-connector/bin/splunk-obs-connector/aob_py3`.

## Usage Instructions

### Parameter Description

| Parameter name  | Description                                                                                                                                                    | Mandatory | Default value |
|:---------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------:|:-------------:|
|    Endpoint     | OBS endpoint corresponding to the bucket. If the endpoint is inconsistent, the bucket cannot be accessed.                                                      |     Y     |     None      |
|       AK        | Access key of the account. The account must have the ListBucket and GetObject permissions.                                                                     |     Y     |     None      |
|       SK        | SecretKey of the account                                                                                                                                       |     Y     |     None      |
|     Bucket      | Bucket name                                                                                                                                                    |     Y     |     None      |
|     Prefix      | Prefix of the target object. When this value is specified, only objects starting with this prefix are listed.                                                  |     N     |     None      |
|    Part Size    | Size of the block used to obtain the object, in bytes. The default value is 4 MB.                                                                              |     N     | 4194304(4 MB) |
|   Retry Times   | Retry times when the object content fails to be obtained                                                                                                       |     N     |       3       |
|   Using HTTPS   | Whether to use HTTPS                                                                                                                                           |     N     |     True      |
| Unpack GZ File  | Whether to automatically decompress files ending with `.gz`. If this parameter is set to False, the contents of `.gz` files cannot be identified.              |     N     |     True      |
| Enable OBS Log  | Whether to enable OBS SDK logs. If this option is enabled, you must specify the path of the log configuration file.                                            |     N     |     False     |
| Log Config Path | Path of the log configuration file. You can obtain the template from [Github](https://github.com/huaweicloud/huaweicloud-sdk-python-obs/blob/master/log.conf). |     N     |     None      |
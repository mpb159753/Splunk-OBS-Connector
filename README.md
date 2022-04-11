# Splunk 对接华为云 OBS 插件
简体中文|[English](https://github.com/mpb159753/Splunk-OBS-Connector/README-EN.md)

## 安装方法

### 从 Github 下载源码安装
1. 安装 [Splunk Add-on Builder](https://splunkbase.splunk.com/app/2962/)
2. 从 Github 下载 OBS Connector, `https://github.com/mpb159753/Splunk-OBS-Connector.git`
3. 进入 Splunk Add-on Builder， 点击 `Import Project` 导入压缩包


### 通过 Splunkbase 安装
1. 通过 [Splunk OBS Connector](https://splunkbase.splunk.com/app/24484/) 下载安装包
2. 进入 Splunk 的应用安装，选择从文件安装
3. 选择步骤 1 中下载的安装包

### 安装依赖
该插件依赖于华为 OBS SDK，由于其 SDK 依赖的三方库 `pycryptodome` 不能跨平台使用，Github 和 SplunkBase 的软件包内已经预置了`Unix` 操作系统在 `x86_64` 架构下的相关依赖，如若与您所使用的版本不符，或安装后使用不正常，请参考参考此章节自行安装对应平台的插件。

1. 在部署 Splunk 的服务器安装 Python3 pip，如已安装可跳过
2. 安装 OBS Python SDK 至临时目录，`pip install esdk-obs-python --root /tmp/obs`
3. 进入依赖安装目录，`cd /tmp/obs/`
4. 进入子目录，直到 `site-packages` 路径下（可能路径为`usr/lib64/python3.7/site-packages/`）
5. 执行 `zip -rq obs.zip *` 进行打包
6. 将第五步打包好依赖包解压至 `$SPLUNK_HOME/etc/apps/splunk-obs-connector/bin/splunk-obs-connector/aob_py3`

## 使用说明

### 配置参数说明

|       参数名       | 说明                                                                                                           | 必填  |     默认值     |
|:---------------:|:-------------------------------------------------------------------------------------------------------------|:---:|:-----------:|
|    Endpoint     | 桶所对应的 OBS Endpoint，如果不一致会无法访问桶                                                                               |  Y  |      无      |
|       AK        | 账号的 AccessKey, 账号需要有 ListBucket 权限和 GetObject 权限                                                             |  Y  |      无      |
|       SK        | 账号的 SecretKey                                                                                                |  Y  |      无      |
|     Bucket      | 桶名                                                                                                           |  Y  |      无      |
|     Prefix      | 目标对象的前缀, 在指定该值后，将仅列举以此前缀开头的对象                                                                                |  N  |      无      |
|    Part Size    | 获取对象时的分块大小，单位为 bytes, 默认值 4M                                                                                 |  N  | 4194304(4M) |
|   Retry Times   | 获取对象内容失败时的重试次数                                                                                               |  N  |      3      |
|   Using HTTPS   | 是否使用 HTTPS                                                                                                   |  N  |    True     |
| Unpack GZ File  | 是否自动解压 `.gz` 结尾的文件, 设置为 False 时将无法识别 `.gz` 文件的内容                                                             |  N  |    True     |
| Enable OBS Log  | 是否开启 OBS SDK 的日志。如若开启该选项则必须指定日志配置文件的路径                                                                       |  N  |    False    |
| Log Config Path | 日志配置文件的路径，可以从  [Github](https://github.com/huaweicloud/huaweicloud-sdk-python-obs/blob/master/log.conf) 获取模板 |  N  |      无      |


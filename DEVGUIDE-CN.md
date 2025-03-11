# 开发者指南
## [English](DEVGUIDE.md)

阿里云对象存储（Object Storage Service，简称OSS），是阿里云对外提供的海量、安全、低成本、高可靠的云存储服务。用户可以通过调用API，在任何应用、任何时间、任何地点上传和下载数据，也可以通过用户Web控制台对数据进行简单的管理。OSS适合存放任意文件类型，适合各种网站、开发企业及开发者使用。

该开发套件隐藏了许多较低级别的实现，例如身份验证、请求重试和错误处理, 通过其提供的接口，让您不用复杂编程即可访问阿里云OSS服务。

该开发套件同时提供实用的模块，例如上传和下载管理器，自动将大对象分成多块并行传输。

您可以参阅该指南，来帮助您安装、配置和使用该开发套件。

跳转到:

* [安装](#安装)
* [配置](#配置)
* [接口说明](#接口说明)
* [场景示例](#场景示例)
* [迁移指南](#迁移指南)

# 安装

## 环境准备

使用Python 3.8及以上版本。
请参考[Python安装](https://www.python.org/)下载和安装Python运行环境。
您可以执行以下命令查看Python语言版本。
```
python --version
```

## 安装SDK

```
pip install alibabacloud-oss-v2
```

## 验证SDK
运行以下代码查看SDK版本：
```
pip show alibabacloud-oss-v2
```

# 配置
您可以配置服务客户端的常用设置，例如超时和重试配置，大多数设置都是可选的。
但是，对于每个客户端，您必须指定区域和凭证。 SDK使用这些信息签署请求并将其发送到正确的区域。

此部分的其它主题
* [区域](#区域)
* [凭证](#凭证)
* [访问域名](#访问域名)
* [HTTP客户端](#http客户端)
* [重试](#重试)
* [配置参数汇总](#配置参数汇总)

## 加载配置
配置客户端的设置有多种方法，以下是推荐的模式。

```
# 以从环境变量中获取访问凭证为例
credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
# 以华东1（杭州）为例
cfg.region = "cn-hangzhou"

client = oss.Client(cfg)
```

## 区域
指定区域时，您可以指定向何处发送请求，例如 cn-hangzhou 或 cn-shanghai。有关所支持的区域列表，请参阅 [OSS访问域名和数据中心](https://www.alibabacloud.com/help/zh/oss/user-guide/regions-and-endpoints)。
SDK 没有默认区域，您需要加载配置时使用`config.region`作为参数显式设置区域。例如
```
cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
```

>**说明**：该SDK默认使用v4签名，所以必须指定该参数。

## 凭证

SDK需要凭证（访问密钥）来签署对 OSS 的请求, 所以您需要显式指定这些信息。当前支持凭证配置如下：
* [环境变量](#环境变量)
* [ECS实例角色](#ecs实例角色)
* [静态凭证](#静态凭证)
* [RAM角色](#ram角色)
* [OIDC角色SSO](#oidc角色sso)
* [自定义凭证提供者](#自定义凭证提供者)

### 环境变量

SDK 支持从环境变量获取凭证，支持的环境变量名如下：
* OSS_ACCESS_KEY_ID
* OSS_ACCESS_KEY_SECRET
* OSS_SESSION_TOKEN（可选）

以下展示了如何配置环境变量。

1. Linux、OS X 或 Unix
```
$ export OSS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
$ export OSS_ACCESS_KEY_SECRET=YOUR_ACCESS_KEY_SECRET
$ export OSS_SESSION_TOKEN=TOKEN
```

2. Windows
```
$ set OSS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
$ set OSS_ACCESS_KEY_SECRET=YOUR_ACCESS_KEY_SECRET
$ set OSS_SESSION_TOKEN=TOKEN
```

使用环境变量凭证

```
credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider

```

### ECS实例角色

如果你需要在阿里云的云服务器ECS中访问您的OSS，您可以通过ECS实例RAM角色的方式访问OSS。实例RAM角色允许您将一个角色关联到云服务器实例，在实例内部基于STS临时凭证通过指定方法访问OSS。

使用ECS实例角色凭证

1. 指定实例角色，例如角色名为 EcsRoleExample
```
from alibabacloud_credentials.client import Client
from alibabacloud_credentials.models import Config
import alibabacloud_oss_v2 as oss

config = Config(
    type='ecs_ram_role',      # 访问凭证类型。固定为ecs_ram_role。
    role_name='EcsRoleExample'    # 为ECS授予的RAM角色的名称。可选参数。如果不设置，将自动检索。强烈建议设置，以减少请求。
)

cred_client = Client(config)

def get_credentials_wrapper():
    cred = cred_client.get_credential()
    return oss.credentials.Credentials(access_key_id=cred.access_key_id, access_key_secret=cred.access_key_secret, security_token=cred.security_token)

provider = oss.credentials.CredentialsProviderFunc(func=get_credentials_wrapper)

cfg = oss.config.load_default()
cfg.credentials_provider = provider
cfg.region = 'cn-hangzhou'

client = oss.Client(cfg)
```
   
2. 不指定实例角色
```
from alibabacloud_credentials.client import Client
from alibabacloud_credentials.models import Config
import alibabacloud_oss_v2 as oss

config = Config(
    type='ecs_ram_role',      # 访问凭证类型。固定为ecs_ram_role。
)

cred_client = Client(config)

def get_credentials_wrapper():
    cred = cred_client.get_credential()
    return oss.credentials.Credentials(access_key_id=cred.access_key_id, access_key_secret=cred.access_key_secret, security_token=cred.security_token)

provider = oss.credentials.CredentialsProviderFunc(func=get_credentials_wrapper)

cfg = oss.config.load_default()
cfg.credentials_provider = provider
cfg.region = 'cn-hangzhou'

client = oss.Client(cfg)
```
当不指定实例角色名时，会自动查询角色名。

### 静态凭证

您可以在应用程序中对凭据进行硬编码，显式设置要使用的访问密钥。

> **注意:** 请勿将凭据嵌入应用程序中，此方法仅用于测试目的。

1. 长期凭证
```
credentials_provider = oss.credentials.StaticCredentialsProvider("AKId", "AKSecrect")
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
```

2. 临时凭证
```
credentials_provider = oss.credentials.StaticCredentialsProvider("AKId", "AKSecrect", "Token")
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
```


### RAM角色

如果您需要授权访问或跨账号访问OSS，您可以通过RAM用户扮演对应RAM角色的方式授权访问或跨账号访问OSS。

SDK 不直接提供该访问凭证实现，需要结合阿里云凭证库[credentials-python](https://github.com/aliyun/credentials-python)，具体配置如下:

```
# -*- coding: utf-8 -*-
import os
from alibabacloud_credentials.client import Client
from alibabacloud_credentials.models import Config
import alibabacloud_oss_v2 as oss

config = Config(
    # 从环境变量中获取RAM用户的访问密钥（AccessKey ID和AccessKey Secret）
    access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    type='ram_role_arn',
    # 要扮演的RAM角色ARN，示例值：acs:ram::123456789012****:role/adminrole，可以通过环境变量ALIBABA_CLOUD_ROLE_ARN设置RoleArn
    role_arn='<RoleArn>',
    # 角色会话名称，可以通过环境变量ALIBABA_CLOUD_ROLE_SESSION_NAME设置RoleSessionName
    role_session_name='<RoleSessionName>',
    # 设置更小的权限策略，非必填。示例值：{"Statement": [{"Action": ["*"],"Effect": "Allow","Resource": ["*"]}],"Version":"1"}
    policy='<Policy>',
    # 设置角色会话有效期，非必填
    role_session_expiration=3600
)

cred_client = Client(config)

def get_credentials_wrapper():
    cred = cred_client.get_credential()
    return oss.credentials.Credentials(access_key_id=cred.access_key_id, access_key_secret=cred.access_key_secret, security_token=cred.security_token)

provider = oss.credentials.CredentialsProviderFunc(func=get_credentials_wrapper)

cfg = oss.config.load_default()
cfg.credentials_provider = provider
cfg.region = 'cn-hangzhou'

client = oss.Client(cfg)

# 使用client进行后续操作...
```

### OIDC角色SSO

您也可以在应用或服务中使用OIDC认证访问OSS服务，关于OIDC角色SSO的更多信息，请参见[OIDC角色SSO概览](https://www.alibabacloud.com/help/zh/ram/user-guide/overview-of-oidc-based-sso)。

SDK 不直接提供该访问凭证实现，需要结合阿里云凭证库[credentials-go](https://github.com/aliyun/credentials-go)，具体配置如下:

```
# -*- coding: utf-8 -*-
import os
from alibabacloud_credentials.client import Client
from alibabacloud_credentials.models import Config
import alibabacloud_oss_v2 as oss

config = Config(
    # 指定Credential类型，固定值为oidc_role_arn。
    type='oidc_role_arn',
    # RAM角色名称ARN，可以通过环境变量ALIBABA_CLOUD_ROLE_ARN设置RoleArn
    role_arn=os.environ.get('<RoleArn>'),
    # OIDC提供商ARN，可以通过环境变量ALIBABA_CLOUD_OIDC_PROVIDER_ARN设置OidcProviderArn
    oidc_provider_arn=os.environ.get('<OidcProviderArn>'),
    # OIDC Token文件路径，可以通过环境变量ALIBABA_CLOUD_OIDC_TOKEN_FILE设置OidcTokenFilePath
    oidc_token_file_path=os.environ.get('<OidcTokenFilePath>'),
    # 角色会话名称，可以通过环境变量ALIBABA_CLOUD_ROLE_SESSION_NAME设置RoleSessionName
    role_session_name='<RoleSessionName>',
    # 设置更小的权限策略，非必填。示例值：{"Statement": [{"Action": ["*"],"Effect": "Allow","Resource": ["*"]}],"Version":"1"}
    policy='<Policy>',
    # 设置session过期时间
    role_session_expiration=3600
)

cred_client = Client(config)

def get_credentials_wrapper():
    cred = cred_client.get_credential()
    return oss.credentials.Credentials(access_key_id=cred.access_key_id, access_key_secret=cred.access_key_secret, security_token=cred.security_token)

provider = oss.credentials.CredentialsProviderFunc(func=get_credentials_wrapper)

cfg = oss.config.load_default()
cfg.credentials_provider = provider
cfg.region = 'cn-hangzhou'

client = oss.Client(cfg)

# 使用client进行后续操作...
```

### 自定义凭证提供者

当以上凭证配置方式不满足要求时，您可以自定义获取凭证的方式。SDK支持多种实现方式。

1. 实现 credentials.CredentialsProvider 接口
```
# -*- coding: utf-8 -*-
import alibabacloud_oss_v2 as oss

class CredentialProviderWrapper(oss.credentials.CredentialsProvider):
    def get_credentials(self):
        # TODO
        # 自定义访问凭证的获取方法

        # 返回长期凭证access_key_id, access_key_secrect
        return oss.credentials.Credentials('<access_key_id>', '<access_key_secrect>')

        # 返回 临时凭证access_key_id, access_key_secrect, token
        # 对于临时凭证，需要根据过期时间，刷新凭证。
        # return oss.credentials.Credentials('<access_key_id>', '<access_key_secrect>', '<token>');


credentials_provider = CredentialProviderWrapper()

cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = 'cn-chengdu'

client = oss.Client(cfg)

# 使用client进行后续操作...

```

2. 通过 credentials.CredentialsProviderFunc

credentials.CredentialsProviderFunc 是 credentials.CredentialsProvider 的 易用性封装。

```
# -*- coding: utf-8 -*-
import alibabacloud_oss_v2 as oss

def get_credentials_wrapper():
    # 返回长期凭证
    return oss.credentials.Credentials(access_key_id='access_key_id', access_key_secret='access_key_security')
    # # 返回临时凭证
    # return oss.credentials.Credentials(access_key_id='access_key_id', access_key_secret='access_key_security', security_token='security_token')

provider = oss.credentials.CredentialsProviderFunc(func=get_credentials_wrapper)

cfg = oss.config.load_default()
cfg.credentials_provider = provider
cfg.region = 'cn-hangzhou'

client = oss.Client(cfg)

# 使用client进行后续操作...
```


## 访问域名

您可以通过Endpoint参数，自定义服务请求的访问域名。

当不指定时，SDK根据Region信息，构造公网访问域名。例如当Region为'cn-hangzhou'时，构造出来的访问域名为'oss-cn-hangzhou.aliyuncs.com'。

您可以通过修改配置参数，构造出其它访问域名，例如 内网访问域名，传输加速访问域名 和 双栈(IPV6,IPV4)访问域名。有关OSS访问域名规则，请参考[OSS访问域名使用规则](https://www.alibabacloud.com/help/zh/oss/user-guide/oss-domain-names)。

当通过自定义域名访问OSS服务时，您需要指定该配置参数。在使用自定义域名发送请求时，请先绑定自定域名至Bucket默认域名，具体操作详见 [绑定自定义域名](https://www.alibabacloud.com/help/zh/oss/user-guide/map-custom-domain-names-5)。


### 使用标准域名访问

以 访问 Region 'cn-hangzhou' 为例

1. 使用公网域名

```
cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'

或者

cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.endpoint = 'oss-cn-hanghzou.aliyuncs.com'
```

2. 使用内网域名

```

cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.use_internal_endpoint = True

或者

cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.endpoint = 'oss-cn-hanghzou-internal.aliyuncs.com'
```
   
3. 使用传输加速域名
```
cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.use_accelerate_endpoint = True

或者

cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.endpoint = 'oss-accelerate.aliyuncs.com'
```   
   
4. 使用双栈域名
```
cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.use_dualstack_endpoint = True

或者

cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.endpoint = 'cn-hangzhou.oss.aliyuncs.com'
```   

### 使用自定义域名访问

以 'www.example-***.com' 域名 绑定到 'cn-hangzhou' 区域 的 bucket-example 存储空间为例

```
cfg = oss.config.load_default()
cfg.region = 'cn-hangzhou'
cfg.endpoint = 'www.example-***.com'
cfg.use_cname = True
```

### 访问专有云或专有域

```
region = "YOUR Region"
endpoint = "YOUR Endpoint"

cfg = oss.config.load_default()
cfg.region = region
cfg.endpoint = endpoint
```

## HTTP客户端

在大多数情况下，使用具有默认值的默认HTTP客户端 能够满足业务需求。您也可以更改HTTP 客户端，或者更改 HTTP 客户端的默认配置，以满足特定环境下的使用需求。

本部分将介绍如何设置 和 创建 HTTP 客户端。

### 设置HTTP客户端常用配置

通过config修改常用的配置，支持参数如下：

|参数名字 | 说明                     | 示例 
|:-------|:-----------------------|:-------
|connect_timeout| 建立连接的超时时间, 默认值为 10 秒   |oss.config.Config(connect_timeout=10)
|readwrite_timeout| 应用读写数据的超时时间, 默认值为 20 秒 |oss.config.Config(readwrite_timeout=20)
|insecure_skip_verify| 是否跳过SSL证书校验，默认检查SSL证书  |oss.config.Config(insecure_skip_verify=True)
|enabled_redirect| 是否开启HTTP重定向, 默认不开启     |oss.config.Config(enabled_redirect=False)
|proxy_host| 设置代理服务器                |oss.config.Config(proxy_host='http://user:passswd@proxy.example-***.com')


示例

```
cfg = oss.config.load_default()
cfg.connect_timeout=10
```

### 自定义HTTP客户端

当常用配置参数无法满足场景需求时，可以使用 cfg.http_client 替换默认的 HTTP 客户端。

在以下示例未提到的设置参数，请参考 [transport](https://gosspublic.alicdn.com/sdk-doc/alibabacloud-oss-python-sdk-v2/latest/_modules/alibabacloud_oss_v2/transport/requests_client.html#RequestsHttpClient) 文档。

```
# 常用超时或其它设置
kwargs: Dict[str, Any] = {}
# 设置session
# kwargs["session"] = requests.Session()
# 设置adapter
# kwargs["adapter"] = HTTPAdapter()
# 是否跳过证书检查，默认不跳过
# kwargs["insecure_skip_verify"] = False
# 是否打开启HTTP重定向，默认不启用
# kwargs["enabled_redirect"] = False
# 设置代理服务器 
# kwargs["proxy_host"] = config.proxy_host
# 设置块大小
# kwargs["block_size"] = 16 * 1024
# 连接超时, 默认值 10秒
kwargs["connect_timeout"] = 30
# 应用读写数据的超时时间, 默认值 20秒
kwargs["readwrite_timeout"] = 30
# 最大连接数，默认值 20
kwargs["max_connections"] = 1024

cfg = oss.config.load_default()
cfg.http_client = oss.transport.RequestsHttpClient(**kwargs)

```

## 重试

您可以配置对HTTP请求的重试行为。

### 默认重试策略

当没有配置重试策略时，SDK 使用 StandardRetryer() 作为客户端的默认实现，其默认配置如下：

|参数名称 | 说明 | 默认值 
|:-------|:-------|:-------
|max_attempts|最大尝试次数| 3
|max_backoff|最大退避时间| 20秒
|base_delay|基础延迟| 0.2秒(200毫秒)
|backoff_delayer|退避算法| FullJitter 退避,  [0.0, 1.0) * min(2 ^ attempts * baseDealy, maxBackoff)
|error_retryables|可重试的错误| 具体的错误信息，请参见[重试错误](https://gosspublic.alicdn.com/sdk-doc/alibabacloud-oss-python-sdk-v2/latest/_modules/alibabacloud_oss_v2/retry/error_retryable.html)

当发生可重试错误时，将使用其提供的配置来延迟并随后重试该请求。请求的总体延迟会随着重试次数而增加，如果默认配置不满足您的场景需求时，需要配置重试参数 或者修改重试实现。

### 调整最大尝试次数

您可以通过以下两种方式修改最大尝试次数。例如 最多尝试 5  次 

```
cfg.retry_max_attempts = 5

或者

cfg.retryer = oss.retry.StandardRetryer(max_attempts=5)
```

### 调整退避延迟

例如 调整 BaseDelay 为 500毫秒，最大退避时间为 25秒

```
cfg.retryer = oss.retry.StandardRetryer(max_backoff=25, base_delay=0.5)
```

### 调整退避算法

例如 使用固定时间退避算法，每次延迟2秒 

```
cfg.retryer = oss.retry.StandardRetryer(backoff_delayer=oss.retry.FixedDelayBackoff(2))
```

### 调整重试错误

例如 在原有基础上，新增自定义可重试错误

```
class CustomErrorCodeRetryable(error_retryable.ErrorRetryable):
    def is_error_retryable(self, error: Exception) -> bool:
        # 判断错误
        # return true
        return False

cfg.retryer = oss.retry.StandardRetryer(
            error_retryables=[CustomErrorCodeRetryable()]
        )
```

### 禁用重试

当您希望禁用所有重试尝试时，可以使用 retry.NopRetryer 实现
```
cfg.retryer = oss.retry.NopRetryer()
```


## 配置参数汇总

支持的配置参数：

|参数名字 | 说明                               | 示例 
|:-------|:---------------------------------|:-------
|region| (必选)请求发送的区域, 必选                  |oss.config.Config(region="cn-hangzhou")
|credentials_provider| (必选)设置访问凭证                       |oss.config.Config(credentials_provider=provider)
|endpoint| 访问域名                             |oss.config.Config(endpoint="oss-cn-hanghzou.aliyuncs.com")
|http_client| HTTP客户都端                         |oss.config.Config(http_client=customClient)
|retry_max_attempts| HTTP请求时的最大尝试次数, 默认值为 3           |oss.config.Config(retry_max_attempts=5)
|retryer| HTTP请求时的重试实现                     |oss.config.Config(retryer=customRetryer)
|connect_timeout| 建立连接的超时时间, 默认值为 10 秒             |oss.config.Config(connect_timeout=20)
|readwrite_timeout30| 应用读写数据的超时时间, 默认值为 20 秒           |oss.config.Config(readwrite_timeout30)
|insecure_skip_verify| 是否跳过SSL证书校验，默认检查SSL证书            |oss.config.Config(insecure_skip_verify=true)
|enabled_redirect| 是否开启HTTP重定向, 默认不开启               |oss.config.Config(enabled_redirect=true)
|proxy_host| 设置代理服务器                          |oss.config.Config(proxy_host="http://user:passswd@proxy.example-***.com")
|signature_version| 签名版本，默认值为v4                      |oss.config.Config(signature_version="v1")
|disable_ssl| 不使用https请求，默认使用https             |oss.config.Config(disable_ssl=true)
|use_path_style| 使用路径请求风格，即二级域名请求风格，默认为bucket托管域名 |oss.config.Config(use_path_style=true)
|use_cname| 是否使用自定义域名访问，默认不使用                |oss.config.Config(use_cname=true)
|use_dualstack_endpoint| 是否使用双栈域名访问，默认不使用                 |oss.config.Config(use_dualstack_endpoint=true)
|use_accelerate_endpoint| 是否使用传输加速域名访问，默认不使用               |oss.config.Config(use_accelerate_endpoint=true)
|use_internal_endpoint| 是否使用内网域名访问，默认不使用                 |oss.config.Config(use_internal_endpoint=true)
|disable_upload_crc64_check| 上传时关闭CRC64校验，默认开启CRC64校验         |oss.config.Config(disable_upload_crc64_check=true)
|disable_download_crc64_check| 下载时关闭CRC64校验，默认开启CRC64校验         |oss.config.Config(disable_download_crc64_check=true)
|additional_headers| 指定额外的签名请求头，V4签名下有效               |oss.config.Config(additional_headers=["content-length"])
|user_agent| 指定额外的User-Agent信息                |oss.config.Config(user_agent="user identifier")

# 接口说明

本部分介绍SDK提供的接口, 以及如何使用这些接口。

此部分的其它主题
* [基础接口](#基础接口)
* [预签名接口](#预签名接口)
* [分页器](#分页器)
* [传输管理器](#传输管理器)
* [类文件(File-Like)](#类文件file-like)
* [客户端加密](#客户端加密)
* [其它接口](#其它接口)
* [上传下载接口对比](#上传下载接口对比)

## 基础接口

SDK 提供了 与 REST API 对应的接口，把这类接口叫做 基础接口 或者 低级别API。您可以通过这些接口访问OSS的服务，例如创建存储空间，更新和删除存储空间的配置等。

这些接口采用了相同的命名规则，其接口定义如下：

```
def <OperationName>(self, request: models.<OperationRequestName>, **kwargs
                 ) -> models.<OperationResulttName>:
    return operations.<OperationName>(self._client, request, **kwargs)
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|request|*\<OperationName\>Request|设置具体接口的请求参数，例如bucket，key
|**kwargs|Any|(可选)任意参数，类型为字典, 例如header

**返回值列表**：

|返回值名|类型|说明
|:-------|:-------|:-------
|result|*\<OperationName\>Result|接口返回值，当 Exception 为None 时有效

示例：
1. 创建存储空间

```
client = oss.Client(cfg)

result = client.put_bucket(oss.PutBucketRequest(
    bucket="example_bucket",
    acl='private',
    create_bucket_configuration=oss.CreateBucketConfiguration(
        storage_class='IA'
    )
))
print(vars(result))
```

2. 拷贝对象, 同时设置接口级的读写超时

```
client = oss.Client(cfg)

kwargs: Dict[str, Any] = {}
kwargs["readwrite_timeout"] = 30

result = client.copy_object(oss.CopyObjectRequest(
    bucket="example_bucket",
    key="example_key",
    source_key="example_source_key",
    source_bucket="example_source_bucket",
    ), **kwargs)
print(vars(result))
```

更多的示例，请参考 sample 目录

## 预签名接口

您可以使用预签名接口生成预签名URL，授予对存储空间中对象的限时访问权限，或者允许他人将特定对象的上传到存储空间。在过期时间之前，您可以多次使用预签名URL。

预签名接口定义如下：
```
def presign(self, request: PresignRequest, **kwargs) -> PresignResult:
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|request|PresignRequest|设置需要生成签名URL的接口名，和 '\<OperationName\>Request' 一致
|**kwargs|Any|(可选)，设置过期时间等

**返回值列表**：

|返回值名|类型|说明
|:-------|:-------|:-------
|result|PresignResult|返回结果，包含 预签名URL，HTTP 方法，过期时间 和 参与签名的请求头

**request参数支持的类型**：

|类型|对应的接口
|:-------|:-------
|GetObjectRequest|get_object
|PutObjectRequest|put_object
|HeadObjectRequest|head_object
|InitiateMultipartUploadRequest|initiate_multipart_upload
|UploadPartRequest|upload_part
|CompleteMultipartUploadRequest|complete_multipart_upload
|AbortMultipartUploadRequest|abort_multipart_upload

**PresignOptions选项**

|选项值|类型|说明
|:-------|:-------|:-------
|expires|datetime.datetime|从当前时间开始，多长时间过期。例如 设置一个有效期为30分钟，datetime.timedelta(minutes=30)
|expiration_time|datetime.datetime|绝对过期时间

> **注意:** 在签名版本4下，有效期最长为7天。同时设置 Expiration 和 Expires时，优先取 Expiration。

**PresignResult返回值**：

|参数名|类型|说明
|:-------|:-------|:-------
|method|str|HTTP 方法，和 接口对应，例如get_object接口，返回 GET
|url|str|预签名 URL
|expiration|datetime.datetime| 签名URL的过期时间
|signed_headers|MutableMapping|被签名的请求头，例如put_object接口，设置了Content-Type 时，会返回 Content-Type 的信息。

示例
1. 为对象生成预签名 URL，然后下载对象（GET 请求）
```
client = oss.Client(cfg)

pre_result = client.presign(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
))

with requests.get(pre_result.url) as resp:
    print(vars(resp))
```

2. 为上传生成预签名 URL, 设置自定义元数据，有效期为10分钟，然后上传文件（PUT 请求）
```
client = oss.Client(cfg)

data = b'hello world'

kwargs: Dict[str, Any] = {}
kwargs["expires"] = datetime.timedelta(minutes=10)

pre_result = client.presign(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
    content_type='text/txt'
), **kwargs)

with requests.put(pre_result.url, headers=pre_result.signed_headers, data=data) as resp:
    print(vars(resp))
```

更多的示例，请参考 sample 目录


## 分页器

对于列举类接口，当响应结果太大而无法在单个响应中返回时，都会返回分页结果，该结果同时包含一个用于检索下一页结果的标记。当需要获取下一页结果时，您需要在发送请求时设置该标记。

对常用的列举接口，V2 SDK 提供了分页器（Paginator），支持自动分页，当进行多次调用时，自动为您获取下一页结果。使用分页器时，您只需要编写处理结果的代码。

分页器 包含了 分页器对象 '\<OperationName\>Paginator' 和 分页器创建方法 '\<OperationName\>_paginator'。分页器创建方法返回一个分页器对象，该对象实现了 'iter_page' 方法，用于调用操作来获取下一页。

分页器创建方法 '\<OperationName\>_paginator' 里的 request 参数类型 与 '\<OperationName\>' 接口中的 reqeust 参数类型一致。

'\<OperationName\>_paginator.iter_page' 返回的结果类型 和 '\<OperationName\>' 接口 返回的结果类型 一致。

```
class <OperationName>Paginator:
    ...

def iter_page(self, request: <OperationName>Request, **kwargs: Any) -> Iterator[<OperationName>Result]:
    ...


def <OperationName>_paginator(self, **kwargs) -> <OperationName>Paginator:
    ...
```

支持的分页器对象如下：

|分页器对象|创建方法|对应的列举接口
|:-------|:-------|:-------
|ListObjectsPaginator|list_objects_paginator|ListObjects, 列举存储空间中的对象信息
|ListObjectsV2Paginator|list_objects_v2_paginator|ListObjectsV2, 列举存储空间中的对象信息
|ListObjectVersionsPaginator|list_object_versions_paginator|ListObjectVersions, 列举存储空间中的对象版本信息
|ListBucketsPaginator|list_buckets_paginator|ListBuckets, 列举存储空间
|ListPartsPaginator|list_parts_paginator|ListParts, 列举指定Upload ID所属的所有已经上传成功分片
|ListMultipartUploadsPaginator|list_multipart_uploads_paginator|ListMultipartUploads, 列举存储空间中的执行中的分片上传事件

PaginatorOptions 选项说明：

|参数|说明
|:-------|:-------
|Limit|指定返回结果的最大数


以 list_objects 为例，分页器遍历所有对象 和 手动分页遍历所有对象 对比

```
// 分页器遍历所有对象
...
client = oss.Client(cfg)

# Create the Paginator for the ListObjects operation
paginator = client.list_objects_paginator()

# Iterate through the object pages
for page in paginator.iter_page(oss.ListObjectsRequest(
        bucket="example_bucket"
    )
):
    for o in page.contents:
        print(vars(o))
```

```
// 手动分页遍历所有对象
...
client = oss.Client(cfg)

marker=''
while True:
    result = client.list_objects(oss.ListObjectsRequest(
            bucket="example_bucket",
            marker=marker
        ))
    for o in result.contents:
        print(vars(o))
    if result.is_truncated:
        marker=result.next_marker
        continue
        
    else:
        break
```


## 传输管理器

针对大文件的传输场景，新增了 'Uploader'，'Downloader' 和 'Copier' 模块，分别管理对象的 上传，下载 和 拷贝。

### 上传管理器(Uploader)

上传管理器 利用分片上传接口，把大文件或者流分成多个较小的分片并发上传，提升上传的性能。
</br>针对文件的上传场景，还提供了断点续传的能力，即在上传过程中，记录已完成的分片状态，如果出现网络中断、程序异常退出等问题导致文件上传失败，甚至重试多次仍无法完成上传，再次上传时，可以通过断点记录文件恢复上传。

```
class Uploader:
  ...

def uploader(self, **kwargs) -> Uploader:
  ...

def upload_file(self, request: models.PutObjectRequest, filepath: str, **kwargs: Any) -> UploadResult:
  ...
  
def upload_from(self, request: models.PutObjectRequest, reader: IO[bytes], **kwargs: Any) -> UploadResult:
  ...
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|request|PutObjectRequest|上传对象的请求参数，和 PutObject 接口的 请求参数一致
|reader|IO[bytes]|需要上传的流
|filepath|str|本地文件路径
|**kwargs|Any|(可选)任意参数，类型为字典


**UploaderOptions选项说明：**

|参数|类型|说明
|:-------|:-------|:-------
|part_size|int|指定分片大小，默认值为 6MiB
|parallel_num|int|指定上传任务的并发数，默认值为 3。针对的是单次调用的并发限制，而不是全局的并发限制
|leave_parts_on_error|bool|当上传失败时，是否保留已上传的分片，默认不保留 
|enable_checkpoint|bool|是否记录断点上传信息，默认不记录
|checkpoint_dir|str|指定记录文件的保存路径，例如 /local/dir/, 当enable_checkpoint 为 true时有效


当使用uploader实例化实例时，您可以指定多个配置选项来自定义对象的上传行为。也可以在每次调用上传接口时，指定多个配置选项来自定义每次上传对象的行为。

设置Uploader的配置参数
```
up_loader = client.uploader(
    part_size=10 * 1024 * 1024,
)
```

设置每次上传请求的配置参数
```
result = up_loader.upload_file(oss.PutObjectRequest(
        bucket="example_bucket",
        key="example_key",
    ),
    filepath="/local/dir/example",
    part_size=10 * 1024 * 1024,
)
```

示例

1. 使用 Uploader上传流

```
...
client = oss.Client(cfg)

up_loader = client.uploader()

data = b'hello world'
result = up_loader.upload_from(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
), reader=data)
print(vars(result))
```

2. 使用 Uploader上传文件

```
...
client = oss.Client(cfg)

up_loader = client.uploader()

result = up_loader.upload_file(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
), filepath="/local/dir/example")

print(vars(result))
```

3. 上传文件，并开启断点续传功能
```
...
client = oss.Client(cfg)

up_loader = client.uploader(
            enable_checkpoint=True,
            checkpoint_dir="/local/dir/"
        )

result = up_loader.upload_file(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
), filepath="/local/dir/example")

print(vars(result))
```

### 下载管理器(Downloader)

下载管理器 利用范围下载，把大文件分成多个较小的分片并发下载，提升下载的性能。
</br>该接口提供了断点续传的能力，即在下载过程中，记录已完成的分片状态，如果出现网络中断、程序异常退出等问题导致文件下载失败，甚至重试多次仍无法完成下载，再次下载时，可以通过断点记录文件恢复下载。

```
class Downloader:
  ...

def downloader(self, **kwargs) -> Downloader:
  ...

def download_file(self, request: models.GetObjectRequest, filepath: str, **kwargs: Any) -> DownloadResult:
  ...
  
def download_to(self, request: models.GetObjectRequest, writer: IO[bytes], **kwargs: Any) -> DownloadResult:
  ...
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|request|GetObjectRequest|下载对象的请求参数，和 GetObject 接口的 请求参数一致
|filePath|str|本地文件路径
|writer|IO[bytes]|下载的流
|**kwargs|Any|(可选)任意参数，类型为字典


**DownloaderOptions选项说明：**

|参数|类型|说明
|:-------|:-------|:-------
|part_size|int|指定分片大小，默认值为 6MiB
|parallel_num|int|指定上传任务的并发数，默认值为 3。针对的是单次调用的并发限制，而不是全局的并发限制
|enable_checkpoint|bool|是否记录断点下载信息，默认不记录
|checkpoint_dir|string|指定记录文件的保存路径，例如 /local/dir/, 当enable_checkpoint 为 true时有效
|verify_data|bool|恢复下载时，是否要校验已下载数据的CRC64值，默认不校验, 当enable_checkpoint 为 true时有效
|use_temp_file |bool|下载文件时，是否使用临时文件，默认使用。先下载到临时文件上，当成功后，再重命名为目标文件


当使用downloader实例化实例时，您可以指定多个配置选项来自定义对象的下载行为。也可以在每次调用下载接口时，指定多个配置选项来自定义每次下载对象的行为。

设置Downloader的配置参数
```
down_loader = client.downloader(
    part_size=10 * 1024 * 1024,
)
```

设置每次下载请求的配置参数
```
result = down_loader.download_file(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
),
    filepath="/local/dir/example",
    part_size=10 * 1024 * 1024,
)
```

示例

1. 使用 Downloader 下载到本地文件

```
...
client = oss.Client(cfg)

down_loader = client.downloader()

result = down_loader.download_file(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
), filepath="/local/dir/example")
print(vars(result))
```

2. 使用 Downloader下载流

```
...
client = oss.Client(cfg)

down_loader = client.downloader()

buffer = io.BytesIO()
result = down_loader.download_to(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
), writer=buffer)
print(vars(result))
print(buffer.getvalue())
```

### 拷贝管理器(Copier) 
当需要将对象从存储空间复制到另外一个存储空间，或者修改对象的属性时，您可以通过拷贝接口 或者分片拷贝接口来完成这个操作。
</br>这两个接口有其适用的场景，例如：
* 拷贝接口(copy_object) 只适合拷贝 5GiB 以下的对象；
* 分片拷贝接口(upload_part_copy) 不支持 元数据指令(x-oss-metadata-directive) 和 标签指令(x-oss-tagging-directive) 参数, 
拷贝时，您需要主动去设置需要复制的元数据和标签。
* 服务端优化了拷贝(copy_object)接口，使其具备浅拷贝的能力，在特定的场景下也支持拷贝大文件。

拷贝管理器提供了通用的拷贝接口，隐藏了接口的差异和实现细节，根据拷贝的请求参数，自动选择合适的接口复制对象。

```
class CopyError(exceptions.BaseError):
  ...

def copier(self, **kwargs) -> Copier:
  ...

def copy(self, request: models.CopyObjectRequest, **kwargs: Any) -> CopyResult:
  ...
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|request|CopyObjectRequest|拷贝对象的请求参数，和 CopyObject 接口的 请求参数一致
|**kwargs|Any|(可选)任意参数，类型为字典


**CopierOptions选项说明：**

|参数|类型|说明
|:-------|:-------|:-------
|part_size|int|指定分片大小，默认值为 64MiB
|parallel_num|int|指定上传任务的并发数，默认值为 3。针对的是单次调用的并发限制，而不是全局的并发限制
|multipart_copy_threshold|int|使用分片拷贝的阈值，默认值为 200MiB
|leave_parts_on_error|bool|当拷贝失败时，是否保留已拷贝的分片，默认不保留 
|disable_shallow_copy|bool|不使用浅拷贝行为，默认使用


当使用NCopier实例化实例时，您可以指定多个配置选项来自定义对象的下载行为。也可以在每次调用下载接口时，指定多个配置选项来自定义每次下载对象的行为。

设置Copier的配置参数
```
copier = client.copier(
    part_size=100 * 1024 * 1024,
)
```

设置每次拷贝请求的配置参数
```
result = copier.copy(oss.CopyObjectRequest(
        bucket="example_bucket",
        key="example_key",
        source_bucket="example_source_bucket",
        source_key="example_source_key",
    ),
    part_size=100 * 1024 * 1024,
)
```

> **注意:**
> </br>拷贝对象时，CopyObjectRequest.metadata_directive 决定了对象元数据的拷贝行为，默认 复制 源对象标签
> </br>拷贝对象时，CopyObjectRequest.tagging_directive 决定了对象标签的拷贝行为，默认 复制 源对象标签 


示例

1. 拷贝文件，默认会复制 元数据 和 标签
```
...
client = oss.Client(cfg)

result = client.copy_object(oss.CopyObjectRequest(
    bucket="example_bucket",
    key="example_key",
    source_bucket="example_source_bucket",
    source_key="example_source_key",
))

print(vars(result))
```

2. 拷贝文件，只拷贝数据，不拷贝元数据和标签
```
...
client = oss.Client(cfg)

result = client.copy_object(oss.CopyObjectRequest(
    bucket="example_bucket",
    key="example_key",
    source_bucket="example_source_bucket",
    source_key="example_source_key",
    metadata_directive="replace",
    tagging_directive="replace",
))

print(vars(result))
```

3. 修改 对象的存储类型 为标准类型

```
...
client = oss.Client(cfg)

result = client.copy_object(oss.CopyObjectRequest(
    bucket="example_bucket",
    key="example_key",
    source_key="example_source_key",
    source_bucket="example_source_bucket",
    storage_class=oss.StorageClassType.STANDARD,
))

print(vars(result))
```

## 类文件(File-Like)

新增了File-Like接口，提供了模仿文件的读写行为来操作存储空间里的对象。

支持以下两种方式：
* 只读(ReadOnlyFile)
* 追加写(AppendOnlyFile)

### 只读文件(ReadOnlyFile)

以只读方式访问存储空间的对象。在只读方式上，提供了 单流 和 并发+预取 两种模式，您可以根据场景需要，调整并发数，以提升读的速度。同时，内部实现了连接断掉重连的机制，在一些比较复杂的网络环境下，具备更好的鲁棒性。

```
class ReadOnlyFile:
    ...


def open_file(self, bucket: str, key: str, version_id: Optional[str] = None, request_payer: Optional[str] = None, **kwargs) -> ReadOnlyFile:
    ...
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|bucket|str|设置存储空间名字
|key|str|设置对象名
|version_id|str|指定对象的版本号，多版本下有效
|request_payer|str|启用了请求者付费模式时，需要设置为'requester'
|**kwargs|Any|(可选)任意参数，类型为字典

**返回值列表**：

|返回值名|类型|说明
|:-------|:-------|:-------
|file|ReadOnlyFile|只读文件的实例


** **kwargs参数说明：**

|参数|类型|说明
|:-------|:-------|:-------
|enable_prefetch|bool|是否启用预取模式，默认不启用
|prefetch_num|int|预取块的数量，默认值为3。启用预取模式时有效
|chunk_size|int|每个预取块的大小，默认值为6MiB。启用预取模式时有效
|prefetch_threshold|int|持续顺序读取多少字节后进入到预取模式，默认值为20MiB。启用预取模式时有效
|block_size|int|块的大小，默认值为None

**ReadOnlyFile接口：**

|接口名|说明
|:-------|:-------
|close(self)|关闭文件句柄，释放资源，例如内存，活动的socket 等
|read(self, n=None)|从数据源中读取长度为len(p)的字节，存储到p中，返回读取的字节数和遇到的错误
|seek(self, pos, whence=0)|用于设置下一次读或写的偏移量。其中whence的取值：0：相对于头部，1：相对于当前偏移量，2：相对于尾部


> **注意:** 当预取模式打开时，如果出现多次乱序读时，则会自动退回单流模式。

示例 

1. 以单流模式，读取整个对象
```
...
client = oss.Client(cfg)

rf: oss.ReadOnlyFile = None
with client.open_file("example_bucket", "example_key") as f:
    rf = f
    copied_stream = io.BytesIO(rf.read())
    print(f'written: {len(copied_stream.getvalue())}')
```

2. 启用预取模式，读取整个对象
```
...
client = oss.Client(cfg)

kwargs: Dict[str, Any] = {}
kwargs["enable_prefetch"] = True

rf: oss.ReadOnlyFile = None
with client.open_file("example_bucket", "example_key", **kwargs) as f:
    rf = f
    copied_stream = io.BytesIO(rf.read())
    print(f'written: {len(copied_stream.getvalue())}')
```

3. 通过Seek方法，从指定位置开始读取剩余的数据

```
...
client = oss.Client(cfg)

rf: oss.ReadOnlyFile = None
with client.open_file("example_bucket", "example_key") as f:
    rf = f
    f.seek(123, os.SEEK_SET)
    copied_stream = io.BytesIO(rf.read())
    print(f'written: {len(copied_stream.getvalue())}')
```

### 追加写文件(AppendOnlyFile)

调用append_object接口以追加写的方式上传数据。如果对象不存在，则创建追加类型的对象。如果对象存在，并且不为追加类型的对象时，则返回错误。

```
class AppendOnlyFile:
    ...

def append_file(self, bucket: str, key: str, request_payer: Optional[str] = None, create_parameter: Optional[models.AppendObjectRequest] = None, **kwargs) -> AppendOnlyFile:
    ...
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|bucket|str|设置存储空间名字
|key|str|设置对象名
|request_payer|str|启用了请求者付费模式时，需要设置为'requester'
|create_parameter|AppendObjectRequest|(可选)，用于首次上传时，设置对象的元信息，包括ContentType，Metadata，权限，存储类型 等
|**kwargs|Any|(可选)任意参数，类型为字典

**返回值列表**：

|返回值名|类型|说明
|:-------|:-------|:-------
|file|*AppendOnlyFile|追加文件的实例

**AppendOnlyFile接口：**

|接口名|说明
|:-------|:-------
|close(self)|关闭文件句柄，释放资源
|write(self, b)|将字节b中的数据写入到数据流中，返回写入的字节数
|write_from(self, b:BodyType)|将任何数据b写入到数据流中，返回写入的字节数
|flush(self)|刷新写缓冲区
|tell(self)|返回一个表示当前流位置的整数
|writable(self)|如果文件是以写模式打开的，则为True


示例 

1. 把多个本地文件合并成一个文件
```
...
client = oss.Client(cfg)

append_f: oss.AppendOnlyFile = None
with client.append_file("example_bucket", "example_key") as f:
    append_f = f
    init_size = append_f.tell()
    print(f'init size: {init_size}')

    with open('/local/dir/example1.txt', 'rb') as f1:
        n = append_f.write_from(f1)
        print(f'written: {n}')

    with open('/local/dir/example2.txt', 'rb') as f2:
        n = append_f.write_from(f2)
        print(f'written: {n}')

    size = append_f.tell()
    print(f'size: {size}')
```

2. 合并数据时，同时设置对象的权限和存储类型
```
...
data1 = "helle"
data2 = " world"

client = oss.Client(cfg)

append_f: oss.AppendOnlyFile = None
with client.append_file("example_bucket", "example_key", create_parameter=oss.AppendObjectRequest(
    acl='public-read',
    storage_class='IA',
    content_type='plain/txt',
    metadata={'user':"test"},
    tagging='TagA&TagB=B',
)) as f:
    append_f = f
    init_size = append_f.tell()
    print(f'init size: {init_size}')

    n = append_f.write(data1.encode())
    print(f'written: {n}')

    n = append_f.write(data2.encode())
    print(f'written: {n}')

    size = append_f.tell()
    print(f'size: {size}')
```

## 客户端加密

客户端加密是在数据上传至OSS之前，由用户在本地对数据进行加密处理，确保只有密钥持有者才能解密数据，增强数据在传输和存储过程中的安全性。

> **注意:** 
> </br>使用客户端加密功能时，您需要对主密钥的完整性和正确性负责。
> </br>在对加密数据进行复制或者迁移时，您需要对加密元数据的完整性和正确性负责。

如果您需要了解OSS客户端加密实现的原理，请参考OSS用户指南中的[客户端加密](https://www.alibabacloud.com/help/zh/oss/user-guide/client-side-encryption)。

使用客户端加密，首先您需要实例化加密客户端，然后调用其提供的接口进行操作。您的对象将作为请求的一部分自动加密和解密。

```
class EncryptionClient:
  ...


def __init__(self,client: Client, master_cipher: MasterCipher, decrypt_master_ciphers: Optional[List[MasterCipher]] = None)
```

**参数列表**：

|参数名|类型|说明
|:-------|:-------|:-------
|client|*Client| 非加密客户端实例
|master_cipher|MasterCipher|主密钥实例，用于加密和解密数据密钥
|decrypt_master_ciphers|List[MasterCipher]|主密钥实例，用于解密数据密钥

**EncryptionClient接口：**

|**基础接口名**|**说明**
|:-------|:-------
|get_object_meta|获取对象的部分元信息
|head_object|获取对象的部元信息
|get_object|下载对象，并自动解密
|put_object|上传对象，并自动加密
|initiate_multipart_upload|初始化一个分片上传事件 和 分片加密上下文（EncryptionMultiPartContext）
|upload_part|初始化一个分片上传事件, 调用该接口上传分片数据，并自动加密。调用该接口时，需要设置 分片加密上下文
|complete_multipart_upload|在将所有分片数据上传完成后，调用该接口合并成一个文件
|abort_multipart_upload|取消分片上传事件,并删除对应的分片数据
|list_parts|列举指定上传事件所属的所有已经上传成功分片


|**辅助接口名**|**说明**
|unwrap|获取非加密客户端实例，可以通过该实例访问其它基础接口

> **说明:** EncryptionClient 采用了 和 Client 一样的接口命名规则 和 调用方式，有关接口的详细用法，请参考指南的其它章节说明。

### 使用RSA主密钥

**创建RAS加密客户端**

```
import argparse
import alibabacloud_oss_v2 as oss

credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = "cn-hangzhou"

client = oss.Client(cfg)

// 创建只包含 主密钥 的 加密客户端
mc = oss.crypto.MasterRsaCipher(
    # 创建一个主密钥的描述信息，创建后不允许修改。主密钥描述信息和主密钥一一对应。
    # 如果所有的对象都使用相同的主密钥，主密钥描述信息可以为空，但后续不支持更换主密钥。
    # 如果主密钥描述信息为空，解密时无法判断使用的是哪个主密钥。
    # 强烈建议为每个主密钥都配置主密钥描述信息，由客户端保存主密钥和描述信息之间的对应关系。
    mat_desc={"desc": "your master encrypt key material describe information"},
    public_key="yourRsaPublicKey",
    private_key="yourRsaPrivateKey"
)
encryption_client = oss.EncryptionClient(client, mc)


// 创建包含主密钥 和 多个解密密钥的 加密客户端
mc = oss.crypto.MasterRsaCipher(
    # 创建一个主密钥的描述信息，创建后不允许修改。主密钥描述信息和主密钥一一对应。
    # 如果所有的对象都使用相同的主密钥，主密钥描述信息可以为空，但后续不支持更换主密钥。
    # 如果主密钥描述信息为空，解密时无法判断使用的是哪个主密钥。
    # 强烈建议为每个主密钥都配置主密钥描述信息，由客户端保存主密钥和描述信息之间的对应关系。
    mat_desc={"desc": "your master encrypt key material describe information"},
    public_key="yourRsaPublicKey",
    private_key="yourRsaPrivateKey"
)
// 当解密时，先匹配解密密钥的描述信息，如果不匹配，则使用主密钥解密
dmc = [oss.crypto.MasterRsaCipher(
    mat_desc={"desc": "your master encrypt key material describe information"},
    public_key=RSA_PUBLIC_KEY,
    private_key=RSA_PRIVATE_KEY
), oss.crypto.MasterRsaCipher(
    mat_desc={"desc": "your master encrypt key material describe information"},
    public_key=RSA_PUBLIC_KEY,
    private_key=RSA_PRIVATE_KEY
)]
encryption_client = oss.EncryptionClient(client, mc, dmc)
```

**使用加密客户端上传或者下载**
```
...
encryption_client = oss.EncryptionClient(client, mc)

// Use PutObject
data = b'hello world'

result = encryption_client.put_object(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
    body=data,
))

print(vars(result))


// Use GetObject
result = encryption_client.get_object(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
))

print(vars(result))


// Use ReadOnlyFile
rf: oss.ReadOnlyFile = None
with encryption_client.open_file("example_bucket", "example_key") as f:
    rf = f
    copied_stream = io.BytesIO(rf.read())
    print(f'written: {len(copied_stream.getvalue())}')
```

**使用加密客户端以分片方式上传数据**
</br>以上传本地文件/local/dir/example为例 
```
...
client = oss.Client(cfg)

part_size = 100 * 1024
data_size = os.path.getsize("/local/dir/example")

mc = oss.crypto.MasterRsaCipher(
    mat_desc={"tag": "your master encrypt key material describe information"},
    public_key=RSA_PUBLIC_KEY,
    private_key=RSA_PRIVATE_KEY
)
encryption_client = oss.EncryptionClient(client, mc)

result = encryption_client.initiate_multipart_upload(oss.InitiateMultipartUploadRequest(
    bucket="example_bucket",
    key="example_key",
    cse_part_size=part_size,
    cse_data_size=data_size
))
print(vars(result))

part_number = 1
upload_parts = []
with open("/local/dir/example", 'rb') as f:
    for start in range(0, data_size, part_size):
        n = part_size
        if start + n > data_size:
            n = data_size - start
        reader = oss.io_utils.SectionReader(oss.io_utils.ReadAtReader(f), start, n)
        up_result = encryption_client.upload_part(oss.UploadPartRequest(
            bucket="example_bucket",
            key="example_key",
            upload_id=result.upload_id,
            part_number=part_number,
            cse_multipart_context=result.cse_multipart_context,
            body=reader
        ))
        print(vars(result))

        upload_parts.append(oss.UploadPart(part_number=part_number, etag=up_result.etag))
        part_number += 1

parts = sorted(upload_parts, key=lambda p: p.part_number)
result = encryption_client.complete_multipart_upload(oss.CompleteMultipartUploadRequest(
    bucket="example_bucket",
    key="example_key",
    upload_id=result.upload_id,
    complete_multipart_upload=oss.CompleteMultipartUpload(
        parts=parts
    )
))
print(vars(result))

```

### 使用自定义主密钥
当RSA主密钥方式无法满足需求时，您可自定主密钥的加密实现。主密钥的接口定义如下：
```
class MasterCipher(abc.ABC):
    def encrypt(self, data: bytes) -> bytes:
    def decrypt(self, data: bytes) -> bytes:
    def get_wrap_algorithm(self) -> str:
    def get_mat_desc(self) -> str:
```
**MasterCipher接口说明**

|接口名|说明
|:-------|:-------
|encrypt|加密 数据加密密钥 和 加密数据的初始值(IV)
|decrypt|解密 数据加密密钥  和 加密数据的初始值(IV)
|get_wrap_algorithm|返回 数据密钥的加密算法信息，建议采用 算法/模式/填充 格式，例如RSA/NONE/PKCS1Padding
|get_mat_desc|返回 主密钥的描述信息，JSON格式

例如

```
...
class MasterCustomCipher(MasterCipher):
    def __init__(
        self,
        mat_desc: Optional[Dict] = None,
        public_key: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        self.public_key = public_key
        self.private_key = private_key
        self.mat_desc = mat_desc

    def get_wrap_algorithm(self) -> str:
        return 'Custom/None/NoPadding'

    def get_mat_desc(self) -> str:
        return self._mat_desc or ''

    def encrypt(self, data: bytes) -> bytes:
        # TODO

    def decrypt(self, data: bytes) -> bytes:
        # TODO
```

## 其它接口

为了方便用户使用，封装了一些易用性接口。当前扩展的接口如下：

|接口名 | 说明
|:-------|:-------
|is_object_exist|判断对象(object)是否存在
|is_bucket_exist|判断存储空间(bucket)是否存在
|put_object_from_file|上传本地文件到存储空间
|get_object_to_file|下载对象到本地文件

### is_object_exist/is_bucket_exist

这两个接口的返回值为 bool,如果bool 为 true，表示存在，如果 bool值为 false，表示不存在。当返回错误信息时，表示无法从该错误信息判断是否存在。

```
def is_object_exist(self, bucket: str, key: str, version_id: Optional[str] = None, request_payer: Optional[str] = None, **kwargs) -> bool:
def is_bucket_exist(self, bucket: str, request_payer: Optional[str] = None, **kwargs) -> bool:
```

例如 判断对象是否存在

```
client = oss.Client(cfg)

result = client.is_object_exist(
    bucket="example_bucket",
    key="example_key",
)

print(f'is exist: {result}')
```

### put_object_from_file

使用简单上传(put_object)接口 把本地文件上传到存储空间，该接口不支持并发。

```
def put_object_from_file(self, request: models.PutObjectRequest, filepath: str, **kwargs) -> models.PutObjectResult:
```

示例

```
client = oss.Client(cfg)

result = client.put_object_from_file(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key"
), "/local/dir/example")

print(vars(result))
```

### get_object_to_file

使用get_object接口，把存储空间的对象下载到本地文件，该接口不支持并发。

```
def get_object_to_file(self, request: models.GetObjectRequest, filepath: str, **kwargs) -> models.GetObjectResult: 
```

示例

```
client = oss.Client(cfg)

result = client.get_object_to_file(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key"
), "/local/dir/example")

print(vars(result))
```

## 上传下载接口对比

提供了各种上传下载接口，您可以根据使用场景，选择适合的接口。

**上传接口**

|接口名 | 说明
|:-------|:-------
|client.put_object|简单上传, 最大支持5GiB</br>支持CRC64数据校验(默认启用)</br>支持进度条</br>请求body类型为io.Reader, 当支持io.Seeker类型时，具备失败重传
|client.put_object_from_file|与client.put_object接口能力一致</br>请求body数据来源于文件路径
|分片上传接口</br>client.initiate_multipart_upload</br>client.upload_part</br>client.complete_multipart_upload|分片上传，单个分片最大5GiB，文件最大48.8TiB</br>upload_part接口支持CRC64校验(默认启用)</br>upload_part接口支持进度条</br>upload_part请求body类型为BodyType，同时支持 str, bytes, Iterable[bytes], IO[str], IO[bytes]
|Uploader.upload_from|封装了简单上传 和 分片上传接口，最大支持48.8TiB</br>支持CRC64数据校验(默认启用)</br>支持进度条</br>请求body参数类型为IO[bytes]
|Uploader.upload_file|与Uploader.UploadFrom接口能力一致</br>请求body数据来源于文件路径</br>支持断点续传
|client.append_object|追加上传, 最终文件最大支持5GiB</br>支持CRC64数据校验(默认启用)</br>支持进度条</br>请求body类型为BodyType，具备失败重传(该接口为非幂等接口，重传时可能出现失败)
|AppendOnlyFile接口</br>AppendOnlyFile.write</br>AppendOnlyFile.write_from|与client.append_object接口能力一致</br>优化了重传时失败后容错处理

**下载接口**

|接口名| 说明
|:-------|:-------
|client.get_object|流式下载, 响应体为StreamBody类型</br>不直接支持CRC64校验</br>不直接支持进度条</br>流式读数据阶段，不支持失败重连
|client.get_object_to_file|下载到本地文件</br>单连接下载</br>支持CRC64数据校验(默认启用)</br>支持进度条</br>支持失败重连
|Downloader.download_file&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|采用分片方式下载到本地文件</br>支持自定义分片大小和并发数</br>支持CRC64数据校验(默认启用)</br>支持进度条</br>支持失败重连</br>支持断点续传</br>先写临时文件，再重命名(可配置，默认启用)
|ReadOnlyFile接口</br>ReadOnlyFile.read</br>ReadOnlyFile.seek</br>ReadOnlyFile.close|File-Like形式接口, 提供read, seek 和 close接口</br>具备Seek能力</br>支持单流模式(默认)</br>支持异步预取模式，提升读的速度</br>支持自定义预取块和预取数</br>不直接支持CRC64校验</br>不直接支持进度条</br>支持失败重连


# 场景示例

本部分将从使用场景出发, 介绍如何使用SDK。

包含的主题
* [设置进度条](#设置进度条)
* [数据校验](#数据校验)

## 设置进度条

在对象的上传，下载 和 拷贝 场景下，您可以设置进度条，用于查看对象的传输状态。

**支持设置进度条的请求参数**

|支持的请求参数| 用法
|:-------|:-------
|PutObjectRequest|PutObjectRequest.progress_fn
|GetObjectRequest|GetObjectRequest.progress_fn
|CopyObjectRequest|CopyObjectRequest.progress_fn
|AppendObjectRequest|AppendObjectRequest.progress_fn
|UploadPartRequest|UploadPartRequest.progress_fn


示例

1. 上传时，设置进度条，以put_object_from_file 为例

```
...
client = oss.Client(cfg)

global progress_save_n
progress_save_n = 0
def _progress_fn(n, _written, total):
    global progress_save_n
    progress_save_n += n
    rate = int(100 * (float(_written) / float(total)))
    print('\r{0}% '.format(rate))

result = client.put_object_from_file(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
    progress_fn=_progress_fn,
), "/local/dir/example")

print(vars(result))
```

2. 下载时，设置进度条，以get_object_to_file为例
```
...
client = oss.Client(cfg)

global progress_save_n
progress_save_n = 0
def _progress_fn(n, _written, total):
    global progress_save_n
    progress_save_n += n
    rate = int(100 * (float(_written) / float(total)))
    print('\r{0}% '.format(rate))

result = client.get_object_to_file(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
    progress_fn=_progress_fn,
), "/local/dir/example")

print(vars(result))
```

3. 流式下载时，设置进度条，以GetObject 为例
```
...
client = oss.Client(cfg)

result = client.get_object(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
))

total_size = result.content_length

progress_save_n = 0
for d in result.body.iter_bytes():
    progress_save_n += len(d)
    rate = int(100 * (float(progress_save_n) / float(total_size)))
    print('\r{0}% '.format(rate))

print(vars(result))
```

## 数据校验

OSS提供基于MD5和CRC64的数据校验，确保请求的过程中的数据完整性。

## MD5校验

当向OSS发送请求时，如果设置了Content-MD5，OSS会根据接收的内容计算MD5。当OSS计算的MD5值和上传提供的MD5值不一致时，则返回InvalidDigest异常，从而保证数据的完整性。

基础接口里，除了 put_object, append_object, upload_part 接口外，会自动计算MD5, 并设置Content-MD5, 保证请求的完整性。

如果您需要在 put_object, append_object, upload_part 接口里使用MD5校验，可以参考以下写法

```
...
client = oss.Client(cfg)

data = "name,school,company,age\nLora Francis,School,Staples Inc,27\n#Lora Francis,School,Staples Inc,27\nEleanor Little,School,\"Conectiv, Inc\",43\nRosie Hughes,School,Western Gas Resources Inc,44\nLawrence Ross,School,MetLife Inc.,24\n"

h = hashlib.md5()
h.update(data.encode())
md5 = base64.b64encode(h.digest()).decode()
print(f'md5: {md5}')

result = client.put_object(oss.PutObjectRequest(
    bucket="example_bucket",
    key="example_key",
    content_md5=md5,
    body=data,
))
print(vars(result))
```

## CRC64校验

上传对象时，默认开启CRC64数据校验，以确保数据的完整性，例如 put_object, append_object, upload_part 等接口。

下载对象时，
* 如果是下载到本地文件，默认开启CRC64数据校验，以确保数据的完整性，例如 Downloader.download_file 和 get_object_to_file 接口。
* 如果是流式读类型的接口，不会做CRC64校验，例如 get_object 和 ReadOnlyFile.read 接口。

如果您需要在流式读接口里使用CRC64校验，可以参考以下写法

```
...
client = oss.Client(cfg)

result = client.get_object(oss.GetObjectRequest(
    bucket="example_bucket",
    key="example_key",
))

# 响应头返回的是整个文件的CRC64值，如果是范围下载，不支持CRC64校验.status_code为206表示是范围下载
if result.status_code == 200:
    crc64_a = crc.Crc64(0)
    crc64_a.update(result.body.read())
    ccrc = str(crc64_a.sum64())

    scrc = result.hash_crc64

    if scrc != ccrc:
        raise oss.exceptions.InconsistentError(
            client_crc=ccrc,
            server_crc=scrc
        )

print(vars(result))
```

如果您需要关闭CRC64校验，通过Config.disable_download_crc64_check 和  Config.disable_upload_crc64_check 配置，例如
```
cfg = oss.config.load_default()

cfg.disable_download_crc64_check = True
cfg.disable_upload_crc64_check = True

client = oss.Client(cfg)
```

# 迁移指南

本部分介绍如何从V1 版本([aliyun-oss-python-sdk](https://github.com/aliyun/aliyun-oss-python-sdk)) 迁移到 V2 版本。

## 最低 python 版本

V2 版本 要求 python 版本最低为 3.8。

## 导入路径

V2 版本使用新的代码仓库，同时也对代码结构进行了调整，按照功能模块组织，以下是这些模块路径和说明：

| 模块路径                                                                                               | 说明 
|:------------------------------|:-------
| alibabacloud_oss_v2        |SDK核心，接口 和 高级接口实现
| alibabacloud_oss_v2.credentials   |访问凭证相关
| alibabacloud_oss_v2.retry     |重试相关
| alibabacloud_oss_v2.signer    |签名相关
| alibabacloud_oss_v2.transport |HTTP客户端相关
| alibabacloud_oss_v2.crypto    |客户端加密相关

示例 

```
// v1 
import oss2
```

```
// v2 
import alibabacloud_oss_v2
```

## 配置加载

V2 版本简化了配置设置方式，全部迁移到 [config](alibabacloud_oss_v2/config.py) 下，可以以编程方式覆盖缺省配置。

V2 默认使用 V4签名，所以必须配置区域（Region）。

V2 支持从区域（Region）信息构造 访问域名(Endpoint), 当访问的是公有云时，可以不设置Endpoint。

示例

```
// v1

from oss2 import http
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

# 环境变量中获取访问凭证
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
endpoint = "https://oss-cn-hangzhou.aliyuncs.com"

# 设置区域
region = "cn-hangzhou"

# 设置HTTP连接超时时间为20秒, HTTP读取或写入超时时间为60秒
bucket = oss2.Bucket(auth, endpoint, "example_bucket", region=region, connect_timeout=(20, 60))

# # 不校验SSL证书校验
# session = http.Session()
# session.session.verify = False
# bucket = oss2.Bucket(auth, endpoint, "example_bucket", region=region, session=session)

```

```
// v2

import alibabacloud_oss_v2 as oss

# 环境变量中获取访问凭证
credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider

# 设置HTTP连接超时时间为20秒
cfg.connect_timeout = 20
# HTTP读取或写入超时时间为60秒
cfg.readwrite_timeout = 60
# 不校验SSL证书校验
cfg.insecure_skip_verify = True
# 设置区域
cfg.region = "cn-hangzhou"

client = oss.Client(cfg)
```

## 创建Client

V2 版本 把 Client 的创建 函数 从 Bucket 修改 为 Client

示例

```
// v1
bucket = oss2.Bucket(auth, endpoint, 'examplebucket', region=region) 
```

```
// v2
client = oss.Client(cfg)
```

## 调用API操作

基础 API 接口 都 合并为 单一操作方法 '\<OperationName\>'，操作的请求参数为 '\<OperationName\>Request'，操作的返回值为 '\<OperationName\>Result'。这些操作方法都 迁移到 Client下。如下格式：

```
def <OperationName>(self, request: models.<OperationName>Request, **kwargs) -> models.<OperationName>Result:
```

关于API接口的详细使用说明，请参考[基础接口](#基础接口)。

示例

```
// v1
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

endpoint = "https://oss-cn-hangzhou.aliyuncs.com"
region = "cn-hangzhou"
bucket = oss2.Bucket(auth, endpoint, "example_bucket", region=region)

result = bucket.put_object('exampleobject.txt', 'example data')
```

```
// v2
import alibabacloud_oss_v2 as oss

credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
cfg = oss.config.load_default()
cfg.region = "cn-hangzhou"
cfg.credentials_provider = credentials_provider

client = oss.Client(cfg)
result = client.put_object(oss.PutObjectRequest(
        bucket="example_bucket",
        key="exampleobject.txt",
        body="example data",
    ))
```

## 预签名

V2 版本 把 预签名接口 名字从 sign_url 修改为 presign，同时把 接口 迁移到 Client 下。接口形式如下：

```
def presign(self, request: PresignRequest, **kwargs) -> PresignResult:
```

对于 request 参数，其类型 与 API 接口中的 '\<OperationName\>Request' 一致。

对于返回结果，除了返回 预签名 URL 外，还返回 HTTP 方法，过期时间 和 被签名的请求头，如下：
```
class PresignResult:
    def __init__(
        self,
        method: Optional[str] = None,
        url: Optional[str] = None,
        expiration: Optional[datetime.datetime] = None,
        signed_headers: Optional[MutableMapping] = None,
    ) -> None:
        self.method = method
        self.url = url
        self.expiration = expiration
        self.signed_headers = signed_headers
```

关于预签名的详细使用说明，请参考[预签名接口](#预签名接口)。

以 生成下载对象的预签名URL 为例，如何从 V1 迁移到 V2

```
// v1
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

endpoint = "https://oss-cn-hangzhou.aliyuncs.com"
region = "cn-hangzhou"
bucket = oss2.Bucket(auth, endpoint, "example_bucket", region=region)

object_name = "exampleobject.txt"

url = bucket.sign_url("GET", object_name, 60, slash_safe=True)
print('预签名URL的地址为：', url)   
```

```
// v2
import datetime
from typing import Dict, Any
import requests
import alibabacloud_oss_v2 as oss

credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = "cn-hangzhou"

client = oss.Client(cfg)

kwargs: Dict[str, Any] = {}
kwargs["expires"] = datetime.timedelta(minutes=10)

pre_result = client.presign(oss.GetObjectRequest(
    bucket="example_bucket",
    key="exampleobject.txt",
), **kwargs)

print(f'url: {pre_result.url}')
```

## 断点续传接口

V2 版本使用 传输管理器 'Uploader'，'Downloader' 和 'Copier' 分别 管理 对象的 上传，下载 和 拷贝。 同时移除了原有的 断点续传接口 bucket.put_object_from_file，bucket.get_object_to_file 和 bucket.copy_object。

接口对比如下：

|场景|v2|v1
|:-------|:-------|:-------
|上传文件|Uploader.upload_file|bucket.put_object_from_file
|上传流|Uploader.upload_from|不支持
|下载到文件|Downloader.download_file|bucket.get_object_to_file
|拷贝对象|Copier.copy|bucket.copy_object

默认参数的变化

|场景|v2|v1
|:-------|:-------|:-------
|上传-分片默认值|6 MiB|通过参数设置
|上传-并发默认值|3|1
|上传-阈值|分片大小|无
|上传-记录checkpoint|支持|支持
|下载-分片默认值|6 MiB|通过参数设置
|下载-并发默认值|3|1
|下载-阈值|分片大小|无
|下载-记录checkpoint|支持|支持
|拷贝-分片默认值|64 MiB|无
|拷贝-并发默认值|3|1
|拷贝-阈值|200 MiB|无
|拷贝-记录checkpoint|不支持|支持

阈值(上传/下载拷贝) 表示 对象/文件 大小 大于该值时，使用分片方式(上传/下载/拷贝)。

关于传输管理器的详细使用说明，请参考[传输管理器](#传输管理器)。

## 客户端加密

V2 版本 使用 EncryptionClient 来提供 客户端加密功能，同时也对API 接口做了精简，采用了 和 Client 一样的接口命名规则 和 调用方式。

另外，该版本 仅保留 基于 RSA 自主管理的主密钥 的参考实现。

对于 KSM 的实现，可以参考[sample/encryption_kms.py](sample/encryption_kms.py)。

关于客户端加密的详细使用说明，请参考[客户端加密](#客户端加密)。

以 使用主密钥RSA 上传对象为例，如何从 V1 迁移到 V2

```
// v1
import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from oss2.crypto import RsaProvider

auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

key_pair = {'private_key': 'yourPrivateKey', 'public_key': 'yourPublicKey'}

endpoint = "https://oss-cn-hangzhou.aliyuncs.com"

region = "cn-hangzhou"

bucket = oss2.CryptoBucket(auth, endpoint, 'example_bucket',
                           crypto_provider=RsaProvider(key_pair), region=region)

bucket.put_object('exampleobject.txt', 'example data')
```

```
// v2
import argparse
import alibabacloud_oss_v2 as oss

credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = "cn-hangzhou"

client = oss.Client(cfg)

mc = oss.crypto.MasterRsaCipher(
    mat_desc={"desc": "your master encrypt key material describe information"},
    public_key="yourRsaPublicKey",
    private_key="yourRsaPrivateKey"
)
encryption_client = oss.EncryptionClient(client, mc)

data = b'example data'

result = encryption_client.put_object(oss.PutObjectRequest(
    bucket="example_bucket",
    key="exampleobject.txt",
    body=data,
))
```

## 重试

V2 版本 默认开启对HTTP请求的重试行为。从 V1 版本迁移到 V2 时，您需要移除原有的重试代码，避免放大重试次数。

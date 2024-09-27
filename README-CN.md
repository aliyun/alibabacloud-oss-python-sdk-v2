# Alibaba Cloud OSS SDK for Python v2

[![GitHub version](https://badge.fury.io/gh/aliyun%2Falibabacloud-oss-python-sdk-v2.svg)](https://badge.fury.io/gh/aliyun%2Falibabacloud-oss-python-sdk-v2)

alibabacloud-oss-python-sdk-v2 是OSS在Python编译语言下的第二版SDK, 处于开发预览版状态

## [README in English](README-CN.md)

## 关于
> - 此Python SDK基于[阿里云对象存储服务](http://www.aliyun.com/product/oss/)官方API构建。
> - 阿里云对象存储（Object Storage Service，简称OSS），是阿里云对外提供的海量，安全，低成本，高可靠的云存储服务。
> - OSS适合存放任意文件类型，适合各种网站、开发企业及开发者使用。
> - 使用此SDK，用户可以方便地在任何应用、任何时间、任何地点上传，下载和管理数据。

## 运行环境
> - Python 3.8 及以上。

## 安装方法
### 通过 pip 安装预发布版本
```bash
$ pip install --pre alibabacloud-oss-v2
```

### 通过解压后的安装程序包安装
```bash
$ sudo python setup.py install
```

## 快速使用
#### 获取存储空间列表（List Bucket）
```python
import alibabacloud_oss_v2 as oss

def main():

    region = "cn-hangzhou"

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = region

    client = oss.Client(cfg)

    # Create the Paginator for the ListBuckets operation
    paginator = client.list_buckets_paginator()

    # Iterate through the bucket pages
    for page in paginator.iter_page(oss.ListBucketsRequest(
        )
    ):
        for o in page.buckets:
            print(f'Bucket: {o.name}, {o.location}, {o.creation_date} {o.resource_group_id}')

if __name__ == "__main__":
    main()

```

#### 获取文件列表（List Objects）
```python
import alibabacloud_oss_v2 as oss

def main():

    region = "cn-hangzhou"
    bucket_name = "your bucket name"
    
    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = region

    client = oss.Client(cfg)

    # Create the Paginator for the ListObjectsV2 operation
    paginator = client.list_objects_v2_paginator()

    # Iterate through the object pages
    for page in paginator.iter_page(oss.ListObjectsV2Request(
            bucket=bucket_name
        )
    ):
        for o in page.contents:
            print(f'Object: {o.key}, {o.size}, {o.last_modified}')

if __name__ == "__main__":
    main()

```

#### 上传文件（Put Object）
```python
import alibabacloud_oss_v2 as oss

def main():

    region = "cn-hangzhou"
    bucket_name = "your bucket name"
    object_name = "your object name"
    local_file  = "your local file path"

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = region


    client = oss.Client(cfg)

    with open(local_file, 'rb') as f:
        result = client.put_object(oss.PutObjectRequest(
            bucket=bucket_name,
            key=object_name,
            body=f,
        ))

    print(f'put object sucessfully, ETag {result.etag}')


if __name__ == "__main__":
    main()

```

## 更多示例
请参看`sample`目录

### 运行示例
> - 进入示例程序目录 `sample`。
> - 通过环境变量，配置访问凭证, `export OSS_ACCESS_KEY_ID="your access key id"`, `export OSS_ACCESS_KEY_SECRET="your access key secrect"`。
> - 以 list_buckets.go 为例，执行 `python list_buckets.python --region cn-hangzhou`。

## 资源
[开发者指南](DEVGUIDE-CN.md) - 参阅该指南，来帮助您安装、配置和使用该开发套件。

## 许可协议
> - Apache-2.0, 请参阅 [许可文件](LICENSE)

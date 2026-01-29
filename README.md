# Alibaba Cloud OSS SDK for Python v2

[![GitHub version](https://badge.fury.io/gh/aliyun%2Falibabacloud-oss-python-sdk-v2.svg)](https://badge.fury.io/gh/aliyun%2Falibabacloud-oss-python-sdk-v2)

alibabacloud-oss-python-sdk-v2 is the v2 of the OSS SDK for the Python programming language

## [README in Chinese](README-CN.md)

## About
> - This Python SDK is based on the official APIs of [Alibaba Cloud OSS](http://www.aliyun.com/product/oss/).
> - Alibaba Cloud Object Storage Service (OSS) is a cloud storage service provided by Alibaba Cloud, featuring massive capacity, security, a low cost, and high reliability. 
> - The OSS can store any type of files and therefore applies to various websites, development enterprises and developers.
> - With this SDK, you can upload, download and manage data on any app anytime and anywhere conveniently. 

## Running Environment
> - Python 3.8 or above. 

## Installing
### Install the beta version through pip
```bash
$ pip install alibabacloud-oss-v2
```

### Install from the unzipped installer package directly
```bash
$ sudo python setup.py install
```

## Getting Started
#### List Bucket
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

#### List Objects
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

#### Put Object
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

    print(f'put object successfully, ETag {result.etag}')


if __name__ == "__main__":
    main()

```

##  Complete Example
More example projects can be found in the `sample` folder 

### Running Example
> - Go to the sample code folder `sample`。
> - Configure credentials values from the environment variables, like `export OSS_ACCESS_KEY_ID="your access key id"`, `export OSS_ACCESS_KEY_SECRET="your access key secrect"`
> - Take `list_buckets.py` as an example，run `python list_buckets.py --region cn-hangzhou` command。

## Resources
[Developer Guide](DEVGUIDE-CN.md) - Use this document to learn how to get started and use this sdk.

## License
> - Apache-2.0, see [license file](LICENSE)

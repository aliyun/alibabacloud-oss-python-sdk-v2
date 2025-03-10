# ChangeLog - Alibaba Cloud OSS SDK for Python v2

## 版本号：1.1.0 日期：2025-03-10
### 变更内容
- Feature：Add clean restored object api
- Feature：Add operation level read-write timeout
- Feature：Add operation level total timeout
- Feature：Add copier
- Fix：The issue that callback result can not be obtained
- Update：Change the type of body parameter of some api

## 版本号：1.0.2b0 日期：2025-01-03
### 变更内容
- Feature：Add bucket worm api
- Feature：Add bucket request payment api
- Feature：Add bucket style api
- Feature：Add bucket resource group api
- Feature：Add public access block api
- Feature：Add bucket access block api
- Feature：Add access point public access block api
- Feature：Add bucket transfer acceleration apiq
- Feature：Add bucket data redundancy transition api
- Feature：Add bucket tags api
- Feature：Add meta query api
- Feature：Add bucket https config api
- Fix：Uploader can not abort upload task
- Break Change: rename sse_kms_key_id to server_side_encryption_key_id

## 版本号：1.0.1.dev2 日期：2024-12-26
### 变更内容
- Feature：Downloader supports progress

## 版本号：1.0.1.dev1 日期：2024-12-19
### 变更内容
- Update：Change requires
- Update：Avoid adding accept-encoding: gzip, deflate' by default.

## 版本号：1.0.1.dev0 日期：2024-12-03
### 变更内容
- Feature：Add access point api
- Feature：Add bucket access monitor api
- Feature：Add bucket archive direct read api
- Feature：Add bucket cname api
- Feature：Add bucket cors api
- Feature：Add bucket encryption api
- Feature：Add bucket logging api
- Feature：Add bucket lifecycle api
- Feature：Add bucket policy api
- Feature：Add bucket inventory api
- Feature：Add bucket referer api
- Feature：Add bucket replication api
- Feature：Add bucket website api

## 版本号：1.0.0.dev1 日期：2024-10-11
### 变更内容
- Update：Remove unnecessary log prints

## 版本号：1.0.0.dev 日期：2024-09-26
### 变更内容
- Feature：Add credentials provider
- Feature：Add retryer
- Feature：Add signer v1 and signer v4
- Feature：Add httpclient
- Feature：Add bucket's basic, bucket acl, bucket versioning api
- Feature：Add object's api
- Feature：Add region's api
- Feature：Add service's api
- Feature：Add presigner
- Feature：Add paginator
- Feature：Add uploader and downloader
- Feature：Add file-like api
- Feature：Add encryption client
- Feature：Add is_object_exist/is_bucket_exist api
- Feature：Add put_object_from_file/get_object_to_file api

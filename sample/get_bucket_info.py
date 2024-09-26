import sys
import os

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket info sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')


def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss.Client(cfg)

    result = client.get_bucket_info(oss.GetBucketInfoRequest(
        bucket=args.bucket,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' name: {result.bucket_info.name},' 
          f' access monitor: {result.bucket_info.access_monitor},' 
          f' location: {result.bucket_info.location},' 
          f' creation date: {result.bucket_info.creation_date},' 
          f' extranet endpoint: {result.bucket_info.extranet_endpoint},' 
          f' intranet endpoint: {result.bucket_info.intranet_endpoint},' 
          f' acl: {result.bucket_info.acl},' 
          f' data redundancy type: {result.bucket_info.data_redundancy_type},' 
          f' id: {result.bucket_info.owner.id},' 
          f' display name: {result.bucket_info.owner.display_name},' 
          f' storage class: {result.bucket_info.storage_class},' 
          f' resource group id: {result.bucket_info.resource_group_id},' 
          f' kms master key id: {result.bucket_info.sse_rule.kms_master_key_id},' 
          f' sse algorithm: {result.bucket_info.sse_rule.sse_algorithm},' 
          f' kms data encryption: {result.bucket_info.sse_rule.kms_data_encryption},' 
          f' versioning: {result.bucket_info.versioning},' 
          f' transfer acceleration: {result.bucket_info.transfer_acceleration},' 
          f' cross region replication: {result.bucket_info.cross_region_replication},' 
          f' log bucket: {result.bucket_info.bucket_policy.log_bucket},' 
          f' log prefix: {result.bucket_info.bucket_policy.log_prefix},' 
          f' comment: {result.bucket_info.comment},' 
          f' block public access: {result.bucket_info.block_public_access},'
    )

if __name__ == "__main__":
    main()
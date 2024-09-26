import sys
import os

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket stat sample")
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

    result = client.get_bucket_stat(oss.GetBucketStatRequest(
        bucket=args.bucket,
    ))
    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' storage: {result.storage},' 
          f' object count: {result.object_count},' 
          f' multi part upload count: {result.multi_part_upload_count},' 
          f' live channel count: {result.live_channel_count},' 
          f' last modified time: {result.last_modified_time},' 
          f' standard storage: {result.standard_storage},' 
          f' standard object count: {result.standard_object_count},' 
          f' infrequent access storage: {result.infrequent_access_storage},' 
          f' infrequent access real storage: {result.infrequent_access_real_storage},' 
          f' infrequent access object count: {result.infrequent_access_object_count},' 
          f' archive storage: {result.archive_storage},' 
          f' archive real storage: {result.archive_real_storage},' 
          f' archive object count: {result.archive_object_count},' 
          f' cold archive storage: {result.cold_archive_storage},' 
          f' cold archive real storage: {result.cold_archive_real_storage},' 
          f' cold archive object count: {result.cold_archive_object_count},' 
          f' deep cold archive storage: {result.deep_cold_archive_storage},' 
          f' deep cold archive real storage: {result.deep_cold_archive_real_storage},' 
          f' deep cold archive object count: {result.deep_cold_archive_object_count},' 
          f' delete marker count: {result.delete_marker_count},'
    )

if __name__ == "__main__":
    main()



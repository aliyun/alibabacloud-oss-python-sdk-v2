import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="get bucket lifecycle sample")
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

    result = client.get_bucket_lifecycle(oss.GetBucketLifecycleRequest(
            bucket=args.bucket,
    ))


    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            # f' key: {result.lifecycle_configuration.rules[0].tags[0].key},'
            # f' value: {result.lifecycle_configuration.rules[0].tags[0].value},'
            # f' noncurrent days: {result.lifecycle_configuration.rules[0].noncurrent_version_expiration.noncurrent_days},'
            # f' object size greater than: {result.lifecycle_configuration.rules[0].filter.object_size_greater_than},'
            # f' object size less than: {result.lifecycle_configuration.rules[0].filter.object_size_less_than},'
            # f' prefix: {result.lifecycle_configuration.rules[0].filter.filter_not[0].prefix},'
            # f' key: {result.lifecycle_configuration.rules[0].filter.filter_not[0].tag.key},'
            # f' value: {result.lifecycle_configuration.rules[0].filter.filter_not[0].tag.value},'
            # f' id: {result.lifecycle_configuration.rules[0].id},'
            # f' created before date: {result.lifecycle_configuration.rules[0].expiration.created_before_date},'
            # f' days: {result.lifecycle_configuration.rules[0].expiration.days},'
            # f' expired object delete marker: {result.lifecycle_configuration.rules[0].expiration.expired_object_delete_marker},'
            # f' created before date: {result.lifecycle_configuration.rules[0].transitions[0].created_before_date},'
            # f' days: {result.lifecycle_configuration.rules[0].transitions[0].days},'
            # f' is access time: {result.lifecycle_configuration.rules[0].transitions[0].is_access_time},'
            # f' return to std when visit: {result.lifecycle_configuration.rules[0].transitions[0].return_to_std_when_visit},'
            # f' allow small file: {result.lifecycle_configuration.rules[0].transitions[0].allow_small_file},'
            # f' is access time: {result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].is_access_time},'
            # f' return to std when visit: {result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].return_to_std_when_visit},'
            # f' allow small file: {result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].allow_small_file},'
            # f' noncurrent days: {result.lifecycle_configuration.rules[0].noncurrent_version_transitions[0].noncurrent_days},'
            # f' atime base: {result.lifecycle_configuration.rules[0].atime_base},'
            # f' prefix: {result.lifecycle_configuration.rules[0].prefix},'
            # f' status: {result.lifecycle_configuration.rules[0].status},'
            # f' days: {result.lifecycle_configuration.rules[0].abort_multipart_upload.days},'
            # f' created before date: {result.lifecycle_configuration.rules[0].abort_multipart_upload.created_before_date},'
    )

    if result.lifecycle_configuration.rules:
        for r in result.lifecycle_configuration.rules:
            print(f'rule: {r}')


if __name__ == "__main__":
    main()
import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="delete multiple objects sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)


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

    # If deleting multiple items, please follow the following format (deprecated)
    # objects = [oss.DeleteObject(key=args.key), oss.DeleteObject(key=args.key2)],
    # result = client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
    #     bucket=args.bucket,
    #     encoding_type='url',
    #     objects=[oss.DeleteObject(key=args.key)],
    # ))

    # New mode using Delete parameter
    delete_request = oss.Delete(
        objects=[
            oss.ObjectIdentifier(key=args.key)
        ],
        quiet=False
    )
    
    result = client.delete_multiple_objects(oss.DeleteMultipleObjectsRequest(
        bucket=args.bucket,
        delete=delete_request,
    ))
    
    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' key: {result.deleted_objects[0].key},' 
          f' version id: {result.deleted_objects[0].version_id},' 
          f' delete marker: {result.deleted_objects[0].delete_marker},' 
          f' delete marker version id: {result.deleted_objects[0].delete_marker_version_id},' 
          f' encoding type: {result.encoding_type},'
    )


if __name__ == "__main__":
    main()
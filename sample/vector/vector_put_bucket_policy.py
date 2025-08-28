import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector put bucket policy sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--uid', help='The user id.', required=True)

def main():
    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.user_id = args.uid
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    vector_client = oss_vectors.Client(cfg)


    policy_content = '''
        {
           "Version":"1",
           "Statement":[
               {
                 "Action":[
                   "ossvector:PutVectors",
                   "ossvector:GetVectors"
                ],
                "Effect":"Deny",
                "Principal":["1234567890"],
                "Resource":["acs:ossvector:cn-hangzhou:1234567890:*"]
               }
            ]
         }
    '''

    result = vector_client.put_bucket_policy(oss_vectors.models.PutBucketPolicyRequest(
        bucket=args.bucket,
        body=policy_content
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()

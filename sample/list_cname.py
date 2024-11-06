import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="list cname sample")
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

    result = client.list_cname(oss.ListCnameRequest(
            bucket=args.bucket,
    ))


    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            # f' domain: {result.cnames[0].domain},'
            # f' last modified: {result.cnames[0].last_modified},'
            # f' status: {result.cnames[0].status},'
            # f' fingerprint: {result.cnames[0].certificate.fingerprint},'
            # f' valid start date: {result.cnames[0].certificate.valid_start_date},'
            # f' valid end date: {result.cnames[0].certificate.valid_end_date},'
            # f' type: {result.cnames[0].certificate.type},'
            # f' cert id: {result.cnames[0].certificate.cert_id},'
            # f' status: {result.cnames[0].certificate.status},'
            # f' creation date: {result.cnames[0].certificate.creation_date},'
            f' bucket: {result.bucket},'
            f' owner: {result.owner},'
    )

    if result.cnames:
        for r in result.cnames:
            print(f'result: {r.domain}, {r.last_modified}, {r.status}, {r.certificate}')

if __name__ == "__main__":
    main()
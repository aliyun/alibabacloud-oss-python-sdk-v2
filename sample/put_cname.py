import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="put cname sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--domain', help='The custom domain name.', required=True)


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

    cert_id='493****-cn-hangzhou'
    certificate='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----'
    private_key='-----BEGIN CERTIFICATE----- MIIDhDCCAmwCCQCFs8ixARsyrDANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMC **** -----END CERTIFICATE-----'
    previous_cert_id='493****-cn-hangzhou'
    force = True

    result = client.put_cname(oss.PutCnameRequest(
            bucket=args.bucket,
            bucket_cname_configuration=oss.BucketCnameConfiguration(
                cname=oss.Cname(
                    domain=args.domain,
                    certificate_configuration=oss.CertificateConfiguration(
                        certificate=certificate,
                        private_key=private_key,
                        previous_cert_id=previous_cert_id,
                        force=force,
                        cert_id=cert_id,
                    ),
                ),
            ),
    ))

    # # Do you want to delete the certificate
    # result = client.put_cname(oss.PutCnameRequest(
    #         bucket=args.bucket,
    #         bucket_cname_configuration=oss.BucketCnameConfiguration(
    #             cname=oss.Cname(
    #                 domain=args.domain,
    #                 certificate_configuration=oss.CertificateConfiguration(
    #                     delete_certificate=True,
    #                 ),
    #             ),
    #         ),
    # ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()
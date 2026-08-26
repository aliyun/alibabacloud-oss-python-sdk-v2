import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="put data pipeline configuration sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--data-pipeline-name', help='The name of the data pipeline.', required=True)
parser.add_argument('--bucket', help='The input bucket name.', required=True)
parser.add_argument('--role', help='The role for the data pipeline.')
parser.add_argument('--description', help='The description of the data pipeline.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    configuration = oss_dataprocess.models.PutDataPipelineConfigurationConfiguration(
        data_pipeline_description=args.description,
        sources=[oss_dataprocess.models.DataPipelineSource(
            input_bucket=args.bucket,
            input_data_scope='All',
        )],
    )

    result = client.put_data_pipeline_configuration(oss_dataprocess.models.PutDataPipelineConfigurationRequest(
        data_pipeline_name=args.data_pipeline_name,
        role=args.role,
        configuration=configuration,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')

if __name__ == "__main__":
    main()

import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="delete data pipeline configuration sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--data-pipeline-name', help='The name of the data pipeline.', required=True)

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.delete_data_pipeline_configuration(oss_dataprocess.models.DeleteDataPipelineConfigurationRequest(
        data_pipeline_name=args.data_pipeline_name,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')

if __name__ == "__main__":
    main()

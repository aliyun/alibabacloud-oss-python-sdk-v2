import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="get data pipeline configuration sample")
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

    result = client.get_data_pipeline_configuration(oss_dataprocess.models.GetDataPipelineConfigurationRequest(
        data_pipeline_name=args.data_pipeline_name,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')
    if result.configuration:
        c = result.configuration
        print(f'data pipeline: name={c.data_pipeline_name}, description={c.data_pipeline_description}, status={c.status}')
        if c.sources:
            for i, s in enumerate(c.sources):
                print(f'  source {i + 1}: bucket={s.input_bucket}, scope={s.input_data_scope}')
        if c.destination:
            print(f'  destination: vector bucket={c.destination.vector_bucket_name}, key prefix={c.destination.vector_key_prefix}')

if __name__ == "__main__":
    main()

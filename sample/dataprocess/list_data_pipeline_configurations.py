import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="list data pipeline configurations sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--max-results', type=int, help='The maximum number of configurations to return.')
parser.add_argument('--prefix', help='The prefix to filter configurations.')
parser.add_argument('--next-token', help='The next token for pagination.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    result = client.list_data_pipeline_configurations(oss_dataprocess.models.ListDataPipelineConfigurationsRequest(
        max_results=args.max_results,
        prefix=args.prefix,
        next_token=args.next_token,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}, next token: {result.next_token}')
    if result.data_pipeline_configurations and result.data_pipeline_configurations.data_pipeline_configuration:
        for i, c in enumerate(result.data_pipeline_configurations.data_pipeline_configuration):
            print(f'configuration {i + 1}: name={c.data_pipeline_name}, description={c.data_pipeline_description}, status={c.status}')

if __name__ == "__main__":
    main()

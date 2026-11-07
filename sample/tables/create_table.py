import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

parser = argparse.ArgumentParser(description="create table sample")
parser.add_argument('--region', help='The region in which the table bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS Tables.')
parser.add_argument('--table-bucket-arn', help='The ARN of the table bucket.', required=True)
parser.add_argument('--namespace', help='The namespace of the table.', required=True)
parser.add_argument('--name', help='The name of the table.', required=True)
parser.add_argument('--format', help='The format of the table.', required=True)

def main():
    args = parser.parse_args()

    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss_tables.Client(cfg)

    # Create schema fields
    schema = oss_tables.models.IcebergSchema(fields=[
        oss_tables.models.SchemaField(name="id", type="long", required=True),
        oss_tables.models.SchemaField(name="name", type="string", required=False),
        oss_tables.models.SchemaField(name="ts", type="timestamptz", required=False),
    ])

    # Create partition spec
    partition_spec = oss_tables.models.IcebergPartitionSpec(
        spec_id=0,
        fields=[
            oss_tables.models.IcebergPartitionField(
                source_id=2,
                field_id=1001,
                name="region",
                transform="identity",
            ),
        ],
    )

    # Create iceberg metadata
    iceberg_metadata = oss_tables.models.IcebergMetadata(
        schema=schema,
        partition_spec=partition_spec,
    )

    # Optional: uncomment the code below to replace iceberg_metadata above with schemaV2.
    # Do not use schema and schemaV2 together; this example omits the legacy partition_spec.
    # iceberg_metadata = oss_tables.models.IcebergMetadata(
    #     schema_v2={
    #         "type": "struct",
    #         "schema-id": 0,
    #         "identifier-field-ids": [10],
    #         "fields": [
    #             {"id": 10, "name": "order_id", "type": "long", "required": True, "doc": "Order ID"},
    #             {
    #                 "id": 20, "name": "customer", "required": False,
    #                 "type": {"type": "struct", "fields": [
    #                     {"id": 21, "name": "name", "type": "string", "required": False},
    #                     {"id": 22, "name": "level", "type": "int", "required": False},
    #                 ]},
    #             },
    #             {
    #                 "id": 30, "name": "tags", "required": False,
    #                 "type": {"type": "list", "element-id": 31,
    #                          "element": "string", "element-required": False},
    #             },
    #             {
    #                 "id": 40, "name": "attributes", "required": False,
    #                 "type": {"type": "map", "key-id": 41, "key": "string",
    #                          "value-id": 42, "value": "string", "value-required": False},
    #             },
    #         ],
    #     },
    #     properties={"format-version": "2"},
    # )

    # Set metadata
    metadata = oss_tables.models.TableMetadata(iceberg=iceberg_metadata)

    # Add encryption configuration
    encryption_configuration = oss_tables.models.EncryptionConfiguration(
        sse_algorithm="AES256",
    )

    result = client.create_table(oss_tables.models.CreateTableRequest(
        table_bucket_arn=args.table_bucket_arn,
        namespace=args.namespace,
        name=args.name,
        format=args.format,
        metadata=metadata,
        encryption_configuration=encryption_configuration,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' table arn: {result.table_arn},'
          f' version token: {result.version_token}')


if __name__ == "__main__":
    main()

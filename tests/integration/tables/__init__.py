# -*- coding: utf-8 -*-
"""Tables integration tests."""

import os
from .. import TestIntegration, get_default_client, random_short_bucket_name

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.tables as oss_tables

ACCESS_ID = os.getenv("OSS_TEST_ACCESS_KEY_ID")
ACCESS_KEY = os.getenv("OSS_TEST_ACCESS_KEY_SECRET")
REGION = os.getenv("OSS_TEST_REGION", "cn-hangzhou")
TABLES_ENDPOINT = os.getenv("OSS_TEST_TABLES_ENDPOINT")


def get_tables_client() -> oss_tables.Client:
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = TABLES_ENDPOINT
    return oss_tables.Client(cfg)


class TestIntegrationTables(TestIntegration):

    @classmethod
    def setUpClass(cls):
        TestIntegration.setUpClass()
        cls.tables_client = get_tables_client()

        # Create a table bucket for testing
        cls.table_bucket_name = random_short_bucket_name()
        result = cls.tables_client.create_table_bucket(
            oss_tables.models.CreateTableBucketRequest(
                name=cls.table_bucket_name,
            )
        )
        cls.table_bucket_arn = result.arn

    @classmethod
    def tearDownClass(cls):
        TestIntegration.tearDownClass()
        clean_table_buckets("python-sdk-test-bucket-")


def clean_table_buckets(prefix: str) -> None:
    tables_client = get_tables_client()

    # List and clean all table buckets with the prefix
    result = tables_client.list_table_buckets(
        oss_tables.models.ListTableBucketsRequest(prefix=prefix)
    )

    for bucket in result.table_buckets:
        clean_table_bucket_content(tables_client, bucket.arn)
        # Delete the table bucket itself
        tables_client.delete_table_bucket(
            oss_tables.models.DeleteTableBucketRequest(
                table_bucket_arn=bucket.arn
            )
        )


def clean_table_bucket_content(client: oss_tables.Client, table_bucket_arn: str) -> None:
    """
    Clean all content in the specified table bucket (including tables and namespaces)
    """
    # Clean all tables
    #clean_tables(client, table_bucket_arn)

    # Clean all namespaces
    clean_namespaces(client, table_bucket_arn)


def clean_tables(client: oss_tables.Client, table_bucket_arn: str, namespace: str) -> None:
    """
    Clean all tables in the specified table bucket
    """
    result = client.list_tables(
        oss_tables.models.ListTablesRequest(
            table_bucket_arn=table_bucket_arn,
            namespace=namespace,
        )
    )
    for table in result.tables:
        client.delete_table(
            oss_tables.models.DeleteTableRequest(
                table_bucket_arn=table_bucket_arn,
                namespace=namespace, 
                name=table.name
            )
        )


def clean_namespaces(client: oss_tables.Client, table_bucket_arn: str) -> None:
    """
    Clean all namespaces in the specified table bucket
    """
    result = client.list_namespaces(
        oss_tables.models.ListNamespacesRequest(
            table_bucket_arn=table_bucket_arn
        )
    )
    for namespace in result.namespaces:
        clean_tables(client, table_bucket_arn, namespace.namespace[0])
        client.delete_namespace(
            oss_tables.models.DeleteNamespaceRequest(
                table_bucket_arn=table_bucket_arn,
                namespace=namespace.namespace[0]
            )
        )

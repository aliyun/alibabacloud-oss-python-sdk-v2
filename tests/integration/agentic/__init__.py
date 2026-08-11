# -*- coding: utf-8 -*-
"""Agentic bucket integration tests."""

import random
import time
from .. import (
    TestIntegration,
    ACCESS_ID,
    ACCESS_KEY,
    REGION,
    ENDPOINT,
    USER_ID,
    get_default_client,
    get_invalid_ak_client,
    get_signv1_client,
)

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

AGENTIC_BUCKET_NAME_PREFIX = "oss-sdk-test-python-ab-"
BUCKETSPACE_PREFIX = "oss-sdk-test-python-bs-"


def get_agentic_client() -> oss_agentic.AgenticBucketClient:
    """Create an AgenticBucketClient for integration tests."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    cfg.account_id = USER_ID
    return oss_agentic.AgenticBucketClient(cfg)


def get_path_style_agentic_client() -> oss_agentic.AgenticBucketClient:
    """Create an AgenticBucketClient with path-style addressing for integration tests."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    cfg.account_id = USER_ID
    cfg.use_path_style = True
    return oss_agentic.AgenticBucketClient(cfg)


def get_invalid_ak_agentic_client() -> oss_agentic.AgenticBucketClient:
    """Create an AgenticBucketClient with invalid credentials for negative tests."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider('invalid-ak', 'invalid-sk')
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    cfg.account_id = USER_ID
    return oss_agentic.AgenticBucketClient(cfg)


def get_bucket_space_client() -> oss.Client:
    """Create a BucketSpaceClient for integration tests."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    cfg.account_id = USER_ID
    return oss_agentic.BucketSpaceClient.create(cfg)



def get_path_style_bucket_space_client() -> oss.Client:
    """Create a BucketSpaceClient with path-style addressing for integration tests."""
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.StaticCredentialsProvider(ACCESS_ID, ACCESS_KEY)
    cfg.region = REGION
    cfg.endpoint = ENDPOINT
    cfg.account_id = USER_ID
    cfg.use_path_style = True
    return oss_agentic.BucketSpaceClient.create(cfg)


def gen_agentic_bucket_name() -> str:
    """Generate a random agentic bucket name prefix.
    """
    return AGENTIC_BUCKET_NAME_PREFIX + str(random.randint(0, 999))


def gen_bucket_space_prefix() -> str:
    """Generate a random bucket space prefix."""
    return BUCKETSPACE_PREFIX + str(random.randint(0, 999))


def get_full_agentic_bucket_name(prefix: str) -> str:
    """Build the full agentic bucket name from a prefix.

    Mirrors the Java helper:
        agenticBucketName + "-" + accountId() + "-" + region() + "-ab-apsr"
    """
    return f'{prefix}-{USER_ID}-{REGION}-ab-apsr'


def clean_agentic_bucket(client: oss_agentic.AgenticBucketClient, bucket: str) -> None:
    """Best-effort cleanup: remove attached properties before deleting the agentic bucket."""
    try:
        print('delete_agentic_bucket_policy')
        client.delete_agentic_bucket_policy(
            oss_agentic.models.DeleteAgenticBucketPolicyRequest(bucket=bucket)
        )
    except Exception:
        pass
    try:
        print('delete_agentic_bucket_encryption')
        client.delete_agentic_bucket_encryption(
            oss_agentic.models.DeleteAgenticBucketEncryptionRequest(bucket=bucket)
        )
    except Exception:
        pass
    try:
        print('delete_agentic_bucket_public_access_block')
        client.delete_agentic_bucket_public_access_block(
            oss_agentic.models.DeleteAgenticBucketPublicAccessBlockRequest(bucket=bucket)
        )
    except Exception:
        pass
    # Disable the bucket before deletion
    try:
        print('put_agentic_bucket_status')
        client.put_agentic_bucket_status(
            oss_agentic.models.PutAgenticBucketStatusRequest(
                bucket=bucket,
                agentic_bucket_status=oss_agentic.models.AgenticBucketStatus(status='Disabled')
            )
        )
    except Exception:
        pass
    try:
        print('delete_agentic_bucket')
        client.delete_agentic_bucket(
            oss_agentic.models.DeleteAgenticBucketRequest(bucket=bucket)
        )
    except Exception as e:
        print("Failed to delete agentic bucket:", bucket, e)
        pass


def _extract_prefix(full_name: str) -> str:
    """Extract user-specified prefix from a full agentic bucket name.

    AgenticProvider appends '-{account_id}-{region}-ab-apsr' to the prefix.
    Strip that suffix to recover the original prefix for API calls.
    """
    suffix = f'-{USER_ID}-{REGION}-ab-apsr'
    if full_name.endswith(suffix):
        return full_name[:-len(suffix)]
    return full_name


def clean_agentic_buckets(prefix: str) -> None:
    """Clean all agentic buckets with the given prefix."""
    client = get_agentic_client()
    paginator = client.list_agentic_buckets_paginator()
    for page in paginator.iter_page(oss_agentic.models.ListAgenticBucketsRequest()):
        if page.agentic_buckets is not None:
            for bucket in page.agentic_buckets:
                if bucket.name is not None and bucket.name.startswith(prefix):
                    bucket_prefix = _extract_prefix(bucket.name)
                    clean_agentic_bucket(client, bucket_prefix)


class TestIntegrationAgentic(TestIntegration):
    """Base class for agentic bucket integration tests."""

    agentic_client: oss_agentic.AgenticBucketClient
    agentic_bucket_name: str
    full_agentic_bucket_name: str

    @classmethod
    def setUpClass(cls):
        # Only initialize clients, do NOT create a regular bucket
        # (sub-user lacks oss:PutBucket permission for standard buckets)
        cls.client = get_default_client()
        cls.invalid_client = get_invalid_ak_client()
        cls.signv1_client = get_signv1_client()
        cls.agentic_client = get_agentic_client()
        # Create the agentic bucket, retry on name collision
        for _ in range(5):
            cls.agentic_bucket_name = gen_agentic_bucket_name()
            cls.full_agentic_bucket_name = get_full_agentic_bucket_name(cls.agentic_bucket_name)
            try:
                cls.agentic_client.create_agentic_bucket(
                    oss_agentic.models.CreateAgenticBucketRequest(
                        bucket=cls.agentic_bucket_name,
                        create_agentic_bucket_configuration=oss_agentic.models.CreateAgenticBucketConfiguration(
                            storage_class='Standard',
                            data_redundancy_type='LRS',
                        ),
                    )
                )
                break
            except Exception as ec:
                cause = ec
                while cause is not None:
                    if isinstance(cause, oss.exceptions.ServiceError) and cause.code == 'BucketAlreadyExists':
                        break
                    cause = cause.__cause__
                else:
                    raise
        # Wait for cache expiration
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        clean_agentic_buckets(AGENTIC_BUCKET_NAME_PREFIX)

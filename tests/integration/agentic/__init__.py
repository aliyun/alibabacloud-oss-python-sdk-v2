# -*- coding: utf-8 -*-
"""Agentic bucket integration tests.

The service requires put_agentic_bucket_status(Disabled) before delete_agentic_bucket, and the
bucket only becomes deletable roughly 24 hours later. A run therefore cannot delete the buckets it
creates; it only marks them Disabled and reclaims the ones left behind by earlier runs whose
readiness window has elapsed.
"""

import os
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
    random_lowstr,
)

import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.agentic as oss_agentic

# The 'ab' / 'bs' markers are what the reaper filters on. The prefixes are kept short on purpose:
# the resolved name {bucket}-{account_id}-{region}-ab-apsr becomes a DNS host label and must stay
# within 63 characters, which leaves 23 characters for prefix plus random part
# (63 - 1 - 16 for the account id - 1 - 14 for the longest region - 8 for '-ab-apsr').
def get_agentic_bucket_name_prefix() -> str:
    val = os.getenv("OSS_TEST_BUCKET_PREFIX")
    if val:
        return val + "ab-"
    return "oss-sdk-test-ab-"


def get_bucket_space_prefix() -> str:
    val = os.getenv("OSS_TEST_BUCKET_PREFIX")
    if val:
        return val + "bs-"
    return "oss-sdk-test-bs-"


AGENTIC_BUCKET_NAME_PREFIX = get_agentic_bucket_name_prefix()
BUCKETSPACE_PREFIX = get_bucket_space_prefix()

# The tails the service appends to an agentic bucket / bucket space name.
AGENTIC_BUCKET_SUFFIX = "ab-apsr"
BUCKET_SPACE_SUFFIX = "bs-apsr"

RANDOM_NAME_LENGTH = 6
LIST_RETRY_TIMES = 10
LIST_RETRY_INTERVAL_SECONDS = 3


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

    The random part has a fixed length: names must not be prefixes of one another, otherwise the
    reaper would also match the bucket of a concurrently running job.
    """
    return AGENTIC_BUCKET_NAME_PREFIX + random_lowstr(RANDOM_NAME_LENGTH)


def gen_bucket_space_prefix() -> str:
    """Generate a random bucket space prefix."""
    return BUCKETSPACE_PREFIX + random_lowstr(RANDOM_NAME_LENGTH)


def get_full_agentic_bucket_name(prefix: str) -> str:
    """Build the full agentic bucket name from a prefix."""
    return f'{prefix}-{USER_ID}-{REGION}-{AGENTIC_BUCKET_SUFFIX}'


def to_short_name(full_name: str, suffix: str) -> str:
    """Strip the resolved tail so a listed physical name can be handed back to a client that
    re-expands short names.
    """
    tail = f'-{USER_ID}-{REGION}-{suffix}'
    if full_name.endswith(tail):
        return full_name[:-len(tail)]
    return full_name


def wait_for_agentic_bucket_listed(case, client: oss_agentic.AgenticBucketClient, bucket: str) -> bool:
    """A newly created agentic bucket only shows up in list_agentic_buckets after a while, so poll.

    Returns False when it is still missing; the caller skips instead of failing, the existence of
    the bucket is already asserted by get_agentic_bucket.
    """
    for _ in range(LIST_RETRY_TIMES):
        paginator = client.list_agentic_buckets_paginator()
        for page in paginator.iter_page(oss_agentic.models.ListAgenticBucketsRequest()):
            case.assertEqual(200, page.status_code)
            if page.agentic_buckets is None:
                continue
            for summary in page.agentic_buckets:
                if summary.name is not None and bucket in summary.name:
                    return True
        time.sleep(LIST_RETRY_INTERVAL_SECONDS)
    return False


def disable_agentic_bucket_quietly(bucket: str) -> None:
    """Best-effort: the bucket of the current run must not be left Enabled, otherwise no later run
    is allowed to reclaim it.
    """
    if bucket is None:
        return
    try:
        get_agentic_client().put_agentic_bucket_status(
            oss_agentic.models.PutAgenticBucketStatusRequest(
                bucket=bucket,
                agentic_bucket_status=oss_agentic.models.AgenticBucketStatus(status='Disabled'),
            )
        )
    except Exception:
        pass


def _detach_agentic_bucket_properties(client: oss_agentic.AgenticBucketClient, bucket: str) -> None:
    try:
        client.delete_agentic_bucket_policy(
            oss_agentic.models.DeleteAgenticBucketPolicyRequest(bucket=bucket)
        )
    except Exception:
        pass
    try:
        client.delete_agentic_bucket_encryption(
            oss_agentic.models.DeleteAgenticBucketEncryptionRequest(bucket=bucket)
        )
    except Exception:
        pass
    try:
        client.delete_agentic_bucket_public_access_block(
            oss_agentic.models.DeleteAgenticBucketPublicAccessBlockRequest(bucket=bucket)
        )
    except Exception:
        pass


def clean_bucket_space_objects(space_full_name: str) -> None:
    """Empty a bucket space, a non-empty one cannot be deleted. Best-effort."""
    try:
        client = get_default_client()
        paginator = client.list_objects_v2_paginator()
        for page in paginator.iter_page(oss.models.ListObjectsV2Request(bucket=space_full_name)):
            if page.contents is None:
                continue
            for obj in page.contents:
                try:
                    client.delete_object(
                        oss.models.DeleteObjectRequest(bucket=space_full_name, key=obj.key)
                    )
                except Exception:
                    pass
    except Exception:
        pass


def delete_bucket_space_quietly(space_full_name: str) -> None:
    """Delete a bucket space by its full name. Best-effort."""
    try:
        get_default_client().delete_bucket(
            oss.models.DeleteBucketRequest(bucket=space_full_name)
        )
    except Exception:
        pass


def _reap_bucket_spaces(client: oss_agentic.AgenticBucketClient, bucket: str) -> None:
    try:
        paginator = client.list_bucket_spaces_paginator()
        for page in paginator.iter_page(oss_agentic.models.ListBucketSpacesRequest(bucket=bucket)):
            if page.bucket_spaces is None:
                continue
            for space in page.bucket_spaces:
                if space.name is None:
                    continue
                # A non-empty bucket space cannot be deleted, and an agentic bucket that still
                # owns a bucket space cannot be deleted either.
                clean_bucket_space_objects(space.name)
                delete_bucket_space_quietly(space.name)
    except Exception:
        pass


def clean_agentic_bucket(client: oss_agentic.AgenticBucketClient, bucket: str) -> None:
    """Reclaim one agentic bucket that is already Disabled. Best-effort."""
    _detach_agentic_bucket_properties(client, bucket)
    _reap_bucket_spaces(client, bucket)
    # Answers 409 AgenticBucketNotReady until the readiness window has elapsed.
    try:
        client.delete_agentic_bucket(
            oss_agentic.models.DeleteAgenticBucketRequest(bucket=bucket)
        )
    except Exception as e:
        print('agentic bucket not reclaimed yet:', bucket, e)


def clean_agentic_buckets(prefix: str) -> None:
    """Reclaim the agentic buckets left behind by the previous runs. Best-effort, every error is
    swallowed so that teardown never fails.
    """
    try:
        client = get_agentic_client()
        paginator = client.list_agentic_buckets_paginator()
        for page in paginator.iter_page(oss_agentic.models.ListAgenticBucketsRequest()):
            if page.agentic_buckets is None:
                continue
            for bucket in page.agentic_buckets:
                if bucket.name is None or not bucket.name.startswith(prefix):
                    continue
                short_name = to_short_name(bucket.name, AGENTIC_BUCKET_SUFFIX)
                # The list summary carries no status, so fetch it: an Enabled bucket may belong to
                # a concurrently running job and must not be touched.
                status = None
                try:
                    result = client.get_agentic_bucket(
                        oss_agentic.models.GetAgenticBucketRequest(bucket=short_name)
                    )
                    if result.agentic_bucket_info is not None:
                        status = result.agentic_bucket_info.status
                except Exception:
                    pass
                if status != 'Disabled':
                    continue
                clean_agentic_bucket(client, short_name)
    except Exception:
        pass


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
        cls.agentic_bucket_name = gen_agentic_bucket_name()
        cls.full_agentic_bucket_name = get_full_agentic_bucket_name(cls.agentic_bucket_name)
        cls.agentic_client.create_agentic_bucket(
            oss_agentic.models.CreateAgenticBucketRequest(
                bucket=cls.agentic_bucket_name,
                create_agentic_bucket_configuration=oss_agentic.models.CreateAgenticBucketConfiguration(
                    storage_class='Standard',
                    data_redundancy_type='LRS',
                ),
            )
        )
        # Wait for cache expiration
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        # A bucket left Enabled can never be reclaimed, so disable this run's bucket even when the
        # scenario failed. Only then reap the backlog of the previous runs.
        disable_agentic_bucket_quietly(cls.agentic_bucket_name)
        clean_agentic_buckets(AGENTIC_BUCKET_NAME_PREFIX)

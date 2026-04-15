# -*- coding: utf-8 -*-
"""Operations for tables."""

from .namespace_basic import (
    create_namespace,
    delete_namespace,
    get_namespace,
    list_namespaces,
)

from .table_bucket_basic import (
    create_table_bucket,
    delete_table_bucket,
    get_table_bucket,
    list_table_buckets,
)

from .table_basic import (
    create_table,
    delete_table,
    get_table,
    list_tables,
    rename_table,
)

from .table_config_basic import (
    get_table_encryption,
    get_table_maintenance_configuration,
    put_table_maintenance_configuration,
    get_table_maintenance_job_status,
    get_table_metadata_location,
    update_table_metadata_location,
    delete_table_policy,
    get_table_policy,
    put_table_policy,
)

from .table_bucket_config_basic import (
    delete_table_bucket_encryption,
    get_table_bucket_encryption,
    put_table_bucket_encryption,
    get_table_bucket_maintenance_configuration,
    put_table_bucket_maintenance_configuration,
    delete_table_bucket_policy,
    get_table_bucket_policy,
    put_table_bucket_policy,
)

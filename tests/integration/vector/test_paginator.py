# pylint: skip-file

import alibabacloud_oss_v2.vectors as oss_vectors
from tests.integration import TestIntegrationVectors, random_bucket_name, random_short_bucket_name

class TestPaginatorBasic(TestIntegrationVectors):
    def test_list_vector_buckets_paginator(self):
        # Create test vector buckets with a common prefix
        bucket_name_prefix = random_short_bucket_name()
        bucket_name1 = bucket_name_prefix + '-1'
        self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(bucket=bucket_name1))
        bucket_name2 = bucket_name_prefix + '-2'
        self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(bucket=bucket_name2))
        bucket_name3 = bucket_name_prefix + '-3'
        self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(bucket=bucket_name3))

        # Test paginator with limit parameter set during initialization
        paginator = self.vector_client.list_vector_buckets_paginator(limit=1)
        request = oss_vectors.models.ListVectorBucketsRequest(
            prefix=bucket_name_prefix
        )
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(1, len(p.buckets))
            # Verify that bucket names start with the bucket_name_prefix
            vals = p.buckets[0].name.split(':')
            self.assertTrue(vals[4].startswith(bucket_name_prefix))
            j += 1
        self.assertIsNone(request.marker)

        # Test paginator with custom limit parameter
        iterator = paginator.iter_page(request, limit=3)
        for p in iterator:
            if p.is_truncated:
                self.assertEqual(3, p.max_keys)
            self.assertEqual(3, len(p.buckets))
            # Verify that all bucket names start with the bucket_name_prefix
            for bucket in p.buckets:
                vals = bucket.name.split(':')
                self.assertTrue(vals[4].startswith(bucket_name_prefix))
        self.assertIsNone(request.marker)

        # Test default paginator without limit
        paginator = self.vector_client.list_vector_buckets_paginator()
        request = oss_vectors.models.ListVectorBucketsRequest(prefix=bucket_name_prefix)
        iterator = paginator.iter_page(request)
        j = 0
        for p in iterator:
            self.assertEqual(3, len(p.buckets))
            # Verify that all bucket names start with the bucket_name_prefix
            for bucket in p.buckets:
                vals = bucket.name.split(':')
                self.assertTrue(vals[4].startswith(bucket_name_prefix))
            j += 1
        self.assertEqual(1, j)

    def test_list_vector_index_paginator(self):
        # Create a test vector bucket
        bucket_name = random_short_bucket_name()
        result = self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(bucket=bucket_name))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # Create test vector indexes
        index_name1 = "testindex1"
        index_name2 = "testindex2"
        index_name3 = "testindex3"

        # Create vector indexes using put_vector_index
        self.vector_client.put_vector_index(oss_vectors.models.PutVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name1,
            data_type='float32',
            dimension=128,
            distance_metric='cosine',
            metadata={"nonFilterableMetadataKeys": ["key1", "key2"]}
        ))

        self.vector_client.put_vector_index(oss_vectors.models.PutVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name2,
            data_type='float32',
            dimension=128,
            distance_metric='cosine',
            metadata={"nonFilterableMetadataKeys": ["key1", "key2"]}
        ))

        self.vector_client.put_vector_index(oss_vectors.models.PutVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name3,
            data_type='float32',
            dimension=128,
            distance_metric='cosine',
            metadata={"nonFilterableMetadataKeys": ["key1", "key2"]}
        ))

        # Test paginator with limit parameter set during initialization
        paginator = self.vector_client.list_vector_indexes_paginator(limit=1)
        request = oss_vectors.models.ListVectorIndexesRequest(
            bucket=bucket_name
        )
        iterator = paginator.iter_page(request)
        pages = []
        for p in iterator:
            pages.append(p)
            self.assertEqual(1, len(p.indexes))
        self.assertEqual(3, len(pages))

        # Test paginator with custom limit parameter
        paginator = self.vector_client.list_vector_indexes_paginator(limit=2)
        iterator = paginator.iter_page(request, limit=3)
        pages = []
        for p in iterator:
            pages.append(p)

            if hasattr(p, 'max_results'):
                self.assertEqual(3, p.max_results)
            self.assertLessEqual(len(p.indexes), 3)
        self.assertGreater(len(pages), 0)

        # Test default paginator without limit
        paginator = self.vector_client.list_vector_indexes_paginator()
        iterator = paginator.iter_page(request)
        total_indexes = 0
        for p in iterator:
            total_indexes += len(p.indexes)
        self.assertEqual(3, total_indexes)

        # Check that next_token is properly handled
        if hasattr(request, 'next_token'):
            self.assertIsNone(request.next_token)

    def test_list_vectors_paginator(self):
        # Create a test vector bucket
        bucket_name = random_short_bucket_name()
        self.vector_client.put_vector_bucket(oss_vectors.models.PutVectorBucketRequest(bucket=bucket_name))

        # Create test vectors using put_vectors
        index_name = "testindex"

        self.vector_client.put_vector_index(oss_vectors.models.PutVectorIndexRequest(
            bucket=bucket_name,
            index_name=index_name,
            data_type='float32',
            dimension=4,
            distance_metric='cosine',
            metadata={"nonFilterableMetadataKeys": ["key1", "key2"]}
        ))

        # Insert vectors using put_vectors
        vectors_data = [
            {
                "data": {"float32": [0.1, 0.2, 0.3, 0.4]},
                "key": "vec1",
                "metadata": {"key1": "value1"}
            },
            {
                "data": {"float32": [0.2, 0.3, 0.4, 0.5]},
                "key": "vec2",
                "metadata": {"key2": "value2"}
            },
            {
                "data": {"float32": [0.3, 0.4, 0.5, 0.6]},
                "key": "vec3",
                "metadata": {"key3": "value3"}
            }
        ]

        # Insert vectors
        self.vector_client.put_vectors(oss_vectors.models.PutVectorsRequest(
            bucket=bucket_name,
            index_name=index_name,
            vectors=vectors_data
        ))

        # Test paginator with limit parameter set during initialization
        paginator = self.vector_client.list_vectors_paginator(limit=1)
        request = oss_vectors.models.ListVectorsRequest(
            bucket=bucket_name,
            index_name=index_name
        )
        iterator = paginator.iter_page(request)
        count = 0
        for p in iterator:
            self.assertEqual(1, len(p.vectors))
            count += 1
        self.assertEqual(3, count)

        # Test paginator with custom limit parameter
        paginator = self.vector_client.list_vectors_paginator()
        request = oss_vectors.models.ListVectorsRequest(
            bucket=bucket_name,
            index_name=index_name
        )
        iterator = paginator.iter_page(request, limit=2)
        pages = list(iterator)
        self.assertGreater(len(pages), 0)
        total_vectors = sum(len(page.vectors) for page in pages)
        self.assertEqual(3, total_vectors)

        # Test default paginator without limit
        paginator = self.vector_client.list_vectors_paginator()
        request = oss_vectors.models.ListVectorsRequest(
            bucket=bucket_name,
            index_name=index_name
        )
        iterator = paginator.iter_page(request)
        total_vectors = 0
        for p in iterator:
            total_vectors += len(p.vectors)
        self.assertEqual(3, total_vectors)

        # Check that next_token is properly handled
        if hasattr(request, 'next_token'):
            self.assertIsNone(request.next_token)

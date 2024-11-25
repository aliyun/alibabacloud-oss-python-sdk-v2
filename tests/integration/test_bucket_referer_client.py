# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestBucketReferer(TestIntegration):

    def test_bucket_referer(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket referer
        result = self.client.put_bucket_referer(oss.PutBucketRefererRequest(
            bucket=bucket_name,
            referer_configuration=oss.RefererConfiguration(
                allow_empty_referer=True,
                allow_truncate_query_string=True,
                truncate_path=False,
                referer_list=oss.RefererList(
                    referers=['LGO3<m&s9<', 'szq,1RZ>VI'],
                ),
                referer_blacklist=oss.RefererBlacklist(
                    referers=['e6MZh;>_<s', 'z\E2$-X9UQ'],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket referer
        result = self.client.get_bucket_referer(oss.GetBucketRefererRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(True, result.referer_configuration.allow_empty_referer)
        self.assertEqual(True, result.referer_configuration.allow_truncate_query_string)
        self.assertEqual(False, result.referer_configuration.truncate_path)
        self.assertEqual(['LGO3<m&s9<', 'szq,1RZ>VI'], result.referer_configuration.referer_list.referers)
        self.assertEqual(['e6MZh;>_<s', 'z\E2$-X9UQ'], result.referer_configuration.referer_blacklist.referers)


    def test_bucket_referer_v1(self):
        # create bucket
        bucket_name = random_bucket_name()
        result = self.signv1_client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # put bucket referer
        result = self.signv1_client.put_bucket_referer(oss.PutBucketRefererRequest(
            bucket=bucket_name,
            referer_configuration=oss.RefererConfiguration(
                allow_empty_referer=True,
                allow_truncate_query_string=True,
                truncate_path=True,
                referer_list=oss.RefererList(
                    referers=['Sc6+B5BJKN', '?yBc/alQK/'],
                ),
                referer_blacklist=oss.RefererBlacklist(
                    referers=['cy<Ebh/6e;', 'c*J$\qf4>t'],
                ),
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get bucket referer
        result = self.signv1_client.get_bucket_referer(oss.GetBucketRefererRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(True, result.referer_configuration.allow_empty_referer)
        self.assertEqual(True, result.referer_configuration.allow_truncate_query_string)
        self.assertEqual(False, result.referer_configuration.truncate_path)
        self.assertEqual(['LGO3<m&s9<', 'szq,1RZ>VI'], result.referer_configuration.referer_list.referers)
        self.assertEqual(['e6MZh;>_<s', 'z\E2$-X9UQ'], result.referer_configuration.referer_blacklist.referers)


    def test_bucket_referer_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put bucket referer
        try:
            self.invalid_client.put_bucket_referer(oss.PutBucketRefererRequest(
                bucket=bucket_name,
                referer_configuration=oss.RefererConfiguration(
                    allow_empty_referer=True,
                    allow_truncate_query_string=True,
                    truncate_path=True,
                    referer_list=oss.RefererList(
                        referers=[':u+m5aSOZ', 'kuN(1+iB/k'],
                    ),
                    referer_blacklist=oss.RefererBlacklist(
                        referers=['HbYyj3d5vB', 'e/+C\K.!(V'],
                    ),
                ),
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # get bucket referer
        try:
            self.invalid_client.get_bucket_referer(oss.GetBucketRefererRequest(
                bucket=bucket_name,
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)
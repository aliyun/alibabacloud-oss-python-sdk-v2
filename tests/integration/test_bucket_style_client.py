# pylint: skip-file

from typing import cast
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_bucket_name


class TestStyle(TestIntegration):

    def test_style(self):
        style_name = 'imagestyle'
        style_name_2 = 'imagestyle2'

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

        # put style
        result = self.client.put_style(oss.PutStyleRequest(
            bucket=bucket_name,
            style_name=style_name,
            category='image',
            style=oss.StyleContent(
                content='image/resize,p_50',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get style
        result = self.client.get_style(oss.GetStyleRequest(
            bucket=bucket_name,
            style_name=style_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('image/resize,p_50', result.style.content)
        self.assertEqual('image', result.style.category)

        # put style
        result = self.client.put_style(oss.PutStyleRequest(
            bucket=bucket_name,
            style_name=style_name_2,
            category='image',
            style=oss.StyleContent(
                content='image/resize,w_200',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # list style
        result = self.client.list_style(oss.ListStyleRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(style_name, result.style_list.styles[0].name)
        self.assertEqual('image/resize,p_50', result.style_list.styles[0].content)
        self.assertEqual('image', result.style_list.styles[0].category)
        self.assertEqual(style_name_2, result.style_list.styles[1].name)
        self.assertEqual('image/resize,w_200', result.style_list.styles[1].content)
        self.assertEqual('image', result.style_list.styles[1].category)

        # delete style
        result = self.client.delete_style(oss.DeleteStyleRequest(
            bucket=bucket_name,
            style_name=style_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # delete style
        result = self.client.delete_style(oss.DeleteStyleRequest(
            bucket=bucket_name,
            style_name=style_name_2,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

    def test_style_v1(self):
        style_name = 'imagestyle'
        style_name_2 = 'imagestyle2'

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

        # put style
        result = self.signv1_client.put_style(oss.PutStyleRequest(
            bucket=bucket_name,
            style_name=style_name,
            category='image',
            style=oss.StyleContent(
                content='image/resize,p_50',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # get style
        result = self.signv1_client.get_style(oss.GetStyleRequest(
            bucket=bucket_name,
            style_name=style_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual('image/resize,p_50', result.style.content)
        self.assertEqual('image', result.style.category)

        # put style
        result = self.signv1_client.put_style(oss.PutStyleRequest(
            bucket=bucket_name,
            style_name=style_name_2,
            category='image',
            style=oss.StyleContent(
                content='image/resize,w_200',
            ),
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # list style
        result = self.signv1_client.list_style(oss.ListStyleRequest(
            bucket=bucket_name,
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
        self.assertEqual(style_name, result.style_list.styles[0].name)
        self.assertEqual('image/resize,p_50', result.style_list.styles[0].content)
        self.assertEqual('image', result.style_list.styles[0].category)
        self.assertEqual(style_name_2, result.style_list.styles[1].name)
        self.assertEqual('image/resize,w_200', result.style_list.styles[1].content)
        self.assertEqual('image', result.style_list.styles[1].category)

        # delete style
        result = self.signv1_client.delete_style(oss.DeleteStyleRequest(
            bucket=bucket_name,
            style_name=style_name,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))

        # delete style
        result = self.signv1_client.delete_style(oss.DeleteStyleRequest(
            bucket=bucket_name,
            style_name=style_name_2,
        ))
        self.assertEqual(204, result.status_code)
        self.assertEqual(24, len(result.request_id))
        self.assertEqual(24, len(result.headers.get('x-oss-request-id')))
    def test_style_fail(self):
        # create bucket
        bucket_name = random_bucket_name()
        self.client.put_bucket(oss.PutBucketRequest(
            bucket=bucket_name,
            acl='private',
            create_bucket_configuration=oss.CreateBucketConfiguration(
                storage_class='IA'
            )
        ))

        # put style
        try:
            self.invalid_client.put_style(oss.PutStyleRequest(
                bucket=bucket_name,
                style_name='test-value',
                category='test_category',
                style=oss.StyleContent(
                    content='test_content',
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

        # get style
        try:
            self.invalid_client.get_style(oss.GetStyleRequest(
                bucket=bucket_name,
                style_name='imagestyle',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

        # list style
        try:
            self.invalid_client.list_style(oss.ListStyleRequest(
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

        # delete style
        try:
            self.invalid_client.delete_style(oss.DeleteStyleRequest(
                bucket=bucket_name,
                style_name='imagestyle',
            ))
            self.fail("should not here")
        except Exception as e:
            ope = cast(oss.exceptions.OperationError, e)
            self.assertIsInstance(ope.unwrap(), oss.exceptions.ServiceError)
            serr = cast(oss.exceptions.ServiceError, ope.unwrap())
            self.assertEqual(403, serr.status_code)
            self.assertEqual(24, len(serr.request_id))
            self.assertEqual('InvalidAccessKeyId', serr.code)

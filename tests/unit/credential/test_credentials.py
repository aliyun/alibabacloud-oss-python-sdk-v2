# pylint: skip-file
import unittest
import datetime

from alibabacloud_oss_v2 import credentials
from alibabacloud_oss_v2.types import Credentials

class TestCredentials(unittest.TestCase):
    
    def test_anonymous_credentials_provider(self):
        provider = credentials.AnonymousCredentialsProvider()
        cred = provider.get_credentials()
        self.assertEqual('', cred.access_key_id)
        self.assertEqual('', cred.access_key_secret)
        self.assertEqual(None, cred.security_token)
        self.assertEqual(None, cred.expiration)
        self.assertEqual(False, cred.is_expired())

    def test_static_credentials_provider(self):
        provider = credentials.StaticCredentialsProvider(
            access_key_id='ak',
            access_key_secret='sk'
        )
        cred = provider.get_credentials()
        self.assertEqual('ak', cred.access_key_id)
        self.assertEqual('sk', cred.access_key_secret)
        self.assertEqual(None, cred.security_token)
        self.assertEqual(None, cred.expiration)
        self.assertEqual(False, cred.is_expired())

        provider = credentials.StaticCredentialsProvider(
            access_key_id='ak',
            access_key_secret='sk',
            security_token='token'
        )
        cred = provider.get_credentials()
        self.assertEqual('ak', cred.access_key_id)
        self.assertEqual('sk', cred.access_key_secret)
        self.assertEqual('token', cred.security_token)
        self.assertEqual(None, cred.expiration)
        self.assertEqual(False, cred.is_expired())


    def test_credentials_provider_func(self):
        provider = credentials.CredentialsProviderFunc(
            func= lambda : Credentials(access_key_id='ak-1', access_key_secret='sk-1')
        )
        cred = provider.get_credentials()
        self.assertEqual('ak-1', cred.access_key_id)
        self.assertEqual('sk-1', cred.access_key_secret)
        self.assertEqual(None, cred.security_token)
        self.assertEqual(None, cred.expiration)
        self.assertEqual(False, cred.is_expired())

        provider = credentials.CredentialsProviderFunc(
            func= lambda : Credentials('ak-1', 'sk-1', 'token-1')
        )
        cred = provider.get_credentials()
        self.assertEqual('ak-1', cred.access_key_id)
        self.assertEqual('sk-1', cred.access_key_secret)
        self.assertEqual('token-1', cred.security_token)
        self.assertEqual(None, cred.expiration)
        self.assertEqual(False, cred.is_expired())

        expiration = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1)
        self.assertIsNotNone(expiration)

        provider = credentials.CredentialsProviderFunc(
            func= lambda : Credentials('ak-1', 'sk-1', 'token-1', expiration)
        )
        cred = provider.get_credentials()
        self.assertEqual('ak-1', cred.access_key_id)
        self.assertEqual('sk-1', cred.access_key_secret)
        self.assertEqual('token-1', cred.security_token)
        self.assertEqual(expiration, cred.expiration)
        self.assertEqual(True, cred.is_expired())

        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
        self.assertIsNotNone(expiration)

        provider = credentials.CredentialsProviderFunc(
            func= lambda : Credentials('ak-2', 'sk-2', 'token-2', expiration)
        )
        cred = provider.get_credentials()
        self.assertEqual('ak-2', cred.access_key_id)
        self.assertEqual('sk-2', cred.access_key_secret)
        self.assertEqual('token-2', cred.security_token)
        self.assertEqual(expiration, cred.expiration)
        self.assertEqual(False, cred.is_expired())



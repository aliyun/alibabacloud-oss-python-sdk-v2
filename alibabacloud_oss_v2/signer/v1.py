# -*- coding: utf-8 -*-
"""V1 signature implentation
"""
import base64
import datetime
from typing import Optional
from email.utils import format_datetime
from urllib.parse import urlsplit, quote, unquote, SplitResult
from hashlib import sha1
import hmac
from .. import exceptions
from ..types import SigningContext, Signer

class SignerV1(Signer):
    """Signer V1
    """
    _subresource_key_set = frozenset(
        ['acl', 'bucketInfo', 'location', 'stat', 'delete', 'append',
         'tagging', 'objectMeta', 'uploads', 'uploadId', 'partNumber',
         'security-token', 'position', 'response-content-type', 'response-content-language',
         'response-expires', 'response-cache-control', 'response-content-disposition',
         'response-content-encoding', 'restore', 'callback', 'callback-var',
         'versions', 'versioning', 'versionId', 'sequential', 'continuation-token',
         'regionList', 'cloudboxes', 'symlink', 'resourceGroup']
    )

    def sign(self, signing_ctx: SigningContext) -> None:
        if signing_ctx is None:
            raise exceptions.ParamNullError(field="SigningContext")

        if signing_ctx.credentials is None or not signing_ctx.credentials.has_keys():
            raise exceptions.ParamNullOrEmptyError(field="SigningContext.credentials")

        if signing_ctx.request is None:
            raise exceptions.ParamNullOrEmptyError(field="SigningContext.request")

        if signing_ctx.auth_method_query:
            return self._auth_query(signing_ctx)

        return self._auth_header(signing_ctx)

    def _auth_header(self, signing_ctx: SigningContext) -> None:
        request = signing_ctx.request
        cred = signing_ctx.credentials

        #Date
        if signing_ctx.signing_time is None:
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
            datetime_now = datetime_now + datetime.timedelta(seconds= (signing_ctx.clock_offset or 0))
        else:
            datetime_now = signing_ctx.signing_time.astimezone(datetime.timezone.utc)

        datetime_now_rfc2822 = format_datetime(datetime_now, True)
        request.headers.update({'Date':datetime_now_rfc2822})

        #Credentials information
        if cred.security_token is not None:
            request.headers.update({'security-token':cred.security_token})

        #string to sign
        string_to_sign = self._calc_string_to_sign(signing_ctx=signing_ctx)
        #print('string_to_sign:{}\n'.format(string_to_sign))

        #signature
        signature = self._calc_signature(
            access_key_secrect=cred.access_key_secret,
            string_to_sign=string_to_sign)

        #credential header
        credential_header = f'OSS {cred.access_key_id}:{signature}'

        request.headers.update({'Authorization':credential_header})

        signing_ctx.string_to_sign = string_to_sign
        signing_ctx.signing_time = datetime_now


    def _auth_query(self, signing_ctx: SigningContext) -> None:
        request = signing_ctx.request
        cred = signing_ctx.credentials

        #Date
        if signing_ctx.signing_time is None:
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
        else:
            datetime_now = signing_ctx.signing_time.astimezone(datetime.timezone.utc)

        if signing_ctx.expiration_time is None:
            expiration_time = datetime.datetime.now(
                datetime.timezone.utc) + datetime.timedelta(minutes=15)
        else:
            expiration_time = signing_ctx.expiration_time.astimezone(datetime.timezone.utc)

        expires = str(int(expiration_time.timestamp()))

        encoded_pairs = {}
        parts = urlsplit(request.url)
        if parts.query:
            for pair in parts.query.split('&'):
                key, _, value = pair.partition('=')
                encoded_pairs[key] = value

        encoded_pairs.pop('Signature', None)
        encoded_pairs.pop('security-token', None)
        encoded_pairs.update(
            {
                'OSSAccessKeyId': cred.access_key_id,
                'Expires': expires,
            }
        )
        if cred.security_token is not None:
            encoded_pairs.update({'security-token': quote(cred.security_token, safe='')})

        query = []
        for key, value in encoded_pairs.items():
            if value:
                query.append(f'{key}={value}')
            else:
                query.append(f'{key}')

        parts = SplitResult(parts.scheme, parts.netloc, parts.path, '&'.join(query), parts.fragment)
        request.url = parts.geturl()

        #string to sign
        string_to_sign = self._calc_string_to_sign(signing_ctx=signing_ctx, date=expires)

        #signature
        signature = self._calc_signature(
            access_key_secrect=cred.access_key_secret,
            string_to_sign=string_to_sign)

        request.url = request.url + f'&Signature={quote(signature, safe="")}'

        # print('string_to_sign:{}\n'.format(string_to_sign))
        signing_ctx.string_to_sign = string_to_sign
        signing_ctx.signing_time = datetime_now
        signing_ctx.expiration_time = expiration_time

    def _calc_string_to_sign(self, signing_ctx: SigningContext, date: Optional[str] = None) -> str:
        """
        Canonical Request
            HTTP Verb + "\n" +
            Content-MD5 + "\n" +
            Content-Type + "\n" +
            Date + "\n" +
            CanonicalizedOSSHeaders + "\n" +
            CanonicalizedResource
        """
        request = signing_ctx.request

        # canonical uri
        uri = '/'
        if signing_ctx.bucket is not None:
            uri = uri + signing_ctx.bucket + '/'
        if signing_ctx.key is not None:
            uri = uri + signing_ctx.key
        canonical_uri = uri

        # canonical query
        canonical_query = ''
        parts = urlsplit(request.url)

        if parts.query:
            key_val_pairs = []
            for pair in parts.query.split('&'):
                key, _, value = pair.partition('=')
                key = unquote(key)
                value = unquote(value)
                if key in self._subresource_key_set:
                    key_val_pairs.append((key, value))
                elif key in signing_ctx.sub_resource:
                    key_val_pairs.append((key, value))

            sorted_key_vals = []
            for key, value in sorted(key_val_pairs):
                if len(value) > 0:
                    sorted_key_vals.append(f'{key}={value}')
                else:
                    sorted_key_vals.append(f'{key}')
            if key_val_pairs:
                canonical_query = '?' + '&'.join(sorted_key_vals)
            else:
                canonical_query = ''

        canonical_resource = canonical_uri + canonical_query

        #canonical headers
        canon_headers = []
        for k, v in request.headers.items():
            lower_key = k.lower()
            if _is_sign_header(lower_key):
                canon_headers.append((lower_key, v))
        canon_headers.sort(key=lambda x: x[0])
        canonical_headers = ''.join(v[0] + ':' + v[1] + '\n' for v in canon_headers)

        content_md5 = request.headers.get('content-md5', '')
        content_type = request.headers.get('content-type', '')

        if date is None:
            date = request.headers.get('x-oss-date', '') or request.headers.get('date', '')

        return '{}\n{}\n{}\n{}\n{}'.format(
            request.method,
            content_md5,
            content_type,
            date,
            canonical_headers + canonical_resource)

    def _calc_signature(self, access_key_secrect:str, string_to_sign:str) -> str:
        h = hmac.new(access_key_secrect.encode(), string_to_sign.encode(), sha1)
        return base64.b64encode(h.digest()).decode('utf-8')

    @staticmethod
    def is_signed_header(h: str) -> bool:
        """Determines the header is a signed header
        """
        return _is_default_sign_header(h.lower())


def _is_default_sign_header(key: str) -> bool:
    if key.startswith('x-oss-'):
        return True

    if key in ['content-type', 'content-md5', 'date']:
        return True

    return False


def _is_sign_header(key: str) -> bool:
    if key is not None:
        if key.startswith('x-oss-'):
            return True

    return False

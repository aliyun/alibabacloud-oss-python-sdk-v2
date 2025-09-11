"""V4 signature implentation
"""
import datetime
from email.utils import format_datetime
from typing import Optional, Set
from urllib.parse import urlsplit, quote, SplitResult
from hashlib import sha256
import hmac

from .. import exceptions
from ..types import HttpRequest, SigningContext, Signer


class VectorsSignerV4(Signer):
    """Signer Vectors V4
    """

    def __init__(self, account_id: str) -> None:
        self._account_id = account_id

    def sign(self, signing_ctx: SigningContext) -> None:
        if signing_ctx is None:
            raise exceptions.ParamNullError(field="SigningContext")

        if signing_ctx.credentials is None or not signing_ctx.credentials.has_keys():
            raise exceptions.ParamNullOrEmptyError(
                field="SigningContext.credentials")

        if signing_ctx.request is None:
            raise exceptions.ParamNullOrEmptyError(
                field="SigningContext.request")
        
        if self._account_id is None or self._account_id == '':
            raise exceptions.ParamNullOrEmptyError(
                field="SignerVectorsV4.account_id")

        if signing_ctx.auth_method_query:
            return self._auth_query(signing_ctx)

        return self._auth_header(signing_ctx)

    def _auth_header(self, signing_ctx: SigningContext) -> None:
        request = signing_ctx.request
        cred = signing_ctx.credentials

        # Date
        if signing_ctx.signing_time is None:
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
            datetime_now = datetime_now + \
                datetime.timedelta(seconds=(signing_ctx.clock_offset or 0))
        else:
            datetime_now = signing_ctx.signing_time.astimezone(
                datetime.timezone.utc)

        datetime_now_iso8601 = datetime_now.strftime('%Y%m%dT%H%M%SZ')
        datetime_now_rfc2822 = format_datetime(datetime_now, True)
        date_now_iso8601 = datetime_now_iso8601[:8]
        request.headers.update({'x-oss-date': datetime_now_iso8601})
        request.headers.update({'Date': datetime_now_rfc2822})

        # Credentials information
        if cred.security_token is not None:
            request.headers.update(
                {'x-oss-security-token': cred.security_token})

        # Other Headers
        request.headers.update({'x-oss-content-sha256': 'UNSIGNED-PAYLOAD'})

        # Scope
        region = signing_ctx.region or ''
        product = signing_ctx.product or ''
        scope = self._build_scope(
            date=date_now_iso8601, region=region, product=product)

        # additional headers
        additional_headers = self._common_additional_headers(
            request, signing_ctx.additional_headers)

        # Canonical request
        canonical_request = self._calc_canonical_request(
            signing_ctx=signing_ctx, additional_headers=additional_headers)

        # string to sign
        string_to_sign = self._calc_string_to_sign(
            datetime_now_iso8601, scope, canonical_request)

        # print('\ncanonical_request:{}\n'.format(canonical_request))
        # print('string_to_sign:{}\n'.format(string_to_sign))

        # signature
        signature = self._calc_signature(
            access_key_secrect=cred.access_key_secret,
            date=date_now_iso8601,
            region=region,
            product=product,
            string_to_sign=string_to_sign)

        # credential header
        credential_header = f'OSS4-HMAC-SHA256 Credential={cred.access_key_id}/{scope}'
        if len(additional_headers) > 0:
            credential_header = f'{credential_header},AdditionalHeaders={";".join(additional_headers)}'
        credential_header = f'{credential_header},Signature={signature}'

        request.headers.update({'Authorization': credential_header})

        signing_ctx.string_to_sign = string_to_sign
        signing_ctx.signing_time = datetime_now

    def _auth_query(self, signing_ctx: SigningContext) -> None:
        request = signing_ctx.request
        cred = signing_ctx.credentials

        # Date
        if signing_ctx.signing_time is None:
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
        else:
            datetime_now = signing_ctx.signing_time.astimezone(
                datetime.timezone.utc)

        if signing_ctx.expiration_time is None:
            expiration_time = datetime.datetime.now(
                datetime.timezone.utc) + datetime.timedelta(minutes=15)
        else:
            expiration_time = signing_ctx.expiration_time.astimezone(
                datetime.timezone.utc)

        datetime_now_iso8601 = datetime_now.strftime('%Y%m%dT%H%M%SZ')
        date_now_iso8601 = datetime_now_iso8601[:8]
        expires = int((expiration_time - datetime_now).total_seconds())

        # Scope
        region = signing_ctx.region or ''
        product = signing_ctx.product or ''
        scope = self._build_scope(
            date=date_now_iso8601, region=region, product=product)

        # additional headers
        additional_headers = self._common_additional_headers(
            request, signing_ctx.additional_headers)

        # credentials information
        encoded_pairs = {}
        parts = urlsplit(request.url)
        if parts.query:
            for pair in parts.query.split('&'):
                key, _, value = pair.partition('=')
                encoded_pairs[key] = value

        encoded_pairs.pop('x-oss-signature', None)
        encoded_pairs.pop('x-oss-security-token', None)
        encoded_pairs.pop('x-oss-additional-headers', None)
        encoded_pairs.update(
            {
                'x-oss-signature-version': 'OSS4-HMAC-SHA256',
                'x-oss-date': datetime_now_iso8601,
                'x-oss-expires': str(expires),
                'x-oss-credential': quote(f'{cred.access_key_id}/{scope}', safe='')
            }
        )
        if cred.security_token is not None:
            encoded_pairs.update(
                {'x-oss-security-token': quote(cred.security_token, safe='')})

        if len(additional_headers) > 0:
            encoded_pairs.update(
                {'x-oss-additional-headers': quote(';'.join(additional_headers), safe='')})

        query = []
        for key, value in encoded_pairs.items():
            if value:
                query.append(f'{key}={value}')
            else:
                query.append(f'{key}')

        parts = SplitResult(parts.scheme, parts.netloc,
                            parts.path, '&'.join(query), parts.fragment)
        request.url = parts.geturl()

        # print('\nrequest.url:{}'.format(request.url))

        # Canonical request
        canonical_request = self._calc_canonical_request(
            signing_ctx=signing_ctx, additional_headers=additional_headers)

        # string to sign
        string_to_sign = self._calc_string_to_sign(
            datetime_now_iso8601, scope, canonical_request)

        # signature
        signature = self._calc_signature(
            access_key_secrect=cred.access_key_secret,
            date=date_now_iso8601,
            region=region,
            product=product,
            string_to_sign=string_to_sign)

        request.url = request.url + f'&x-oss-signature={quote(signature, safe="")}'

        # print('\ncanonical_request:{}\n'.format(canonical_request))
        # print('string_to_sign:{}\n'.format(string_to_sign))
        signing_ctx.string_to_sign = string_to_sign
        signing_ctx.signing_time = datetime_now
        signing_ctx.expiration_time = expiration_time

    def _build_scope(self, date: str, region: str, product: str) -> str:
        return f'{date}/{region}/{product}/aliyun_v4_request'

    def _common_additional_headers(self, request: HttpRequest,
                                   additional_headers: Optional[Set[str]] = None
                                   ) -> Set[str]:
        keys = set()
        if additional_headers is None or request is None:
            return keys

        for k in additional_headers:
            lk = k.lower()
            if _is_default_sign_header(lk):
                continue
            elif len(request.headers.get(lk, '')) > 0:
                keys.add(lk)

        keys = sorted(keys)
        return keys

    def _calc_canonical_request(self,
                                signing_ctx: SigningContext,
                                additional_headers: Optional[Set[str]] = None
                                ) -> str:
        """
        Canonical Request
            HTTP Verb + "\n" +
            Canonical URI + "\n" +
            Canonical Query String + "\n" +
            Canonical Headers + "\n" +
            Additional Headers + "\n" +
            Hashed PayLoad
        """
        request = signing_ctx.request

        # canonical uri
        uri = f'/acs:ossvector:{signing_ctx.region}:'
        if signing_ctx.bucket is not None:
            uri += f'{self._account_id}:{signing_ctx.bucket}/'
        else:
            uri += ':/'
        if signing_ctx.key is not None:
            uri += f'{signing_ctx.key}'
        canonical_uri = quote(uri, safe='/')

        # canonical query
        canonical_query = ''
        parts = urlsplit(request.url)
        if parts.query:
            key_val_pairs = []
            for pair in parts.query.split('&'):
                key, _, value = pair.partition('=')
                key_val_pairs.append((key, value))
            sorted_key_vals = []
            for key, value in sorted(key_val_pairs):
                if len(value) > 0:
                    sorted_key_vals.append(f'{key}={value}')
                else:
                    sorted_key_vals.append(f'{key}')
            canonical_query = '&'.join(sorted_key_vals)

        # canonical headers
        canon_headers = []
        # canon_headers = [('x-oss-meta-aaa', 'value2'), ('x-oss-meta-ABC', 'value7'), ('x-oss-content-sha256', 'UNSIGNED-PAYLOAD'), ('x-oss-date', '20231216T162057Z')]
        for k, v in request.headers.items():
            lower_key = k.lower()
            if _is_sign_header(lower_key, additional_headers):
                canon_headers.append((lower_key, v))
        canon_headers.sort(key=lambda x: x[0])
        canonical_headers = ''.join(
            v[0] + ':' + v[1] + '\n' for v in canon_headers)

        # canonical additional Headers
        canonical_additional_headers = ';'.join(additional_headers)

        # hash payload
        hash_payload = request.headers.get(
            'x-oss-content-sha256', 'UNSIGNED-PAYLOAD')

        return f'{request.method}\n{canonical_uri}\n{canonical_query}\n{canonical_headers}\n{canonical_additional_headers}\n{hash_payload}'

    def _calc_string_to_sign(self, datetime_: str, scope: str, canonical_request: str) -> str:
        """
        StringToSign
            "OSS4-HMAC-SHA256" + "\n" +
            TimeStamp + "\n" +
            Scope + "\n" +
            Hex(SHA256Hash(Canonical Request))
        """
        values = ['OSS4-HMAC-SHA256']
        values.append(datetime_)
        values.append(scope)
        values.append(sha256(canonical_request.encode('utf-8')).hexdigest())
        return '\n'.join(values)

    def _calc_signature(self, access_key_secrect: str, date: str, region: str, product: str, string_to_sign: str) -> str:
        key_secret = ('aliyun_v4' + access_key_secrect).encode('utf-8')
        signing_date = hmac.new(
            key_secret, date.encode('utf-8'), sha256).digest()
        signing_region = hmac.new(
            signing_date, region.encode('utf-8'), sha256).digest()
        signing_product = hmac.new(
            signing_region, product.encode('utf-8'), sha256).digest()
        signing_key = hmac.new(
            signing_product, 'aliyun_v4_request'.encode('utf-8'), sha256).digest()
        signature = hmac.new(
            signing_key, string_to_sign.encode(), sha256).hexdigest()
        return signature

    @staticmethod
    def is_signed_header(h: str) -> bool:
        """Determines the header is a signed header
        """
        return _is_default_sign_header(h.lower())


def _is_default_sign_header(key: str) -> bool:
    if key.startswith('x-oss-'):
        return True

    if key in ['content-type', 'content-md5']:
        return True

    return False


def _is_sign_header(key: str, additional_headers) -> bool:
    if key is not None:
        if key.startswith('x-oss-'):
            return True

        if key in ['content-type', 'content-md5']:
            return True

        if additional_headers is not None and key in additional_headers:
            return True

    return False

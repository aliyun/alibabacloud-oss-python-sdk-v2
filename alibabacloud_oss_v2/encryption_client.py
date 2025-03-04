# pylint: disable=line-too-long
"""Encryption Client"""
import copy
import base64
from typing import MutableMapping, List, Optional, cast
from .types import StreamBody, CaseInsensitiveDict
from .client import Client
from . import models
from . import exceptions
from . import utils
from . import io_utils
from .crypto import MasterCipher, Envelope, ContentCipherBuilder, ContentCipher, CipherData
from .crypto.aes_ctr_cipher import AESCtrCipherBuilder
from .crypto.aes_ctr import _BLOCK_SIZE_LEN

class EncryptionMultiPartContext:
    """EncryptionMultiPartContext save encryption or decryption information
    """    
    def __init__(
        self,
        content_cipher: ContentCipher,
        data_size: int,
        part_size: int,
    ) -> None:
        self.content_cipher = content_cipher
        self.data_size = data_size
        self.part_size = part_size

    def is_valid(self) -> bool:
        """is valid
        """
        if (self.content_cipher is None or
            self.data_size == 0 or
            self.part_size == 0):
            return False

        return True

class EncryptionClient:
    """Encryption Client
    """

    def __init__(
        self,
        client: Client,
        master_cipher: MasterCipher,
        decrypt_master_ciphers: Optional[List[MasterCipher]] = None,
    ) -> None:
        self._client = client
        self._master_cipher = master_cipher
        self._defualt_ccbuilder = AESCtrCipherBuilder(master_cipher)
        self._decrypt_master_ciphers = decrypt_master_ciphers or []
        self._ccbuilders = {}
        for mc in self._decrypt_master_ciphers:
            mat_desc = mc.get_mat_desc() or ''
            if len(mat_desc) > 0:
                self._ccbuilders[mat_desc] = AESCtrCipherBuilder(mc)

    def unwrap(self) -> Client:
        """unwrap

        Returns:
            Client: _description_
        """
        return self._client

    def __repr__(self) -> str:
        return "<OssEncryptionClient>"

     # object
    def put_object(self, request: models.PutObjectRequest, **kwargs
                   ) -> models.PutObjectResult:
        """
        Uploads objects.

        Args:
            request (PutObjectRequest): Request parameters for PutObject operation.

        Returns:
            PutObjectResult: Reponse result for PutObject operation.
        """

        return self._put_object_securely(request, **kwargs)

    def get_object(self, request: models.GetObjectRequest, **kwargs
                   ) -> models.GetObjectResult:
        """
        Queries an object. To call this operation, you must have read permissions on the object.

        Args:
            request (GetObjectRequest): Request parameters for GetObject operation.

        Returns:
            GetObjectResult: Reponse result for GetObject operation.
        """

        return self._get_object_securely(request, **kwargs)

    def head_object(self, request: models.HeadObjectRequest, **kwargs
                    ) -> models.HeadObjectResult:
        """
        Queries information about the object in a bucket.

        Args:
            request (HeadObjectRequest): Request parameters for HeadObject operation.

        Returns:
            HeadObjectResult: Reponse result for HeadObject operation.
        """

        return self._client.head_object(request, **kwargs)

    def initiate_multipart_upload(self, request: models.InitiateMultipartUploadRequest, **kwargs
                    ) -> models.InitiateMultipartUploadResult:
        """
        Initiates a multipart upload task before you can upload data in parts to Object Storage Service (OSS).

        Args:
            request (InitiateMultipartUploadRequest): Request parameters for InitiateMultipartUpload operation.

        Returns:
            InitiateMultipartUploadResult: Reponse result for InitiateMultipartUpload operation.
        """

        return self._initiate_multipart_upload_securely(request, **kwargs)

    def upload_part(self, request: models.UploadPartRequest, **kwargs
                    ) -> models.UploadPartResult:
        """
        Call the UploadPart interface to upload data in blocks (parts) based on the specified Object name and uploadId.

        Args:
            request (UploadPartRequest): Request parameters for UploadPart operation.

        Returns:
            UploadPartResult: Reponse result for UploadPart operation.
        """

        return self._upload_part_securely(request, **kwargs)

    def complete_multipart_upload(self, request: models.CompleteMultipartUploadRequest, **kwargs
                    ) -> models.CompleteMultipartUploadResult:
        """
        Completes the multipart upload task of an object after all parts of the object are uploaded.

        Args:
            request (CompleteMultipartUploadRequest): Request parameters for CompleteMultipartUpload operation.

        Returns:
            CompleteMultipartUploadResult: Reponse result for CompleteMultipartUpload operation.
        """

        return self._client.complete_multipart_upload(request, **kwargs)

    def abort_multipart_upload(self, request: models.AbortMultipartUploadRequest, **kwargs
                    ) -> models.AbortMultipartUploadResult:
        """
        Cancels a multipart upload task and deletes the parts uploaded in the task.

        Args:
            request (AbortMultipartUploadRequest): Request parameters for AbortMultipartUpload operation.

        Returns:
            AbortMultipartUploadResult: Reponse result for AbortMultipartUpload operation.
        """

        return self._client.abort_multipart_upload(request, **kwargs)

    def list_parts(self, request: models.ListPartsRequest, **kwargs
                    ) -> models.ListPartsResult:
        """
        Lists all parts that are uploaded by using a specified upload ID.

        Args:
            request (ListPartsRequest): Request parameters for ListParts operation.

        Returns:
            ListPartsResult: Reponse result for ListParts operation.
        """

        return self._client.list_parts(request, **kwargs)

    def _get_ccbuilder(self, envelope: Envelope ) -> ContentCipherBuilder:
        return self._ccbuilders.get(envelope.mat_desc or '', self._defualt_ccbuilder)


    def _put_object_securely(self, request: models.PutObjectRequest, **kwargs
                   ) -> models.PutObjectResult:

        cc = self._defualt_ccbuilder.content_cipher()
        body = cc.encrypt_content(request.body)
        erequest = copy.copy(request)
        erequest.body = body
        _add_crypto_header_putobject(erequest, cc.get_cipher_data())
        return self._client.put_object(erequest, **kwargs)

    def _get_object_securely(self, request: models.GetObjectRequest, **kwargs
                   ) -> models.GetObjectResult:

        adjust_range_start = 0
        discard_count = 0
        erequest = request
        if request.range_header is not None:
            http_range = utils.parse_http_range(request.range_header)
            adjust_range_start = _adjust_range_start(http_range[0])
            discard_count = http_range[0] - adjust_range_start

            if discard_count > 0:
                erequest = copy.copy(request)
                range_start = str(adjust_range_start) if adjust_range_start >= 0 else ''
                range_end = str(http_range[1]) if http_range[1] >= 0 else ''
                erequest.range_header = f'bytes={range_start}-{range_end}'
                erequest.range_behavior = 'standard'

        result = self._client.get_object(erequest, **kwargs)

        try:
            if _has_encrypted_header(result.headers):
                envelope = _get_envelope_from_header(result.headers)

                if not _is_valid_content_alg(envelope.cek_algorithm or ''):
                    raise exceptions.ParamInvalidError(field='envelope.cek_algorithm')

                if not envelope.is_valid():
                    raise exceptions.ParamInvalidError(field='envelope')

                cc = self._get_ccbuilder(envelope).content_cipher_from_env(envelope, offset=adjust_range_start)
                result.body = cast(StreamBody, cc.decrypt_content(result.body))

        except Exception as err:
            if result.body is not None:
                result.body.close()

            raise err

        if discard_count > 0:
            #rewrite ContentRange & ContentLength
            if result.content_range is not None:
                crange = utils.parse_content_range(result.content_range)
                value = f'bytes {crange[0] + discard_count}-{crange[1]}/{crange[2]}'
                result.content_range = value
                result.headers.update({"Content-Range": value})
            else:
                result.headers.update({"Content-Range": f'bytes {discard_count}-/*'})

            if result.content_length is not None:
                result.content_length -= discard_count
                result.headers.update({"Content-Length": str(result.content_length)})

            result.body = io_utils.StreamBodyDiscarder(result.body, discard_count)


        return result

    def _initiate_multipart_upload_securely(self, request: models.InitiateMultipartUploadRequest, **kwargs
                    ) -> models.InitiateMultipartUploadResult:

        _valid_encryption_context(request)
        erequest = copy.copy(request)

        cc = self._defualt_ccbuilder.content_cipher()
        _add_crypto_header_initpart(erequest, cc.get_cipher_data())

        result = self._client.initiate_multipart_upload(erequest, **kwargs)

        result.cse_multipart_context = EncryptionMultiPartContext(
            content_cipher=cc,
            part_size= utils.safety_int(request.cse_part_size),
            data_size= utils.safety_int(request.cse_data_size),
        )

        return result

    def _upload_part_securely(self, request: models.UploadPartRequest, **kwargs
                              ) -> models.UploadPartResult:

        cse_context = request.cse_multipart_context
        if cse_context is None:
            raise exceptions.ParamNullError(
                field='request.cse_multipart_context')

        if (not isinstance(cse_context, EncryptionMultiPartContext) or
                not request.cse_multipart_context.is_valid()):
            raise exceptions.ParamInvalidError(
                field='request.cse_multipart_context')

        if cse_context.part_size % _BLOCK_SIZE_LEN != 0:
            raise ValueError(f'EncryptionMultiPartContext.part_size must be aligned to {_BLOCK_SIZE_LEN}')

        offset = 0
        if request.part_number > 1:
            offset = (request.part_number - 1) * cse_context.part_size

        cc = cse_context.content_cipher.clone(offset=offset)

        erequest = copy.copy(request)
        erequest.body = cc.encrypt_content(request.body)
        _add_crypto_header_uploadpart(erequest, cse_context, cc.get_cipher_data())

        return self._client.upload_part(erequest, **kwargs)


def _add_crypto_common_header(headers: MutableMapping, cipher_data: CipherData) -> None:
    # mat desc
    if len(cipher_data.mat_desc) > 0:
        headers['x-oss-meta-client-side-encryption-matdesc'] = cipher_data.mat_desc

    # encrypted key
    value = base64.b64encode(cipher_data.encrypted_key)
    headers['x-oss-meta-client-side-encryption-key'] = value.decode()

    # encrypted iv
    value = base64.b64encode(cipher_data.encrypted_iv)
    headers['x-oss-meta-client-side-encryption-start'] = value.decode()

    # wrap alg
    headers['x-oss-meta-client-side-encryption-wrap-alg'] = cipher_data.wrap_algorithm

    # cek alg
    headers['x-oss-meta-client-side-encryption-cek-alg'] = cipher_data.cek_algorithm


def _add_crypto_header_putobject(request: models.PutObjectRequest, cipher_data: CipherData) -> None:
    headers = getattr(request, 'headers', None)
    if headers is None:
        headers = CaseInsensitiveDict()

    # convert content-md5
    if request.content_md5 is not None:
        headers['x-oss-meta-client-side-encryption-unencrypted-content-md5'] = request.content_md5
        request.content_md5 = None

    # convert content-length
    if request.content_length is not None:
        headers['x-oss-meta-client-side-encryption-unencrypted-content-length'] = str(request.content_length)
        request.content_length = None

    _add_crypto_common_header(headers, cipher_data)
    setattr(request, 'headers', headers)


def _add_crypto_header_initpart(request: models.InitiateMultipartUploadRequest, cipher_data: CipherData) -> None:
    headers = getattr(request, 'headers', None)
    if headers is None:
        headers = CaseInsensitiveDict()

    # data size
    if utils.safety_int(int(request.cse_data_size)) > 0:
        headers['x-oss-meta-client-side-encryption-data-size'] = str(request.cse_data_size)

    # part size
    headers['x-oss-meta-client-side-encryption-part-size'] = str(request.cse_part_size)

    _add_crypto_common_header(headers, cipher_data)

    setattr(request, 'headers', headers)

def _add_crypto_header_uploadpart(request: models.UploadPartRequest,
                                  cse_context: EncryptionMultiPartContext,
                                  cipher_data: CipherData) -> None:
    headers = getattr(request, 'headers', None)
    if headers is None:
        headers = CaseInsensitiveDict()

    # data size
    if utils.safety_int(int(cse_context.data_size)) > 0:
        headers['x-oss-meta-client-side-encryption-data-size'] = str(cse_context.data_size)

    # part size
    headers['x-oss-meta-client-side-encryption-part-size'] = str(cse_context.part_size)

    _add_crypto_common_header(headers, cipher_data)

    setattr(request, 'headers', headers)


def _has_encrypted_header(headers: MutableMapping[str, str]) -> bool:
    return len(headers.get("x-oss-meta-client-side-encryption-key", '')) > 0

def _get_envelope_from_header(headers: MutableMapping[str, str]) -> Envelope:
    env = Envelope()
    env.iv = base64.b64decode(headers.get("x-oss-meta-client-side-encryption-start", ''))
    env.cipher_key = base64.b64decode(headers.get("x-oss-meta-client-side-encryption-key", ''))
    env.mat_desc = headers.get("x-oss-meta-client-side-encryption-matdesc", '')
    env.cek_algorithm = headers.get("x-oss-meta-client-side-encryption-cek-alg", '')
    env.wrap_algorithm = headers.get("x-oss-meta-client-side-encryption-wrap-alg", '')
    env.unencrypted_md5 = headers.get("x-oss-meta-client-side-encryption-unencrypted-content-md5", '')
    env.unencrypted_content_length = headers.get("x-oss-meta-client-side-encryption-unencrypted-content-length", '')
    return env

def _get_envelope_from_list_parts(result: models.ListPartsResult) -> Envelope:
    env = Envelope()
    env.iv = base64.b64decode(utils.safety_str(result.client_encryption_start))
    env.cipher_key = base64.b64decode(utils.safety_str(result.client_encryption_key))
    env.cek_algorithm = utils.safety_str(result.client_encryption_cek_alg)
    env.wrap_algorithm = utils.safety_str(result.client_encryption_wrap_alg)
    env.mat_desc = ''
    return env

def _is_valid_content_alg(alg_name:str) -> bool:
    #now content encyrption only support aec/ctr algorithm
    return alg_name == 'AES/CTR/NoPadding'

def _adjust_range_start(start):
    return (start // _BLOCK_SIZE_LEN) * _BLOCK_SIZE_LEN

def _valid_encryption_context(request: models.InitiateMultipartUploadRequest) -> None:
    part_size = request.cse_part_size
    if part_size is None:
        raise exceptions.ParamNullError(field='request.cse_part_size')

    if not isinstance(part_size, int):
        raise TypeError(f'request.cse_part_size need int, but got {type(part_size)}')

    if part_size <= 0:
        raise exceptions.ParamInvalidError(field='request.cse_part_size')

    if not 0 == part_size % _BLOCK_SIZE_LEN:
        raise ValueError(f'request.CSEPartSize must aligned to the {_BLOCK_SIZE_LEN}')

    data_size = request.cse_data_size
    if data_size is not None and not isinstance(data_size, int):
        raise TypeError(f'request.cse_data_size need int, but got {type(data_size)}')

from typing import Optional, List, Any
from .. import serde


class CnameCertificate(serde.Model):
    """
    The information about the certificate.
    """

    _attribute_map = { 
        'fingerprint': {'tag': 'xml', 'rename': 'Fingerprint', 'type': 'str'},
        'valid_start_date': {'tag': 'xml', 'rename': 'ValidStartDate', 'type': 'str'},
        'valid_end_date': {'tag': 'xml', 'rename': 'ValidEndDate', 'type': 'str'},
        'type': {'tag': 'xml', 'rename': 'Type', 'type': 'str'},
        'cert_id': {'tag': 'xml', 'rename': 'CertId', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'creation_date': {'tag': 'xml', 'rename': 'CreationDate', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CnameCertificate'
    }

    def __init__(
        self,
        fingerprint: Optional[str] = None,
        valid_start_date: Optional[str] = None,
        valid_end_date: Optional[str] = None,
        type: Optional[str] = None,
        cert_id: Optional[str] = None,
        status: Optional[str] = None,
        creation_date: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            fingerprint (str, optional): The signature of the certificate.
            valid_start_date (str, optional): The time when the certificate takes effect.
            valid_end_date (str, optional): The time when the certificate expires.
            type (str, optional): The source of the certificate.Valid values:*   CAS            *   Upload
            cert_id (str, optional): The ID of the certificate.
            status (str, optional): The status of the certificate.Valid values:*   Enabled            *   Disabled
            creation_date (str, optional): The time when the certificate was bound.
        """
        super().__init__(**kwargs)
        self.fingerprint = fingerprint
        self.valid_start_date = valid_start_date
        self.valid_end_date = valid_end_date
        self.type = type
        self.cert_id = cert_id
        self.status = status
        self.creation_date = creation_date


class CnameToken(serde.Model):
    """
    The container that stores the CNAME token.
    """

    _attribute_map = { 
        'cname': {'tag': 'xml', 'rename': 'Cname', 'type': 'str'},
        'token': {'tag': 'xml', 'rename': 'Token', 'type': 'str'},
        'expire_time': {'tag': 'xml', 'rename': 'ExpireTime', 'type': 'str'},
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CnameToken'
    }

    def __init__(
        self,
        cname: Optional[str] = None,
        token: Optional[str] = None,
        expire_time: Optional[str] = None,
        bucket: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cname (str, optional): The name of the CNAME record that is mapped to the bucket.
            token (str, optional): The CNAME token that is returned by OSS.
            expire_time (str, optional): The time when the CNAME token expires.
            bucket (str, optional): The name of the bucket to which the CNAME record is mapped.
        """
        super().__init__(**kwargs)
        self.cname = cname
        self.token = token
        self.expire_time = expire_time
        self.bucket = bucket


class CertificateConfiguration(serde.Model):
    """
    The container for which the certificate is configured.
    """

    _attribute_map = { 
        'certificate': {'tag': 'xml', 'rename': 'Certificate', 'type': 'str'},
        'private_key': {'tag': 'xml', 'rename': 'PrivateKey', 'type': 'str'},
        'previous_cert_id': {'tag': 'xml', 'rename': 'PreviousCertId', 'type': 'str'},
        'force': {'tag': 'xml', 'rename': 'Force', 'type': 'bool'},
        'delete_certificate': {'tag': 'xml', 'rename': 'DeleteCertificate', 'type': 'bool'},
        'cert_id': {'tag': 'xml', 'rename': 'CertId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'CertificateConfiguration'
    }

    def __init__(
        self,
        certificate: Optional[str] = None,
        private_key: Optional[str] = None,
        previous_cert_id: Optional[str] = None,
        force: Optional[bool] = None,
        delete_certificate: Optional[bool] = None,
        cert_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            certificate (str, optional): The public key of the certificate.
            private_key (str, optional): The private key of the certificate.
            previous_cert_id (str, optional): The ID of the certificate. If the Force parameter is not set to true, the OSS server checks whether the value of the Force parameter matches the current certificate ID. If the value does not match the certificate ID, an error is returned.noticeIf you do not specify the PreviousCertId parameter when you bind a certificate, you must set the Force parameter to true./notice
            force (bool, optional): Specifies whether to overwrite the certificate. Valid values:- true: overwrites the certificate.- false: does not overwrite the certificate.
            delete_certificate (bool, optional): Specifies whether to delete the certificate. Valid values:- true: deletes the certificate.- false: does not delete the certificate.
            cert_id (str, optional): The ID of the certificate.
        """
        super().__init__(**kwargs)
        self.certificate = certificate
        self.private_key = private_key
        self.previous_cert_id = previous_cert_id
        self.force = force
        self.delete_certificate = delete_certificate
        self.cert_id = cert_id


class Cname(serde.Model):
    """
    The container that stores the CNAME information.
    """

    _attribute_map = {
        'domain': {'tag': 'xml', 'rename': 'Domain', 'type': 'str'},
        'certificate_configuration': {'tag': 'xml', 'rename': 'CertificateConfiguration', 'type': 'CertificateConfiguration'},
    }

    _xml_map = {
        'name': 'Cname'
    }

    _dependency_map = {
        'CertificateConfiguration': {'new': lambda: CertificateConfiguration()},
    }

    def __init__(
        self,
        domain: Optional[str] = None,
        certificate_configuration: Optional[CertificateConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            domain (str, optional): The custom domain name.
            certificate_configuration (CertificateConfiguration, optional): The container for which the certificate is configured.
        """
        super().__init__(**kwargs)
        self.domain = domain
        self.certificate_configuration = certificate_configuration


class BucketCnameConfiguration(serde.Model):
    """
    The container that stores the CNAME record.
    """

    _attribute_map = { 
        'cname': {'tag': 'xml', 'rename': 'Cname', 'type': 'Cname'},
    }

    _xml_map = {
        'name': 'BucketCnameConfiguration'
    }

    _dependency_map = { 
        'Cname': {'new': lambda: Cname()},
    }

    def __init__(
        self,
        cname: Optional[Cname] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cname (Cname, optional): The container that stores the CNAME information.
        """
        super().__init__(**kwargs)
        self.cname = cname


class CnameInfo(serde.Model):
    """
    The information about the CNAME records.
    """

    _attribute_map = { 
        'domain': {'tag': 'xml', 'rename': 'Domain', 'type': 'str'},
        'last_modified': {'tag': 'xml', 'rename': 'LastModified', 'type': 'str'},
        'status': {'tag': 'xml', 'rename': 'Status', 'type': 'str'},
        'certificate': {'tag': 'xml', 'rename': 'Certificate', 'type': 'CnameCertificate'},
    }

    _xml_map = {
        'name': 'CnameInfo'
    }

    _dependency_map = { 
        'CnameCertificate': {'new': lambda: CnameCertificate()},
    }

    def __init__(
        self,
        domain: Optional[str] = None,
        last_modified: Optional[str] = None,
        status: Optional[str] = None,
        certificate: Optional[CnameCertificate] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            domain (str, optional): The custom domain name.
            last_modified (str, optional): The time when the custom domain name was mapped.
            status (str, optional): The status of the domain name. Valid values:*   Enabled*   Disabled
            certificate (CnameCertificate, optional): The container in which the certificate information is stored.
        """
        super().__init__(**kwargs)
        self.domain = domain
        self.last_modified = last_modified
        self.status = status
        self.certificate = certificate


class PutCnameRequest(serde.RequestModel):
    """
    The request for the PutCname operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'bucket_cname_configuration': {'tag': 'input', 'position': 'body', 'rename': 'BucketCnameConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        bucket_cname_configuration: Optional[BucketCnameConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            bucket_cname_configuration (BucketCnameConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.bucket_cname_configuration = bucket_cname_configuration


class PutCnameResult(serde.ResultModel):
    """
    The request for the PutCname operation.
    """

class ListCnameRequest(serde.RequestModel):
    """
    The request for the ListCname operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class ListCnameResult(serde.ResultModel):
    """
    The request for the ListCname operation.
    """

    _attribute_map = { 
        'cnames': {'tag': 'xml', 'rename': 'Cname', 'type': '[CnameInfo],xml'},
        'bucket': {'tag': 'xml', 'rename': 'Bucket', 'type': 'str'},
        'owner': {'tag': 'xml', 'rename': 'Owner', 'type': 'str'},
    }

    _dependency_map = { 
        'CnameInfo': {'new': lambda: CnameInfo()},
    }

    def __init__(
        self,
        cnames: Optional[List[CnameInfo]] = None,
        bucket: Optional[str] = None,
        owner: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cnames (List[CnameInfo], optional): The container that is used to store the information about all CNAME records.
            bucket (str, optional): The name of the bucket to which the CNAME records you want to query are mapped.
            owner (str, optional): The name of the bucket owner.
        """
        super().__init__(**kwargs)
        self.cnames = cnames
        self.bucket = bucket
        self.owner = owner

class DeleteCnameRequest(serde.RequestModel):
    """
    The request for the DeleteCname operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'bucket_cname_configuration': {'tag': 'input', 'position': 'body', 'rename': 'BucketCnameConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        bucket_cname_configuration: Optional[BucketCnameConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            bucket_cname_configuration (BucketCnameConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.bucket_cname_configuration = bucket_cname_configuration


class DeleteCnameResult(serde.ResultModel):
    """
    The request for the DeleteCname operation.
    """

class GetCnameTokenRequest(serde.RequestModel):
    """
    The request for the GetCnameToken operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'cname': {'tag': 'input', 'position': 'query', 'rename': 'cname', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        cname: str = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            cname (str, required): The name of the CNAME record that is mapped to the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.cname = cname


class GetCnameTokenResult(serde.ResultModel):
    """
    The request for the GetCnameToken operation.
    """

    _attribute_map = { 
        'cname_token': {'tag': 'output', 'position': 'body', 'rename': 'CnameToken', 'type': 'CnameToken,xml'},
    }

    _dependency_map = { 
        'CnameToken': {'new': lambda: CnameToken()},
    }

    def __init__(
        self,
        cname_token: Optional[CnameToken] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cname_token (CnameToken, optional): The container in which the CNAME token is stored.
        """
        super().__init__(**kwargs)
        self.cname_token = cname_token

class CreateCnameTokenRequest(serde.RequestModel):
    """
    The request for the CreateCnameToken operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'bucket_cname_configuration': {'tag': 'input', 'position': 'body', 'rename': 'BucketCnameConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        bucket_cname_configuration: Optional[BucketCnameConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            bucket_cname_configuration (BucketCnameConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.bucket_cname_configuration = bucket_cname_configuration


class CreateCnameTokenResult(serde.ResultModel):
    """
    The request for the CreateCnameToken operation.
    """

    _attribute_map = { 
        'cname_token': {'tag': 'output', 'position': 'body', 'rename': 'CnameToken', 'type': 'CnameToken,xml'},
    }

    _dependency_map = { 
        'CnameToken': {'new': lambda: CnameToken()},
    }

    def __init__(
        self,
        cname_token: Optional[CnameToken] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            cname_token (CnameToken, optional): The container in which the CNAME token is stored.
        """
        super().__init__(**kwargs)
        self.cname_token = cname_token

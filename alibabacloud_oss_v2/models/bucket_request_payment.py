import datetime
from typing import Optional, List, Any, Union
from .. import serde


class RequestPaymentConfiguration(serde.Model):
    """
    Indicates the container for the payer.
    """

    _attribute_map = { 
        'payer': {'tag': 'xml', 'rename': 'Payer', 'type': 'str'},
    }

    _xml_map = {
        'name': 'RequestPaymentConfiguration'
    }

    def __init__(
        self,
        payer: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            payer (str, optional): Indicates who pays the download and request fees.
        """
        super().__init__(**kwargs)
        self.payer = payer




class PutBucketRequestPaymentRequest(serde.RequestModel):
    """
    The request for the PutBucketRequestPayment operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'request_payment_configuration': {'tag': 'input', 'position': 'body', 'rename': 'RequestPaymentConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        request_payment_configuration: Optional[RequestPaymentConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            request_payment_configuration (RequestPaymentConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.request_payment_configuration = request_payment_configuration


class PutBucketRequestPaymentResult(serde.ResultModel):
    """
    The request for the PutBucketRequestPayment operation.
    """

class GetBucketRequestPaymentRequest(serde.RequestModel):
    """
    The request for the GetBucketRequestPayment operation.
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


class GetBucketRequestPaymentResult(serde.ResultModel):
    """
    The request for the GetBucketRequestPayment operation.
    """

    _attribute_map = { 
        'request_payment_configuration': {'tag': 'output', 'position': 'body', 'rename': 'RequestPaymentConfiguration', 'type': 'RequestPaymentConfiguration,xml'},
    }

    _dependency_map = { 
        'RequestPaymentConfiguration': {'new': lambda: RequestPaymentConfiguration()},
    }

    def __init__(
        self,
        request_payment_configuration: Optional[RequestPaymentConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            request_payment_configuration (RequestPaymentConfiguration, optional): Indicates the container for the payer.
        """
        super().__init__(**kwargs)
        self.request_payment_configuration = request_payment_configuration

import argparse
from typing import Optional, Any, List
from requests.structures import CaseInsensitiveDict
from alibabacloud_oss_v2 import serde, OperationInput, serde_utils
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="invoke operation bucket tags sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')


class Tag(serde.Model):
    """The inforamtion about the tag."""

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
            key (str, optional): The key of the tag.
            value (str, optional): The value of the tag.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value

    _attribute_map = {
        "key": {"tag": "xml", "rename": "Key"},
        "value": {"tag": "xml", "rename": "Value"},
    }
    _xml_map = {
        "name": "Tag"
    }

class TagSet(serde.Model):
    """The collection of tags."""

    def __init__(
        self,
        tags: Optional[List[Tag]] = None,
        **kwargs: Any
    ) -> None:
        """
            tags ([Tag], optional): A list of tags.
        """
        super().__init__(**kwargs)
        self.tags = tags

    _attribute_map = {
        "tags": {"tag": "xml", "rename": "Tag", "type": "[Tag]"},
    }

    _dependency_map = {
        "Tag": {"new": lambda: Tag()},
    }

    _xml_map = {
        "name": "TagSet"
    }

class Tagging(serde.Model):
    """
    The container that stores the returned tags of the bucket. If no tags are configured for the bucket, an XML message body is returned in which the Tagging element is empty.
    """

    _attribute_map = {
        'tag_set': {'tag': 'xml', 'rename': 'TagSet', 'type': 'TagSet'},
    }

    _xml_map = {
        'name': 'Tagging'
    }

    _dependency_map = {
        'TagSet': {'new': lambda: TagSet()},
    }

    def __init__(
        self,
        tag_set: Optional[TagSet] = None,
        **kwargs: Any
    ) -> None:
        """
        tag_set (TagSet, optional): The container that stores the returned tags of the bucket.
        """
        super().__init__(**kwargs)
        self.tag_set = tag_set


class PutBucketTagsRequest(serde.RequestModel):
    """
    The request for the PutBucketTags operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'tagging': {'tag': 'input', 'position': 'body', 'rename': 'Tagging', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        tagging: Optional[Tagging] = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        tagging (Tagging, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.tagging = tagging


class PutBucketTagsResult(serde.ResultModel):
    """
    The request for the PutBucketTags operation.
    """

class GetBucketTagsRequest(serde.RequestModel):
    """
    The request for the GetBucketTags operation.
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
        bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketTagsResult(serde.ResultModel):
    """
    The request for the GetBucketTags operation.
    """

    _attribute_map = {
        'tagging': {'tag': 'output', 'position': 'body', 'rename': 'Tagging', 'type': 'Tagging,xml'},
    }

    _dependency_map = {
        'Tagging': {'new': lambda: Tagging()},
    }

    def __init__(
        self,
        tagging: Optional[Tagging] = None,
        **kwargs: Any
    ) -> None:
        """
        tagging (Tagging, optional): The container that stores the returned tags of the bucket. If no tags are configured for the bucket, an XML message body is returned in which the Tagging element is empty.
        """
        super().__init__(**kwargs)
        self.tagging = tagging

class DeleteBucketTagsRequest(serde.RequestModel):
    """
    The request for the DeleteBucketTags operation.
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
        bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketTagsResult(serde.ResultModel):
    """
    The request for the DeleteBucketTags operation.
    """



def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss.Client(cfg)

    # put bucket tags
    request = PutBucketTagsRequest(
            bucket=args.bucket,
            tagging=Tagging(
                tag_set=TagSet(
                    tags=[Tag(
                        key='test_key',
                        value='test_value',
                    ), Tag(
                        key='test_key2',
                        value='test_value2',
                    )],
                ),
            ),
    )

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='PutBucketTags',
            method='PUT',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'tagging': '',
            },
            bucket=args.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input)

    result = serde.deserialize_output(
        result=PutBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


    # get bucket tags
    request = GetBucketTagsRequest(
        bucket=args.bucket,
    )

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='GetBucketTags',
            method='GET',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'tagging': '',
            },
            bucket=args.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input)

    result = serde.deserialize_output(
        result=GetBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' key: {result.tagging.tag_set.tags[0].key},'
            f' value: {result.tagging.tag_set.tags[0].value},'
            f' key: {result.tagging.tag_set.tags[1].key},'
            f' value: {result.tagging.tag_set.tags[1].value},'
    )


    # delete bucket tags
    request = DeleteBucketTagsRequest(
        bucket=args.bucket,
    )

    op_input = serde.serialize_input(
        request=request,
        op_input=OperationInput(
            op_name='DeleteBucketTags',
            method='DELETE',
            headers=CaseInsensitiveDict({
                'Content-Type': 'application/xml',
            }),
            parameters={
                'tagging': '',
            },
            bucket=args.bucket,
            op_metadata={'sub-resource': ['tagging']},
        ),
        custom_serializer=[
            serde_utils.add_content_md5
        ]
    )

    op_output = client.invoke_operation(op_input)

    result = serde.deserialize_output(
        result=DeleteBucketTagsResult(),
        op_output=op_output,
        custom_deserializer=[
            serde.deserialize_output_xmlbody
        ],
    )

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()
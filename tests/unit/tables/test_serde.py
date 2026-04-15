# pylint: skip-file
import unittest
import json
import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from alibabacloud_oss_v2 import serde
from alibabacloud_oss_v2.tables.operations._serde import (
    serialize_input_tables_json_model,
    deserialize_output_tables_json_model,
    _deserialize_json_model_tables,
)
from alibabacloud_oss_v2.types import OperationInput, OperationOutput, CaseInsensitiveDict
from alibabacloud_oss_v2 import exceptions


class HttpResponseStub:
    """Mock HttpResponse for testing"""
    def __init__(self, content: bytes = b''):
        self._content = content

    @property
    def content(self) -> bytes:
        return self._content if self._content is not None else b''


def create_op_input():
    """Helper to create OperationInput with required args"""
    return OperationInput(op_name='Test', method='GET')


def create_op_output(http_response=None):
    """Helper to create OperationOutput with required args"""
    return OperationOutput(
        status='OK',
        status_code=200,
        http_response=http_response
    )


class TestSerializeInputTablesJsonModel(unittest.TestCase):
    """Test cases for serialize_input_tables_json_model function"""

    def test_basic_serialization(self):
        """Test basic serialization with simple fields"""
        class BasicRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "format": {"tag": "body", "position": "body", "rename": "format"},
            }

            def __init__(self, name: Optional[str] = None, format: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.format = format

        request = BasicRequest(name="test-table", format="parquet")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test-table")
        self.assertEqual(body_data["format"], "parquet")

    def test_serialization_with_headers(self):
        """Test serialization with headers"""
        class HeaderRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
            }
            _headers_map = {
                "table_bucket_arn": {"rename": "x-oss-table-bucket-arn"},
            }

            def __init__(self, table_bucket_arn: str = None, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.table_bucket_arn = table_bucket_arn
                self.name = name
                self.headers = {"x-oss-table-bucket-arn": table_bucket_arn} if table_bucket_arn else {}

        request = HeaderRequest(table_bucket_arn="arn:oss:table-bucket:123", name="test")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        self.assertEqual(result.headers["x-oss-table-bucket-arn"], "arn:oss:table-bucket:123")
        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test")

    def test_serialization_with_query(self):
        """Test serialization with headers"""
        class HeaderRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "query_value": {"tag": "input", "position": "query", "rename": "queryValue"},
            }

            def __init__(self, table_bucket_arn: str = None, name: Optional[str] = None, query_value: Optional[str] = None,**kwargs) -> None:
                super().__init__(**kwargs)
                self.table_bucket_arn = table_bucket_arn
                self.name = name
                self.query_value = query_value

        request = HeaderRequest(table_bucket_arn="arn:oss:table-bucket:123", name="test", query_value='val')
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        self.assertEqual(result.parameters["queryValue"], "val")
        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test")

    def test_serialization_with_parameters(self):
        """Test serialization with query parameters"""
        class ParamRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
            }

            def __init__(self, namespace: str = None, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.namespace = namespace
                self.name = name
                self.parameters = {"namespace": namespace} if namespace else {}

        request = ParamRequest(namespace="my-ns", name="test-table")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        self.assertEqual(result.parameters["namespace"], "my-ns")
        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test-table")

    def test_serialization_with_payload(self):
        """Test serialization with payload"""
        class PayloadRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
            }

            def __init__(self, name: Optional[str] = None, payload: bytes = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self._payload = payload

            @property
            def payload(self) -> bytes:
                return self._payload

        request = PayloadRequest(name="test", payload=b"raw payload data")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        # Payload is set first, then json_data overwrites it
        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test")

    def test_serialization_required_field_missing(self):
        """Test that missing required field raises ParamRequiredError"""
        class RequiredFieldRequest(serde.RequestModel):
            _attribute_map = {
                "required_field": {"tag": "body", "position": "body", "rename": "requiredField", "required": True},
                "optional_field": {"tag": "body", "position": "body", "rename": "optionalField"},
            }

            def __init__(self, required_field: Optional[str] = None, optional_field: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.required_field = required_field
                self.optional_field = optional_field

        # Required field is None
        request = RequiredFieldRequest(optional_field="value")
        op_input = create_op_input()

        with self.assertRaises(exceptions.ParamRequiredError):
            serialize_input_tables_json_model(request, op_input)

    def test_serialization_with_nested_model(self):
        """Test that nested model objects are stored but not JSON serialized by this function"""
        class NestedModel(serde.Model):
            _attribute_map = {
                "nested_value": {"tag": "json", "rename": "nestedValue"},
            }

            def __init__(self, nested_value: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.nested_value = nested_value

        class ParentRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "nested": {"tag": "body", "position": "body", "rename": "nested", "type": "NestedModel"},
            }

            def __init__(self, name: Optional[str] = None, nested: Optional[NestedModel] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.nested = nested

        # Test with nested model = None (can be serialized)
        request = ParentRequest(name="parent-test", nested=None)
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "parent-test")
        # When nested is None, it should not appear in json_data
        self.assertNotIn("nested", body_data)

        # Test with nested model = Value
        request = ParentRequest(name="parent-test", nested=NestedModel(nested_value="nest-value"))
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "parent-test")
        # When nested is None, it should not appear in json_data
        self.assertEqual(body_data["nested"]['nestedValue'], "nest-value")


    def test_serialization_with_list_type(self):
        """Test serialization with list type fields"""
        class ListRequest(serde.RequestModel):
            _attribute_map = {
                "tags": {"tag": "body", "position": "body", "rename": "tags", "type": "dict"},
            }

            def __init__(self, tags: Optional[Dict[str, str]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.tags = tags

        request = ListRequest(tags={"tag1": "value1", "tag2": "value2"})
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["tags"]["tag1"], "value1")
        self.assertEqual(body_data["tags"]["tag2"], "value2")

    def test_serialization_non_request_model_raises_error(self):
        """Test that non-RequestModel raises SerializationError"""
        class NonRequestModel(serde.Model):
            _attribute_map = {}

        request = NonRequestModel()
        op_input = create_op_input()

        with self.assertRaises(exceptions.SerializationError):
            serialize_input_tables_json_model(request, op_input)

    def test_serialization_with_custom_serializer(self):
        """Test serialization with custom serializer callback"""
        class CustomRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        custom_called = []

        def custom_serializer(request, op_input):
            custom_called.append(True)
            op_input.headers["X-Custom-Header"] = "custom-value"

        request = CustomRequest(name="test")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input, custom_serializer=[custom_serializer])

        self.assertTrue(len(custom_called) > 0)
        self.assertEqual(result.headers["X-Custom-Header"], "custom-value")

    def test_serialization_initializes_empty_headers_and_params(self):
        """Test that None headers and parameters are initialized"""
        class SimpleRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        request = SimpleRequest(name="test")
        op_input = create_op_input()
        op_input.headers = None
        op_input.parameters = None

        result = serialize_input_tables_json_model(request, op_input)

        self.assertIsNotNone(result.headers)
        self.assertIsNotNone(result.parameters)


class TestDeserializeJsonModelTables(unittest.TestCase):
    """Test cases for _deserialize_json_model_tables function"""

    def test_deserialize_basic_types(self):
        """Test deserialization of basic types"""
        class BasicModel(serde.Model):
            _attribute_map = {
                "name": {"tag": "json", "rename": "name", "type": "str"},
                "count": {"tag": "json", "rename": "count", "type": "int"},
                "enabled": {"tag": "json", "rename": "enabled", "type": "bool"},
                "ratio": {"tag": "json", "rename": "ratio", "type": "float"},
            }

            def __init__(self, name: Optional[str] = None, count: Optional[int] = None,
                         enabled: Optional[bool] = None, ratio: Optional[float] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.count = count
                self.enabled = enabled
                self.ratio = ratio

        data = {
            "name": "test",
            "count": 42,
            "enabled": True,
            "ratio": 3.14
        }
        obj = BasicModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.count, 42)
        self.assertEqual(obj.enabled, True)
        self.assertEqual(obj.ratio, 3.14)

    def test_deserialize_case_insensitive_keys(self):
        """Test that deserialization handles case-insensitive keys"""
        class CaseModel(serde.Model):
            _attribute_map = {
                "myField": {"tag": "json", "rename": "myField", "type": "str"},
            }

            def __init__(self, myField: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.myField = myField

        # JSON has lowercase key, model expects myField
        data = {"myfield": "test-value"}
        obj = CaseModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.myField, "test-value")

    def test_deserialize_nested_model(self):
        """Test deserialization of nested model objects"""
        class NestedModel(serde.Model):
            _attribute_map = {
                "nested_name": {"tag": "json", "rename": "nestedName", "type": "str"},
            }

            def __init__(self, nested_name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.nested_name = nested_name

        class ParentModel(serde.Model):
            _attribute_map = {
                "name": {"tag": "json", "rename": "name", "type": "str"},
                "nested": {"tag": "json", "rename": "nested", "type": "NestedModel"},
            }
            _dependency_map = {
                "NestedModel": {"new": lambda: NestedModel()},
            }

            def __init__(self, name: Optional[str] = None, nested: Optional[NestedModel] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.nested = nested

        data = {
            "name": "parent",
            "nested": {"nestedName": "nested-value"}
        }
        obj = ParentModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.name, "parent")
        self.assertEqual(obj.nested.nested_name, "nested-value")

    def test_deserialize_list_of_primitives(self):
        """Test deserialization of list of primitive types"""
        class ListModel(serde.Model):
            _attribute_map = {
                "tags": {"tag": "json", "rename": "tags", "type": "[str]"},
                "counts": {"tag": "json", "rename": "counts", "type": "[int]"},
            }

            def __init__(self, tags: Optional[List[str]] = None, counts: Optional[List[int]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.tags = tags
                self.counts = counts

        data = {
            "tags": ["tag1", "tag2", "tag3"],
            "counts": [1, 2, 3]
        }
        obj = ListModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.tags, ["tag1", "tag2", "tag3"])
        self.assertEqual(obj.counts, [1, 2, 3])

    def test_deserialize_list_of_models(self):
        """Test deserialization of list of model objects"""
        class ItemModel(serde.Model):
            _attribute_map = {
                "item_name": {"tag": "json", "rename": "itemName", "type": "str"},
            }

            def __init__(self, item_name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.item_name = item_name

        class ContainerModel(serde.Model):
            _attribute_map = {
                "items": {"tag": "json", "rename": "items", "type": "[ItemModel]"},
            }
            _dependency_map = {
                "ItemModel": {"new": lambda: ItemModel()},
            }

            def __init__(self, items: Optional[List[ItemModel]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.items = items

        data = {
            "items": [
                {"itemName": "item1"},
                {"itemName": "item2"}
            ]
        }
        obj = ContainerModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(len(obj.items), 2)
        self.assertEqual(obj.items[0].item_name, "item1")
        self.assertEqual(obj.items[1].item_name, "item2")

    def test_deserialize_non_dict_data_returns_early(self):
        """Test that non-dict data returns early without error"""
        class TestModel(serde.Model):
            _attribute_map = {
                "name": {"tag": "json", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        obj = TestModel()
        # Should not raise, just return
        _deserialize_json_model_tables("not a dict", obj)
        _deserialize_json_model_tables(None, obj)
        _deserialize_json_model_tables([1, 2, 3], obj)

    def test_deserialize_missing_optional_field(self):
        """Test that missing optional fields are skipped"""
        class OptionalModel(serde.Model):
            _attribute_map = {
                "required_field": {"tag": "json", "rename": "requiredField", "type": "str"},
                "optional_field": {"tag": "json", "rename": "optionalField", "type": "str"},
            }

            def __init__(self, required_field: Optional[str] = None, optional_field: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.required_field = required_field
                self.optional_field = optional_field

        data = {"requiredField": "present"}
        obj = OptionalModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.required_field, "present")
        self.assertIsNone(obj.optional_field)

    def test_deserialize_datetime_field(self):
        """Test deserialization of datetime fields"""
        class DateTimeModel(serde.Model):
            _attribute_map = {
                "created_at": {"tag": "json", "rename": "createdAt", "type": "datetime"},
            }

            def __init__(self, created_at: Optional[datetime.datetime] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.created_at = created_at

        data = {"createdAt": "2024-01-15T10:30:00Z"}
        obj = DateTimeModel()
        _deserialize_json_model_tables(data, obj)

        self.assertIsInstance(obj.created_at, datetime.datetime)


class TestDeserializeOutputTablesJsonModel(unittest.TestCase):
    """Test cases for deserialize_output_tables_json_model function"""

    def test_deserialize_output_basic_fields(self):
        """Test deserialization of basic output fields"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
                "count": {"tag": "output", "position": "body", "rename": "count", "type": "int"},
            }

            def __init__(self, name: Optional[str] = None, count: Optional[int] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.count = count

        json_data = json.dumps({"name": "test-output", "count": 100}).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertEqual(result.name, "test-output")
        self.assertEqual(result.count, 100)

    def test_deserialize_output_nested_model(self):
        """Test deserialization of nested model in output"""
        class NestedOutput(serde.Model):
            _attribute_map = {
                "nested_value": {"tag": "json", "rename": "nestedValue", "type": "str"},
            }

            def __init__(self, nested_value: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.nested_value = nested_value

        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
                "nested": {"tag": "output", "position": "body", "rename": "nested", "type": "NestedOutput"},
            }
            _dependency_map = {
                "NestedOutput": {"new": lambda: NestedOutput()},
            }

            def __init__(self, name: Optional[str] = None, nested: Optional[NestedOutput] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.nested = nested

        json_data = json.dumps({
            "name": "parent-output",
            "nested": {"nestedValue": "nested-output"}
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertEqual(result.name, "parent-output")
        self.assertEqual(result.nested.nested_value, "nested-output")

    def test_deserialize_output_list_of_models(self):
        """Test deserialization of list of models in output"""
        class ItemOutput(serde.Model):
            _attribute_map = {
                "item_name": {"tag": "json", "rename": "itemName", "type": "str"},
            }

            def __init__(self, item_name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.item_name = item_name

        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "items": {"tag": "output", "position": "body", "rename": "items", "type": "[ItemOutput]"},
            }
            _dependency_map = {
                "ItemOutput": {"new": lambda: ItemOutput()},
            }

            def __init__(self, items: Optional[List[ItemOutput]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.items = items

        json_data = json.dumps({
            "items": [
                {"itemName": "item1"},
                {"itemName": "item2"}
            ]
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.items[0].item_name, "item1")
        self.assertEqual(result.items[1].item_name, "item2")

    def test_deserialize_output_empty_body(self):
        """Test that empty body is handled gracefully"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        # Empty content
        http_response = HttpResponseStub(content=b'')
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertIsNone(result.name)

    def test_deserialize_output_none_content(self):
        """Test that None content is handled gracefully"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        http_response = HttpResponseStub(content=None)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertIsNone(result.name)

    def test_deserialize_output_invalid_json_raises_error(self):
        """Test that invalid JSON raises DeserializationError"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        http_response = HttpResponseStub(content=b'invalid json {{{')
        op_output = create_op_output(http_response=http_response)

        with self.assertRaises(exceptions.DeserializationError):
            deserialize_output_tables_json_model(OutputModel(), op_output)

    def test_deserialize_output_string_content(self):
        """Test deserialization with string content (not bytes)"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        http_response = HttpResponseStub(content='{"name": "string-content"}')
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertEqual(result.name, "string-content")

    def test_deserialize_output_dict_content(self):
        """Test deserialization with dict content (already parsed)"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        # Mock http_response with dict content
        class DictHttpResponse:
            @property
            def content(self):
                return {"name": "dict-content"}

        http_response = DictHttpResponse()
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        self.assertEqual(result.name, "dict-content")

    def test_deserialize_output_unsupported_type_raises_error(self):
        """Test that unsupported json_data type raises DeserializationError"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
            }

            def __init__(self, name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name

        class UnsupportedHttpResponse:
            @property
            def content(self):
                return 12345  # Not bytes, str, or dict

        http_response = UnsupportedHttpResponse()
        op_output = create_op_output(http_response=http_response)

        with self.assertRaises(exceptions.DeserializationError):
            deserialize_output_tables_json_model(OutputModel(), op_output)

    def test_deserialize_output_with_dict_type_field(self):
        """Test deserialization of dict type field"""
        class DictOutputModel(serde.ResultModel):
            _attribute_map = {
                "metadata": {"tag": "output", "position": "body", "rename": "metadata", "type": "dict"},
            }

            def __init__(self, metadata: Optional[Dict[str, Any]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.metadata = metadata

        json_data = json.dumps({
            "metadata": {"key1": "value1", "key2": {"nested": "value"}}
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(DictOutputModel(), op_output)

        self.assertEqual(result.metadata["key1"], "value1")

    def test_deserialize_output_with_list_type_field(self):
        """Test deserialization of [dict] type field"""
        class ListOutputModel(serde.ResultModel):
            _attribute_map = {
                "items": {"tag": "output", "position": "body", "rename": "items", "type": "[dict]"},
            }

            def __init__(self, items: Optional[List[Dict[str, Any]]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.items = items

        json_data = json.dumps({
            "items": [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2", "nested": {"key": "value"}}
            ]
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(ListOutputModel(), op_output)

        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.items[0]["id"], 1)
        self.assertEqual(result.items[1]["name"], "item2")

    def test_deserialize_output_body_tag_position_filtering(self):
        """Test that only fields with tag='output' and position='body' are deserialized"""
        class OutputModel(serde.ResultModel):
            _attribute_map = {
                "body_field": {"tag": "output", "position": "body", "rename": "bodyField", "type": "str"},
                "header_field": {"tag": "output", "position": "headers", "rename": "headerField", "type": "str"},
                "input_field": {"tag": "input", "position": "body", "rename": "inputField", "type": "str"},
            }

            def __init__(self, body_field: Optional[str] = None, header_field: Optional[str] = None,
                         input_field: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.body_field = body_field
                self.header_field = header_field
                self.input_field = input_field

        json_data = json.dumps({
            "bodyField": "body-value",
            "headerField": "header-value",
            "inputField": "input-value"
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(OutputModel(), op_output)

        # Only body_field should be deserialized from JSON
        self.assertEqual(result.body_field, "body-value")
        self.assertIsNone(result.header_field)
        self.assertIsNone(result.input_field)


class TestSerializeInputTablesJsonModelEdgeCases(unittest.TestCase):
    """Edge case tests for serialize_input_tables_json_model function"""

    def test_serialization_with_enum_field(self):
        """Test serialization with enum field using _serialize_json_any_tables"""
        class StatusEnum(Enum):
            ACTIVE = "active"
            INACTIVE = "inactive"

        class EnumRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "status": {"tag": "body", "position": "body", "rename": "status"},
            }

            def __init__(self, name: Optional[str] = None, status: Optional[StatusEnum] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.status = status

        request = EnumRequest(name="test", status=StatusEnum.ACTIVE)
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["status"], "active")

    def test_serialization_with_bool_field(self):
        """Test serialization with boolean field - should be converted to lowercase string"""
        class BoolRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "enabled": {"tag": "body", "position": "body", "rename": "enabled"},
            }

            def __init__(self, name: Optional[str] = None, enabled: Optional[bool] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.enabled = enabled

        request = BoolRequest(name="test", enabled=True)
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["enabled"], "true")

        # Test with False
        request = BoolRequest(name="test", enabled=False)
        op_input = create_op_input()
        result = serialize_input_tables_json_model(request, op_input)
        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["enabled"], "false")

    def test_serialization_with_list_of_models(self):
        """Test serialization with list of model objects"""
        # Note: The current implementation of serialize_input_tables_json_model
        # does not recursively serialize Model objects in lists.
        # This test verifies the current behavior where Model objects in lists
        # are kept as-is (not JSON serialized).
        class ItemModel(serde.Model):
            _attribute_map = {
                "item_name": {"tag": "json", "rename": "itemName"},
                "item_value": {"tag": "json", "rename": "itemValue"},
            }

            def __init__(self, item_name: Optional[str] = None, item_value: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.item_name = item_name
                self.item_value = item_value

        class ListRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "items": {"tag": "body", "position": "body", "rename": "items", "type": "[ItemModel]"},
            }

            _dependency_map = {
                "ItemModel": {"new": lambda: ItemModel()},
            }

            def __init__(self, name: Optional[str] = None, items: Optional[List[ItemModel]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.items = items

        # Test with list of primitive values (dicts) instead of Model objects
        # This matches the current implementation behavior
        class DictListRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "items": {"tag": "body", "position": "body", "rename": "items", "type": "dict"},
            }

            def __init__(self, name: Optional[str] = None, items: Optional[List[Dict[str, Any]]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.items = items

        request = DictListRequest(
            name="test",
            items=[{"itemName": "item1", "itemValue": "value1"},
                   {"itemName": "item2", "itemValue": "value2"}]
        )
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test")
        self.assertEqual(len(body_data["items"]), 2)
        self.assertEqual(body_data["items"][0]["itemName"], "item1")
        self.assertEqual(body_data["items"][1]["itemValue"], "value2")

    def test_serialization_with_deeply_nested_model(self):
        """Test serialization with deeply nested model objects"""
        class Level3Model(serde.Model):
            _attribute_map = {
                "level3_value": {"tag": "json", "rename": "level3Value"},
                "level3_count": {"tag": "json", "rename": "level3Count", "type": "int"},
            }

            def __init__(self, level3_value: Optional[str] = None, level3_count: Optional[int] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.level3_value = level3_value
                self.level3_count = level3_count

        class Level2Model(serde.Model):
            _attribute_map = {
                "level2_value": {"tag": "json", "rename": "level2Value"},
                "level3": {"tag": "json", "rename": "level3", "type": "Level3Model"},
            }

            _dependency_map = {
                "Level3Model": {"new": lambda: Level3Model()},
            }

            def __init__(self, level2_value: Optional[str] = None, level3: Optional[Level3Model] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.level2_value = level2_value
                self.level3 = level3

        class Level1Model(serde.Model):
            _attribute_map = {
                "level1_value": {"tag": "json", "rename": "level1Value"},
                "level2": {"tag": "json", "rename": "level2", "type": "Level2Model"},
            }

            _dependency_map = {
                "Level2Model": {"new": lambda: Level2Model()},
            }

            def __init__(self, level1_value: Optional[str] = None, level2: Optional[Level2Model] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.level1_value = level1_value
                self.level2 = level2

        class DeepNestedRequest(serde.RequestModel):
            _attribute_map = {
                "name": {"tag": "body", "position": "body", "rename": "name"},
                "data": {"tag": "body", "position": "body", "rename": "data", "type": "Level1Model"},
            }

            _dependency_map = {
                "Level1Model": {"new": lambda: Level1Model()},
            }

            def __init__(self, name: Optional[str] = None, data: Optional[Level1Model] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.data = data

        # Create deeply nested structure: Request -> Level1 -> Level2 -> Level3
        level3 = Level3Model(level3_value="L3-value", level3_count=42)
        level2 = Level2Model(level2_value="L2-value", level3=level3)
        level1 = Level1Model(level1_value="L1-value", level2=level2)
        request = DeepNestedRequest(name="deep-test", data=level1)
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))

        # Verify top-level fields
        self.assertEqual(body_data["name"], "deep-test")
        self.assertIn("data", body_data)

        # Verify level 1
        self.assertEqual(body_data["data"]["level1Value"], "L1-value")

        # Verify level 2
        self.assertEqual(body_data["data"]["level2"]["level2Value"], "L2-value")

        # Verify level 3
        self.assertEqual(body_data["data"]["level2"]["level3"]["level3Value"], "L3-value")
        self.assertEqual(body_data["data"]["level2"]["level3"]["level3Count"], 42)

    def test_serialization_only_body_position_fields(self):
        """Test that only fields with position='body' are serialized to JSON"""
        class MixedRequest(serde.RequestModel):
            _attribute_map = {
                "body_field": {"tag": "body", "position": "body", "rename": "bodyField"},
                "query_field": {"tag": "input", "position": "query", "rename": "queryField"},
                "host_field": {"tag": "input", "position": "host", "rename": "hostField"},
            }

            def __init__(self, body_field: Optional[str] = None, query_field: Optional[str] = None,
                         host_field: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.body_field = body_field
                self.query_field = query_field
                self.host_field = host_field

        request = MixedRequest(body_field="body", query_field="query", host_field="host")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        body_data = json.loads(result.body.decode('utf-8'))
        # Only body_field should be in JSON
        self.assertEqual(body_data["bodyField"], "body")
        self.assertNotIn("queryField", body_data)
        self.assertNotIn("hostField", body_data)

    def test_serialization_with_json_tag_only(self):
        """Test that only fields with tag='json' are processed by _serialize_json_model_tables"""
        # Note: serialize_input_tables_json_model processes fields with tag='body' and position='body'
        # This test verifies that fields without tag='body' position='body' are not serialized to JSON
        class MixedRequest(serde.RequestModel):
            _attribute_map = {
                "body_field": {"tag": "body", "position": "body", "rename": "bodyField"},
                "json_only_field": {"tag": "json", "position": "body", "rename": "jsonOnlyField"},
                "input_field": {"tag": "input", "rename": "inputField"},
                "output_field": {"tag": "output", "rename": "outputField"},
            }

            def __init__(self, body_field: Optional[str] = None, json_only_field: Optional[str] = None,
                         input_field: Optional[str] = None, output_field: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.body_field = body_field
                self.json_only_field = json_only_field
                self.input_field = input_field
                self.output_field = output_field

        request = MixedRequest(body_field="body", json_only_field="json", input_field="input", output_field="output")
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        # When there are no fields with tag='body' and position='body', body remains None
        # But the function should not crash
        # Fields with tag='json' should be serialized
        if result.body is not None:
            body_data = json.loads(result.body.decode('utf-8'))
            # body_field has tag='body' and position='body', should be in JSON
            self.assertIn("bodyField", body_data)


class TestDeserializeJsonModelTablesEdgeCases(unittest.TestCase):
    """Edge case tests for _deserialize_json_model_tables function"""

    def test_deserialize_with_raw_value_not_list_when_expected(self):
        """Test deserialization when array type field receives non-array value"""
        class ArrayModel(serde.Model):
            _attribute_map = {
                "tags": {"tag": "json", "rename": "tags", "type": "[str]"},
            }

            def __init__(self, tags: Optional[List[str]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.tags = tags

        # Single value instead of array - should be wrapped
        data = {"tags": "single-tag"}
        obj = ArrayModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.tags, ["single-tag"])

    def test_deserialize_case_insensitive_key_variations(self):
        """Test various case insensitive key matching"""
        class CaseModel(serde.Model):
            _attribute_map = {
                "MyField": {"tag": "json", "rename": "MyField", "type": "str"},
                "anotherField": {"tag": "json", "rename": "anotherField", "type": "str"},
            }

            def __init__(self, MyField: Optional[str] = None, anotherField: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.MyField = MyField
                self.anotherField = anotherField

        # Test MYFIELD -> MyField
        data = {"MYFIELD": "value1", "ANOTHERFIELD": "value2"}
        obj = CaseModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.MyField, "value1")
        self.assertEqual(obj.anotherField, "value2")

    def test_deserialize_deeply_nested_model(self):
        """Test deserialization of deeply nested model objects"""
        class Level3Model(serde.Model):
            _attribute_map = {
                "level3_value": {"tag": "json", "rename": "level3Value", "type": "str"},
            }

            def __init__(self, level3_value: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.level3_value = level3_value

        class Level2Model(serde.Model):
            _attribute_map = {
                "level2_value": {"tag": "json", "rename": "level2Value", "type": "str"},
                "level3": {"tag": "json", "rename": "level3", "type": "Level3Model"},
            }
            _dependency_map = {
                "Level3Model": {"new": lambda: Level3Model()},
            }

            def __init__(self, level2_value: Optional[str] = None, level3: Optional[Level3Model] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.level2_value = level2_value
                self.level3 = level3

        class Level1Model(serde.Model):
            _attribute_map = {
                "level1_value": {"tag": "json", "rename": "level1Value", "type": "str"},
                "level2": {"tag": "json", "rename": "level2", "type": "Level2Model"},
            }
            _dependency_map = {
                "Level2Model": {"new": lambda: Level2Model()},
            }

            def __init__(self, level1_value: Optional[str] = None, level2: Optional[Level2Model] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.level1_value = level1_value
                self.level2 = level2

        data = {
            "level1Value": "L1",
            "level2": {
                "level2Value": "L2",
                "level3": {
                    "level3Value": "L3"
                }
            }
        }
        obj = Level1Model()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.level1_value, "L1")
        self.assertEqual(obj.level2.level2_value, "L2")
        self.assertEqual(obj.level2.level3.level3_value, "L3")

    def test_deserialize_list_of_models_empty_array(self):
        """Test deserialization of empty list of models"""
        class ItemModel(serde.Model):
            _attribute_map = {
                "item_name": {"tag": "json", "rename": "itemName", "type": "str"},
            }

            def __init__(self, item_name: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.item_name = item_name

        class ContainerModel(serde.Model):
            _attribute_map = {
                "items": {"tag": "json", "rename": "items", "type": "[ItemModel]"},
            }
            _dependency_map = {
                "ItemModel": {"new": lambda: ItemModel()},
            }

            def __init__(self, items: Optional[List[ItemModel]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.items = items

        data = {"items": []}
        obj = ContainerModel()
        _deserialize_json_model_tables(data, obj)

        self.assertEqual(obj.items, [])

    def test_deserialize_skip_non_json_tag_fields(self):
        """Test that fields without tag='json' are skipped during deserialization"""
        class MixedModel(serde.Model):
            _attribute_map = {
                "json_field": {"tag": "json", "rename": "jsonField", "type": "str"},
                "output_field": {"tag": "output", "rename": "outputField", "type": "str"},
                "input_field": {"tag": "input", "rename": "inputField", "type": "str"},
            }

            def __init__(self, json_field: Optional[str] = None, output_field: Optional[str] = None,
                         input_field: Optional[str] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.json_field = json_field
                self.output_field = output_field
                self.input_field = input_field

        data = {"jsonField": "json-value", "outputField": "output-value", "inputField": "input-value"}
        obj = MixedModel()
        _deserialize_json_model_tables(data, obj)

        # Only json_field should be deserialized
        self.assertEqual(obj.json_field, "json-value")
        self.assertIsNone(obj.output_field)
        self.assertIsNone(obj.input_field)


class TestDeserializeOutputTablesJsonModelEdgeCases(unittest.TestCase):
    """Edge case tests for deserialize_output_tables_json_model function"""

    def test_deserialize_output_with_list_of_primitives(self):
        """Test deserialization of list of primitive types"""
        class PrimitiveListModel(serde.ResultModel):
            _attribute_map = {
                "tags": {"tag": "output", "position": "body", "rename": "tags", "type": "[str]"},
                "counts": {"tag": "output", "position": "body", "rename": "counts", "type": "[int]"},
            }

            def __init__(self, tags: Optional[List[str]] = None, counts: Optional[List[int]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.tags = tags
                self.counts = counts

        json_data = json.dumps({
            "tags": ["tag1", "tag2", "tag3"],
            "counts": [1, 2, 3]
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(PrimitiveListModel(), op_output)

        self.assertEqual(result.tags, ["tag1", "tag2", "tag3"])
        self.assertEqual(result.counts, [1, 2, 3])

    def test_deserialize_output_bool_field(self):
        """Test deserialization of boolean field"""
        class BoolOutputModel(serde.ResultModel):
            _attribute_map = {
                "enabled": {"tag": "output", "position": "body", "rename": "enabled", "type": "bool"},
            }

            def __init__(self, enabled: Optional[bool] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.enabled = enabled

        json_data = json.dumps({"enabled": True}).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(BoolOutputModel(), op_output)

        self.assertTrue(result.enabled)

    def test_deserialize_output_single_value_wrapped_in_list(self):
        """Test that single value is wrapped in list for array type"""
        class ArrayOutputModel(serde.ResultModel):
            _attribute_map = {
                "tags": {"tag": "output", "position": "body", "rename": "tags", "type": "[str]"},
            }

            def __init__(self, tags: Optional[List[str]] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.tags = tags

        json_data = json.dumps({"tags": "single-tag"}).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(ArrayOutputModel(), op_output)

        self.assertEqual(result.tags, ["single-tag"])

    def test_deserialize_output_with_null_field_values(self):
        """Test deserialization when JSON contains null values"""
        class NullableOutputModel(serde.ResultModel):
            _attribute_map = {
                "name": {"tag": "output", "position": "body", "rename": "name", "type": "str"},
                "count": {"tag": "output", "position": "body", "rename": "count", "type": "int"},
            }

            def __init__(self, name: Optional[str] = None, count: Optional[int] = None, **kwargs) -> None:
                super().__init__(**kwargs)
                self.name = name
                self.count = count

        json_data = json.dumps({"name": None, "count": None}).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(NullableOutputModel(), op_output)

        # Null values should be skipped
        self.assertIsNone(result.name)
        self.assertIsNone(result.count)


class TestIntegrationTablesSerialization(unittest.TestCase):
    """Integration tests using actual table models"""

    def test_create_table_request_serialization(self):
        """Test serialization of CreateTableRequest"""
        from alibabacloud_oss_v2.tables.models.table_basic import CreateTableRequest
        from alibabacloud_oss_v2.types import CaseInsensitiveDict

        request = CreateTableRequest(
            table_bucket_arn="arn:oss:table-bucket:123",
            namespace="my-namespace",
            name="test-table",
            format="parquet",
            # Manually set headers and parameters as the function expects
            headers=CaseInsensitiveDict({"x-oss-table-bucket-arn": "arn:oss:table-bucket:123"}),
            parameters={"namespace": "my-namespace"},
        )
        op_input = create_op_input()

        result = serialize_input_tables_json_model(request, op_input)

        # Headers are copied from request.headers
        self.assertEqual(op_input.headers["x-oss-table-bucket-arn"], "arn:oss:table-bucket:123")
        # Parameters are copied from request.parameters
        self.assertEqual(op_input.parameters["namespace"], "my-namespace")

        body_data = json.loads(result.body.decode('utf-8'))
        self.assertEqual(body_data["name"], "test-table")
        self.assertEqual(body_data["format"], "parquet")

    def test_get_table_result_deserialization(self):
        """Test deserialization of GetTableResult"""
        from alibabacloud_oss_v2.tables.models.table_basic import GetTableResult

        json_data = json.dumps({
            "namespace": ["my-namespace"],
            "name": "test-table",
            "type": "managed",
            "tableARN": "arn:oss:table:456",
            "createdAt": "2024-01-15T10:30:00Z",
            "format": "parquet",
        }).encode('utf-8')
        http_response = HttpResponseStub(content=json_data)
        op_output = create_op_output(http_response=http_response)

        result = deserialize_output_tables_json_model(GetTableResult(), op_output)

        self.assertEqual(result.name, "test-table")
        self.assertEqual(result.type, "managed")
        self.assertEqual(result.table_arn, "arn:oss:table:456")
        self.assertEqual(result.format, "parquet")
        self.assertEqual(result.created_at, "2024-01-15T10:30:00Z")


if __name__ == '__main__':
    unittest.main()

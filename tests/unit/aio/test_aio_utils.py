# pylint: skip-file
import unittest
from alibabacloud_oss_v2.aio.aio_utils import AsyncStreamBodyReader
from alibabacloud_oss_v2.exceptions import ResponseNotReadError
from .. import MockAsyncHttpResponse


class TestAsyncStreamBodyReader(unittest.IsolatedAsyncioTestCase):
    async def test_async_context_manager(self):
        response = MockAsyncHttpResponse(
            status_code=200,
            body=b'hello world',
        )
        async with AsyncStreamBodyReader(response) as reader:
            self.assertFalse(reader.is_closed)
            self.assertEqual(b'hello world', await reader.read())

        self.assertTrue(reader.is_closed)
        self.assertTrue(response.is_closed)

    async def test_read(self):
        reader = AsyncStreamBodyReader(MockAsyncHttpResponse(
            status_code=200,
            body=b'hello world',
        ))

        try:
            _ = reader.content
            self.fail('should not here')
        except ResponseNotReadError:
            pass

        self.assertEqual(b'hello world', await reader.read())
        self.assertTrue(reader.is_stream_consumed)
        self.assertEqual(b'hello world', reader.content)

        await reader.close()
        self.assertTrue(reader.is_closed)


if __name__ == '__main__':
    unittest.main()

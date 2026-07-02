# pylint: skip-file
import sys
import subprocess
import unittest


def _run_snippet(snippet: str) -> subprocess.CompletedProcess:
    """Run a python snippet in a fresh interpreter so import state is clean."""
    return subprocess.run(
        [sys.executable, "-c", snippet],
        capture_output=True,
        text=True,
    )


class TestNoCrcmod(unittest.TestCase):
    def test_sdk_usable_without_crcmod_installed(self):
        # Simulate a missing crcmod: block its import, then exercise the common
        # code paths (import SDK, build client + request, import operations) and
        # assert that crcmod stays unloaded and nothing raises ImportError.
        snippet = (
            "import builtins\n"
            "import sys\n"
            "_real_import = builtins.__import__\n"
            "def _blocked_import(name, *args, **kwargs):\n"
            "    if name == 'crcmod' or name.startswith('crcmod.'):\n"
            "        raise ImportError('crcmod is blocked for test')\n"
            "    return _real_import(name, *args, **kwargs)\n"
            "builtins.__import__ = _blocked_import\n"
            "import alibabacloud_oss_v2 as oss\n"
            "assert 'crcmod' not in sys.modules, 'crcmod was imported at package load'\n"
            "cfg = oss.config.load_default()\n"
            "cfg.region = 'cn-hangzhou'\n"
            "cfg.credentials_provider = oss.credentials.StaticCredentialsProvider('ak', 'sk')\n"
            "cfg.disable_upload_crc64_check = True\n"
            "cfg.disable_download_crc64_check = True\n"
            "client = oss.Client(cfg)\n"
            "req = oss.PutObjectRequest(bucket='b', key='k', body=b'123456789')\n"
            "from alibabacloud_oss_v2.operations import select_object\n"
            "assert 'crcmod' not in sys.modules, 'crcmod got imported without being needed'\n"
            "print('OK')\n"
        )
        proc = _run_snippet(snippet)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_put_object_crc_disabled_without_crcmod(self):
        # With crcmod blocked and upload crc check disabled, a full put_object
        # (over a mocked transport) must succeed and never touch crcmod. If the
        # disabled path wrongly reached crc code, the blocked import would raise.
        snippet = (
            "import builtins\n"
            "import sys\n"
            "_real_import = builtins.__import__\n"
            "def _blocked_import(name, *args, **kwargs):\n"
            "    if name == 'crcmod' or name.startswith('crcmod.'):\n"
            "        raise ImportError('crcmod is blocked for test')\n"
            "    return _real_import(name, *args, **kwargs)\n"
            "builtins.__import__ = _blocked_import\n"
            "from unittest import mock\n"
            "import alibabacloud_oss_v2 as oss\n"
            "from tests.unit import MockHttpResponse\n"
            "cfg = oss.config.Config(\n"
            "    region='cn-hangzhou',\n"
            "    credentials_provider=oss.credentials.AnonymousCredentialsProvider(),\n"
            "    disable_upload_crc64_check=True,\n"
            "    disable_download_crc64_check=True,\n"
            ")\n"
            "client = oss.Client(cfg)\n"
            "def _send(request, **kwargs):\n"
            "    return MockHttpResponse(status_code=200, reason='OK',\n"
            "        headers={'x-oss-request-id': 'id-1234', 'x-oss-hash-crc64ecma': '123'}, body='')\n"
            "with mock.patch.object(client._client._options.http_client, 'send', new=_send):\n"
            "    result = client.put_object(oss.PutObjectRequest(bucket='bucket', key='key', body='hello world'))\n"
            "assert result.status_code == 200, result.status_code\n"
            "assert result.hash_crc64 == '123', result.hash_crc64\n"
            "assert 'crcmod' not in sys.modules, 'crcmod loaded on disabled crc path'\n"
            "print('OK')\n"
        )
        proc = _run_snippet(snippet)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_crc_enabled_path_lazily_loads_crcmod(self):
        # When crc checking is actually exercised, crcmod is loaded lazily and
        # computes the expected value. Skip if crcmod is not installed locally.
        try:
            import crcmod  # noqa: F401
        except ImportError:
            self.skipTest("crcmod not installed")

        snippet = (
            "import sys\n"
            "import alibabacloud_oss_v2 as oss\n"
            "from alibabacloud_oss_v2 import crc\n"
            "c = crc.Crc64(0)\n"
            "c.update(b'123456789')\n"
            "assert c.sum64() == 11051210869376104954, c.sum64()\n"
            "assert 'crcmod' in sys.modules\n"
            "print('OK')\n"
        )
        proc = _run_snippet(snippet)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()

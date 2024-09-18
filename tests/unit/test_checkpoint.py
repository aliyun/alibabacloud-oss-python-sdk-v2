# pylint: skip-file
import os
import json
import unittest
from alibabacloud_oss_v2.types import CaseInsensitiveDict
from alibabacloud_oss_v2 import checkpoint
from alibabacloud_oss_v2 import models
from alibabacloud_oss_v2 import defaults
from alibabacloud_oss_v2 import utils

def _remove_slice(filename):
    try:
        os.remove(filename)
    except (OSError, ValueError):
        pass

def _write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)    

class TestCheckpoint(unittest.TestCase):
    def test_download_checkpoint(self):
        request = models.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        dest_filepath = "download-file-no-surfix"
        cpdir = "."

        headers = CaseInsensitiveDict({
            "Etag": "\"D41D8CD98F00B204E9800998ECF8****\"",
            "Content-Length": "344606",
            "Last-Modified": "Fri, 24 Feb 2012 06:07:48 GMT",
        })
        part_size = defaults.DEFAULT_DOWNLOAD_PART_SIZE
        cp = checkpoint.DownloadCheckpoint(request, dest_filepath, cpdir, headers, part_size)
        self.assertIsNotNone(cp)
        self.assertEqual("\"D41D8CD98F00B204E9800998ECF8****\"", cp.cp_info["Data"]["ObjectMeta"]["ETag"])
        self.assertEqual("Fri, 24 Feb 2012 06:07:48 GMT", cp.cp_info["Data"]["ObjectMeta"]["LastModified"])
        self.assertEqual(344606, cp.cp_info["Data"]["ObjectMeta"]["Size"])

        self.assertEqual("oss://bucket/key", cp.cp_info["Data"]["ObjectInfo"]["Name"])
        self.assertEqual("", cp.cp_info["Data"]["ObjectInfo"]["VersionId"])
        self.assertEqual("", cp.cp_info["Data"]["ObjectInfo"]["Range"])
 
        self.assertEqual(defaults.CHECKPOINT_MAGIC, cp.cp_info["Magic"])
        self.assertEqual(None, cp.cp_info.get("MD5", None))

        self.assertEqual(dest_filepath, cp.cp_info["Data"]["FilePath"])
        self.assertEqual(defaults.DEFAULT_DOWNLOAD_PART_SIZE, cp.cp_info["Data"]["PartSize"])

	    #has version id
        request = models.GetObjectRequest(
            bucket='bucket',
            key='key',
            version_id='id'
        )
        cp_vid = checkpoint.DownloadCheckpoint(request, dest_filepath, cpdir, headers, part_size)
        self.assertEqual("oss://bucket/key", cp_vid.cp_info["Data"]["ObjectInfo"]["Name"])
        self.assertEqual("id", cp_vid.cp_info["Data"]["ObjectInfo"]["VersionId"])
        self.assertEqual("", cp_vid.cp_info["Data"]["ObjectInfo"]["Range"])

    	#has range
        request = models.GetObjectRequest(
            bucket='bucket',
            key='key',
            version_id='id',
            range_header='bytes=1-10'
        )
        cp_range = checkpoint.DownloadCheckpoint(request, dest_filepath, cpdir, headers, part_size)
        self.assertEqual("oss://bucket/key", cp_range.cp_info["Data"]["ObjectInfo"]["Name"])
        self.assertEqual("id", cp_range.cp_info["Data"]["ObjectInfo"]["VersionId"])
        self.assertEqual("bytes=1-10", cp_range.cp_info["Data"]["ObjectInfo"]["Range"])

        #with other destFilePath
        dest_filepath1 = dest_filepath + "-123"
        cp_range_dest = checkpoint.DownloadCheckpoint(request, dest_filepath1, cpdir, headers, part_size)
        self.assertEqual(dest_filepath1, cp_range_dest.cp_info["Data"]["FilePath"])
        self.assertNotEqual(cp_range.cp_filepath, cp_range_dest.cp_filepath)

        #check dump
        cp.dump()
        self.assertTrue(os.path.isfile(cp.cp_filepath))
        content = b''
        with open(cp.cp_filepath, 'rb') as f:
            content = f.read()
        self.assertTrue(len(content) > 0)
        info = json.loads(content)

        self.assertEqual("\"D41D8CD98F00B204E9800998ECF8****\"", info["Data"]["ObjectMeta"]["ETag"])
        self.assertEqual("Fri, 24 Feb 2012 06:07:48 GMT", info["Data"]["ObjectMeta"]["LastModified"])
        self.assertEqual(344606, info["Data"]["ObjectMeta"]["Size"])

        self.assertEqual("oss://bucket/key", info["Data"]["ObjectInfo"]["Name"])
        self.assertEqual("", info["Data"]["ObjectInfo"]["VersionId"])
        self.assertEqual("", info["Data"]["ObjectInfo"]["Range"])

        self.assertEqual(defaults.CHECKPOINT_MAGIC, info["Magic"])
        self.assertEqual(32, len(info["MD5"]))

        self.assertEqual(dest_filepath, info["Data"]["FilePath"])
        self.assertEqual(part_size, info["Data"]["PartSize"])

    	#check load
        cp.load()
        self.assertEqual(True, cp.loaded)

        #check valid
        self.assertEqual(True, cp._is_valid())

        #check complete
        self.assertEqual(True, os.path.isfile(cp.cp_filepath))
        cp.remove()
        self.assertEqual(False, os.path.exists(cp.cp_filepath))

        #load not match
        cp = checkpoint.DownloadCheckpoint(request, dest_filepath, cpdir, headers, part_size)
        self.assertEqual(False, cp.loaded)
        not_match = '{"Magic":"92611BED-89E2-46B6-89E5-72F273D4B0A3","MD5":"2f132b5bf65640868a47cb52c57492c8","Data":{"ObjectInfo":{"Name":"oss://bucket/key","VersionId":"","Range":""},"ObjectMeta":{"Size":344606,"LastModified":"Fri, 24 Feb 2012 06:07:48 GMT","ETag":"D41D8CD98F00B204E9800998ECF8****"},"FilePath":"gthnjXGQ-no-surfix","PartSize":5242880,"DownloadInfo":{"Offset":5242880,"CRC64":0}}}'
        with open(cp.cp_filepath, 'wb') as f:
            f.write(not_match.encode())
        self.assertEqual(True, os.path.isfile(cp.cp_filepath))
        cp.load()
        self.assertEqual(False, cp.loaded)
        self.assertEqual(False, os.path.exists(cp.cp_filepath))


    def test_download_checkpoint_invalid_cppath(self):
        request = models.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        dest_filepath = "checkpoint_invalid_cppath-no-surfix"
        cpdir = "./invliad-dir/"

        headers = CaseInsensitiveDict({
            "Etag": "\"D41D8CD98F00B204E9800998ECF8****\"",
            "Content-Length": "344606",
            "Last-Modified": "Fri, 24 Feb 2012 06:07:48 GMT",
        })
        part_size = defaults.DEFAULT_DOWNLOAD_PART_SIZE
        cp = checkpoint.DownloadCheckpoint(request, dest_filepath, cpdir, headers, part_size)

        self.assertIsNotNone(cp)
        self.assertEqual(dest_filepath, cp.cp_info["Data"]["FilePath"])
        self.assertEqual("./invliad-dir", cp.cp_dirpath)
        self.assertIn("invliad-dir", cp.cp_filepath)

        #dump fail
        done = cp.dump()
        self.assertFalse(done)

        #load fail
        try:
            cp.load()
            self.fail("should not here")
        except Exception as err:
            self.assertIn("Invaid checkpoint dir", str(err))

    def test_download_checkpoint_valid(self):
        request = models.GetObjectRequest(
            bucket='bucket',
            key='key'
        )

        dest_filepath = "gthnjXGQ-no-surfix"
        cpdir = "."

        headers = CaseInsensitiveDict({
            "Etag": "\"D41D8CD98F00B204E9800998ECF8****\"",
            "Content-Length": "344606",
            "Last-Modified": "Fri, 24 Feb 2012 06:07:48 GMT",
        })

        part_size = 5 * 1024 *1024
        cp = checkpoint.DownloadCheckpoint(request, dest_filepath, cpdir, headers, part_size)

        _remove_slice(dest_filepath)
        self.assertEqual(0, cp.doffset)
        #cpdata = '{"Magic":"92611BED-89E2-46B6-89E5-72F273D4B0A3","MD5":"cc615a3b3fca2766786669a68895f3ed","Data":{"ObjectInfo":{"Name":"oss://bucket/key","VersionId":"","Range":""},"ObjectMeta":{"Size":344606,"LastModified":"Fri, 24 Feb 2012 06:07:48 GMT","ETag":"\\"D41D8CD98F00B204E9800998ECF8****\\""},"FilePath":"gthnjXGQ-no-surfix","PartSize":5242880,"DownloadInfo":{"Offset":5242880,"CRC64":0}}}'
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "cc615a3b3fca2766786669a68895f3ed", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 5242880, "DownloadInfo": {"Offset": 5242880, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertTrue(cp._is_valid())
        self.assertEqual(5242880, cp.doffset)

        #md5 fail
        cpdata = '{"Magic":"92611BED-89E2-46B6-89E5-72F273D4B0A3","MD5":"4f132b5bf65640868a47cb52c57492c8","Data":{"ObjectInfo":{"Name":"oss://bucket/key","VersionId":"","Range":""},"ObjectMeta":{"Size":344606,"LastModified":"Fri, 24 Feb 2012 06:07:48 GMT","ETag":"\\"D41D8CD98F00B204E9800998ECF8****\\""},"FilePath":"gthnjXGQ-no-surfix","PartSize":5242880,"DownloadInfo":{"Offset":5242880,"CRC64":0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        #Magic fail
        cpdata = '{"Magic":"82611BED-89E2-46B6-89E5-72F273D4B0A3","MD5":"cc615a3b3fca2766786669a68895f3ed","Data":{"ObjectInfo":{"Name":"oss://bucket/key","VersionId":"","Range":""},"ObjectMeta":{"Size":344606,"LastModified":"Fri, 24 Feb 2012 06:07:48 GMT","ETag":"\\"D41D8CD98F00B204E9800998ECF8****\\""},"FilePath":"gthnjXGQ-no-surfix","PartSize":5242880,"DownloadInfo":{"Offset":5242880,"CRC64":0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # invalid cp format
        cpdata = '"Magic":"92611BED-89E2-46B6-89E5-72F273D4B0A3","MD5":"cc615a3b3fca2766786669a68895f3ed","Data":{"ObjectInfo":{"Name":"oss://bucket/key","VersionId":"","Range":""},"ObjectMeta":{"Size":344606,"LastModified":"Fri, 24 Feb 2012 06:07:48 GMT","ETag":"\\"D41D8CD98F00B204E9800998ECF8****\\""},"FilePath":"gthnjXGQ-no-surfix","PartSize":5242880,"DownloadInfo":{"Offset":5242880,"CRC64":0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # ObjectInfo not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "67c7658602742baa0a5b6788bfbb9b8f", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "123", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 5242880, "DownloadInfo": {"Offset": 5242880, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # ObjectMeta not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "574e30360fd1575dcbba5831ae0a3e30", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 3446061, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 5242880, "DownloadInfo": {"Offset": 5242880, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # FilePath not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "8b328023db46b845d6cfc60ce4b5b7cd", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix-1", "PartSize": 5242880, "DownloadInfo": {"Offset": 5242880, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # PartSize not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "3a4412930e3598bdc6ee92c12376e597", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 2621440, "DownloadInfo": {"Offset": 5242880, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # Offset invalid
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "3834d2b67de65d7ccc5775f419e1ec62", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 5242880, "DownloadInfo": {"Offset": -1, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # Offset %
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "d4b74aa6f9e6311925956684619e824c", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 5242880, "DownloadInfo": {"Offset": 1, "CRC64": 0}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # check sum equal
        cp.cp_info["Data"]["PartSize"] = 6
        cp.verify_data = True
        data = "hello world!"
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "f58be84fc61d45ef092d056b200e85b5", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 6, "DownloadInfo": {"Offset": 12, "CRC64": 9548687815775124833}}}'
        _write_file(dest_filepath, data.encode())
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertTrue(cp._is_valid())
        self.assertEqual(12, cp.doffset)
        self.assertEqual(9548687815775124833, cp.dcrc64)
        
        # check sum not equal
        cp.cp_info["Data"]["PartSize"] = 6
        cp.verify_data = True
        data = "hello world!"
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "96b19210cc0f66aa0e4afec872bffc8b", "Data": {"ObjectInfo": {"Name": "oss://bucket/key", "VersionId": "", "Range": ""}, "ObjectMeta": {"Size": 344606, "LastModified": "Fri, 24 Feb 2012 06:07:48 GMT", "ETag": "\\"D41D8CD98F00B204E9800998ECF8****\\""}, "FilePath": "gthnjXGQ-no-surfix", "PartSize": 6, "DownloadInfo": {"Offset": 12, "CRC64": 9548687815775124834}}}'
        _write_file(dest_filepath, data.encode())
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        _remove_slice(dest_filepath)        
        _remove_slice(cp.cp_filepath)        

    def test_upload_checkpoint(self):
        request = models.PutObjectRequest(
            bucket='bucket',
            key='key'
        )

        src_filepath = "upload_checkpoint-no-surfix"
        cpdir = "."
        fileinfo = os.stat("./tests/data/example.jpg")
        part_size = defaults.DEFAULT_UPLOAD_PART_SIZE
        cp = checkpoint.UploadCheckpoint(request, src_filepath, cpdir, fileinfo, part_size)

        self.assertIsNotNone(cp)
        self.assertEqual(fileinfo.st_mtime, cp.cp_info["Data"]["FileMeta"]["LastModified"])
        self.assertEqual(fileinfo.st_size, cp.cp_info["Data"]["FileMeta"]["Size"])

        self.assertEqual("oss://bucket/key", cp.cp_info["Data"]["ObjectInfo"]["Name"])
 
        self.assertEqual(defaults.CHECKPOINT_MAGIC, cp.cp_info["Magic"])
        self.assertEqual(None, cp.cp_info.get("MD5", None))

        self.assertEqual(src_filepath, cp.cp_info["Data"]["FilePath"])
        self.assertEqual(defaults.DEFAULT_UPLOAD_PART_SIZE, cp.cp_info["Data"]["PartSize"])

        #check dump
        cp.upload_id = "upload-id"
        done = cp.dump()
        self.assertEqual(True, done)
        self.assertTrue(os.path.isfile(cp.cp_filepath))
        content = b''
        with open(cp.cp_filepath, 'rb') as f:
            content = f.read()
        self.assertTrue(len(content) > 0)
        info = json.loads(content)

        self.assertEqual(fileinfo.st_mtime, info["Data"]["FileMeta"]["LastModified"])
        self.assertEqual(fileinfo.st_size, info["Data"]["FileMeta"]["Size"])

        self.assertEqual("oss://bucket/key", info["Data"]["ObjectInfo"]["Name"])
  
        self.assertEqual(src_filepath, info["Data"]["FilePath"])
        self.assertEqual(defaults.DEFAULT_UPLOAD_PART_SIZE, info["Data"]["PartSize"])

        self.assertEqual("upload-id", info["Data"]["UploadInfo"]["UploadId"])
 
        #check load
        cp.load()
        self.assertEqual(True, cp.loaded)

        #check valid
        self.assertEqual(True, cp._is_valid())

        #check complete
        self.assertEqual(True, os.path.isfile(cp.cp_filepath))
        cp.remove()
        self.assertEqual(False, os.path.isfile(cp.cp_filepath))

        #load not match
        cp = checkpoint.UploadCheckpoint(request, src_filepath, cpdir, fileinfo, part_size)
        self.assertEqual(False, cp.loaded)
        not_match = '{"Magic":"92611BED-89E2-46B6-89E5-72F273D4B0A3","MD5":"5ff2e8fbddc007157488c1087105f6d2","Data":{"FilePath":"vhetHfkY-no-surfix","FileMeta":{"Size":100,"LastModified":"2024-01-08 16:46:27.7178907 +0800 CST m=+0.014509001"},"ObjectInfo":{"Name":"oss://bucket/key"},"PartSize":5242880,"UploadInfo":{"UploadId":""}}}'
        _write_file(cp.cp_filepath, not_match.encode())
        self.assertEqual(True, os.path.isfile(cp.cp_filepath))
        cp.load()
        self.assertEqual(False, cp.loaded)
        self.assertEqual(False, os.path.isfile(cp.cp_filepath))


    def test_upload_checkpoint_invalid_cppath(self):
        request = models.PutObjectRequest(
            bucket='bucket',
            key='key'
        )

        src_filepath = "upload_checkpoint-no-surfix"
        cpdir = "./invliad-dir/"
        fileinfo = os.stat("./tests/data/example.jpg")
        part_size = defaults.DEFAULT_UPLOAD_PART_SIZE
        cp = checkpoint.UploadCheckpoint(request, src_filepath, cpdir, fileinfo, part_size)
        self.assertEqual(src_filepath, cp.cp_info["Data"]["FilePath"])
        self.assertEqual("./invliad-dir", cp.cp_dirpath)
        self.assertIn("invliad-dir", cp.cp_filepath)

        done = cp.dump()
        self.assertEqual(False, done)

        #load fail
        try:
            cp.load()
            self.fail("should not here")
        except Exception as err:
            self.assertIn("Invaid checkpoint dir", str(err))

    def test_upload_checkpoint_valid(self):
        request = models.PutObjectRequest(
            bucket='bucket',
            key='key'
        )

        src_filepath = "athnjXGQ-no-surfix"
        cpdir = "."
        fileinfo = os.stat_result((33206, 1688849865056404,13015084316502127928, 1, 0, 0, 21839, 1725449727, 1724840443, 1724840443), {})
        part_size = 5 * 1024 *1024
        cp = checkpoint.UploadCheckpoint(request, src_filepath, cpdir, fileinfo, part_size)

        _remove_slice(cp.cp_filepath)
        self.assertEqual('', cp.upload_id)
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "4e42d5e63ed9a59bb896e55a794320e7", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertTrue(cp._is_valid())
        self.assertEqual('upload-id', cp.upload_id)

        # md5 fail
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "1e42d5e63ed9a59bb896e55a794320e7", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # Magic fail
        cpdata = '{"Magic": "82611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "4e42d5e63ed9a59bb896e55a794320e7", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # invalid cp format
        cpdata = '"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "4e42d5e63ed9a59bb896e55a794320e7", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # FilePath not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "0ad12fa896c688cf90de0961423e253d", "Data": {"FilePath": "athnjXGQ-no-surfix-1", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # FileMeta not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "aa5ed50adf5d52cf978ee29aea958d0f", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840444}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # ObjectInfo not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "44347464d321317bbc86c9d17dbcca9e", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key-1"}, "PartSize": 5242880, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # PartSize not equal
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "18127e61e60aa011f38d5cba64b1fe47", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 52428800, "UploadInfo": {"UploadId": "upload-id"}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        # uploadId invalid
        cpdata = '{"Magic": "92611BED-89E2-46B6-89E5-72F273D4B0A3", "MD5": "38dd6a5cde64c5b0499d70b70fe5899c", "Data": {"FilePath": "athnjXGQ-no-surfix", "FileMeta": {"Size": 21839, "LastModified": 1724840443}, "ObjectInfo": {"Name": "oss://bucket/key"}, "PartSize": 5242880, "UploadInfo": {"UploadId": ""}}}'
        _write_file(cp.cp_filepath, cpdata.encode())
        self.assertFalse(cp._is_valid())

        _remove_slice(src_filepath)
        _remove_slice(cp.cp_filepath)        
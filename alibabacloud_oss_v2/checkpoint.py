import os
import json
from typing import MutableMapping, Dict
from urllib.parse import quote
from tempfile import gettempdir
import hashlib
from .models import GetObjectRequest, PutObjectRequest
from .utils import safety_str, parse_http_range
from .io_utils import LimitReader
from .crc import Crc64
from .defaults import (
    CHECKPOINT_FILE_SUFFIX_DOWNLOADER,
    CHECKPOINT_FILE_SUFFIX_UPLOADER,
    CHECKPOINT_MAGIC
)

# ----- download checkpoint  -----
# {
#     "CpDirPath": string,         // checkpoint dir full path
#     "CpFilePath": string,        // checkpoint file full path
#     "VerifyData": bool,          // verify downloaded data in FilePath
#     "Loaded": bool,              // If Info.Data.DownloadInfo is loaded from checkpoint
#     "Info": {                    // checkpoint data
#         "Magic": string,         // Magic
#         "MD5": string,           // The Data's MD5
#         "Data": {
#             "ObjectInfo": {         // source
#                "Name": string,
#                "VersionId": string,
#                "Range": string,
#             },
#             "ObjectMeta": {
#                 "Size": int,
#                 "LastModified": string,
#                 "ETag": string,
#             },
#             "FilePath": string,    // destination, Local file
#             "PartSize": int,
#
#             "DownloadInfo": {      // download info
#                 "Offset": int,
#                 "CRC64": int
#             },
#         }
#     },
# }

class DownloadCheckpoint:
    """Download Checkpoint
    """
    def __init__(
        self,
        request: GetObjectRequest,
        filepath: str,
        basedir: str,
        headers: MutableMapping,
        part_size: int
    ) -> None:
        name = f'{request.bucket}/{request.key}'
        canon_src = f'oss://{quote(name)}\n{safety_str(request.version_id)}\n{safety_str(request.range_header)}'
        h = hashlib.md5()
        h.update(canon_src.encode())
        src_hash = h.hexdigest()

        absfilepath = os.path.abspath(filepath)
        h = hashlib.md5()
        h.update(absfilepath.encode())
        dst_hash = h.hexdigest()

        if not basedir:
            dirbase = gettempdir()
        else:
            dirbase = os.path.dirname(basedir)

        cp_filepath = os.path.join(dirbase, f'{src_hash}-{dst_hash}{CHECKPOINT_FILE_SUFFIX_DOWNLOADER}')
        object_size = int(headers.get("Content-Length"))

        self.cp_filepath = cp_filepath
        self.cp_dirpath = dirbase
        self.verify_data = False
        self.loaded = False
        self.cp_info = {
            "Magic": CHECKPOINT_MAGIC,
            #"MD5": md5hex,
            "Data": {
                "ObjectInfo": {
                    "Name": f'oss://{name}',
                    "VersionId": safety_str(request.version_id),
                    "Range": safety_str(request.range_header),
                },
                "ObjectMeta": {
                    "Size": object_size,
                    "LastModified": headers.get("Last-Modified", ''),
                    "ETag": headers.get("ETag", ''),
                },
                "FilePath": filepath,
                "PartSize": part_size,
            },
        }
        self.doffset = 0
        self.dcrc64 = 0

    def load(self):
        """load checkpoint from local file
        """
        if len(self.cp_dirpath) > 0 and not os.path.isdir(self.cp_dirpath):
            raise ValueError(f'Invaid checkpoint dir {self.cp_dirpath}')

        if not os.path.isfile(self.cp_filepath):
            return

        if not self._is_valid():
            self.remove()
            return

        self.loaded = True

    def _is_valid(self) -> bool:
        try:
            dcp_info = {}
            with open(self.cp_filepath, 'rb') as f:
                dcp_info = json.loads(f.read())
                if not isinstance(dcp_info, Dict):
                    return False

                js = json.dumps(dcp_info.get("Data", {})).encode()
                h = hashlib.md5()
                h.update(js)
                md5sum = h.hexdigest()

                if (CHECKPOINT_MAGIC != dcp_info.get("Magic") or
                    md5sum != dcp_info.get("MD5")):
                    return False

            cpid = self.cp_info["Data"]
            dcpid = dcp_info["Data"]

            #compare
            if (cpid["ObjectInfo"] != dcpid["ObjectInfo"] or
                cpid["ObjectMeta"] != dcpid["ObjectMeta"] or
                cpid["FilePath"] != dcpid["FilePath"] or
                cpid["PartSize"] != dcpid["PartSize"]):
                return False

	        #download info
            offset = dcpid["DownloadInfo"].get('Offset', 0)
            crc64 = dcpid["DownloadInfo"].get('CRC64', 0)
            if (not isinstance(offset, int) or
                not isinstance(crc64, int)):
                return False

            if offset == 0 and crc64 != 0:
                return False

            roffset = 0
            if len(cpid["ObjectInfo"]["Range"]) > 0:
                range_header = parse_http_range(cpid["ObjectInfo"]["Range"])
                if offset < range_header[0]:
                    return False
                roffset = range_header[0]

            remains = (offset - roffset) % dcpid["PartSize"]
            if remains != 0:
                return False

            #valid data
            if self.verify_data and crc64 != 0:
                try:
                    with open(dcpid["FilePath"], 'rb') as f:
                        chash = Crc64(0)
                        limitn = offset - roffset
                        r = LimitReader(f, limitn)
                        chunk = 32 * 1024
                        for _ in range(0, limitn, chunk):
                            chash.write(r.read(chunk))
                        if chash.sum64() != crc64:
                            return False
                except Exception:
                    return False

            self.doffset = offset
            self.dcrc64 = crc64

            return True
        except Exception:
            #print(f"err = {err}")
            pass

        return False

    def dump(self) -> bool:
        """dump the checkpoint to local file
        """
        #Calculate MD5
        self.cp_info["Data"]["DownloadInfo"] = {
            "Offset": self.doffset,
            "CRC64": self.dcrc64
        }
        js = json.dumps(self.cp_info["Data"]).encode()
        h = hashlib.md5()
        h.update(js)
        self.cp_info["MD5"] = h.hexdigest()

        #Serialize
        try:
            js = json.dumps(self.cp_info).encode()
            with open(self.cp_filepath, 'wb') as f:
                f.write(js)
        except (OSError, ValueError):
            return False

        return True

    def remove(self) -> None:
        try:
            os.remove(self.cp_filepath)
        except (OSError, ValueError):
            pass

# ----- upload checkpoint  -----
# {
#     "CpDirPath": string,         // checkpoint dir full path
#     "CpFilePath": string,        // checkpoint file full path
#     "Loaded": bool,              // If Info.Data.DownloadInfo is loaded from checkpoint
#     "Info": {                    // checkpoint data
#         "Magic": string,         // Magic
#         "MD5": string,           // The Data's MD5
#         "Data": {
#             "FilePath": string,    // source, Local file
#             "FileMeta": {          // source
#                "Size": int,
#                "LastModified": string,
#             },
#             "ObjectInfo": {
#                 "Name": string,
#             },
#
#             "PartSize": int,
#             "UploadInfo": {      // upload info
#                 "UploadId": string,
#             },
#         }
#     },
# }

class UploadCheckpoint:
    """Upload Checkpoint
    """
    def __init__(
        self,
        request: PutObjectRequest,
        filepath: str,
        basedir: str,
        fileinfo: os.stat_result,
        part_size: int
    ) -> None:
        name = f'{request.bucket}/{request.key}'
        canon_dst = f'oss://{quote(name)}'
        h = hashlib.md5()
        h.update(canon_dst.encode())
        dst_hash = h.hexdigest()

        absfilepath = os.path.abspath(filepath)
        h = hashlib.md5()
        h.update(absfilepath.encode())
        src_hash = h.hexdigest()

        if basedir is None or len(basedir) == 0:
            dirbase = gettempdir()
        else:
            dirbase = os.path.dirname(basedir)

        cp_filepath = os.path.join(dirbase, f'{src_hash}-{dst_hash}{CHECKPOINT_FILE_SUFFIX_UPLOADER}')

        self.cp_filepath = cp_filepath
        self.cp_dirpath = dirbase
        self.loaded = False
        self.cp_info = {
            "Magic": CHECKPOINT_MAGIC,
            #"MD5": md5hex,
            "Data": {
                "FilePath": filepath,
                "FileMeta": {
                    "Size": fileinfo.st_size,
                    "LastModified": fileinfo.st_mtime,
                },
                "ObjectInfo": {
                    "Name": f'oss://{name}',
                },
                "PartSize": part_size,
            },
        }
        self.upload_id = ''

    def load(self):
        """load checkpoint from local file
        """
        if len(self.cp_dirpath) > 0 and not os.path.isdir(self.cp_dirpath):
            raise ValueError(f'Invaid checkpoint dir {self.cp_dirpath}')

        if not os.path.isfile(self.cp_filepath):
            return

        if not self._is_valid():
            self.remove()
            return

        self.loaded = True

    def _is_valid(self) -> bool:
        try:
            ucp_info = {}
            with open(self.cp_filepath, 'rb') as f:
                ucp_info = json.loads(f.read())
                if not isinstance(ucp_info, Dict):
                    return False

                js = json.dumps(ucp_info.get("Data", {})).encode()
                h = hashlib.md5()
                h.update(js)
                md5sum = h.hexdigest()

                if (CHECKPOINT_MAGIC != ucp_info.get("Magic") or
                    md5sum != ucp_info.get("MD5")):
                    return False

            cpid = self.cp_info["Data"]
            ucpid = ucp_info["Data"]

            #compare
            if (cpid["ObjectInfo"] != ucpid["ObjectInfo"] or
                cpid["FileMeta"] != ucpid["FileMeta"] or
                cpid["FilePath"] != ucpid["FilePath"] or
                cpid["PartSize"] != ucpid["PartSize"]):
                return False

	        #upload info
            uploadid = ucpid["UploadInfo"]["UploadId"]
            if not isinstance(uploadid, str) or uploadid == '':
                return False

            self.upload_id = uploadid

            return True
        except Exception:
            #print(f"err = {err}")
            pass

        return False

    def dump(self) -> bool:
        """dump the checkpoint to local file
        """
        #Calculate MD5
        self.cp_info["Data"]["UploadInfo"] = {
            "UploadId": self.upload_id,
        }
        js = json.dumps(self.cp_info["Data"]).encode()
        h = hashlib.md5()
        h.update(js)
        self.cp_info["MD5"] = h.hexdigest()

        #Serialize
        try:
            js = json.dumps(self.cp_info).encode()
            with open(self.cp_filepath, 'wb') as f:
                f.write(js)
        except (OSError, ValueError):
            return False

        return True

    def remove(self) -> None:
        """remove the checkpoint file
        """
        try:
            os.remove(self.cp_filepath)
        except (OSError, ValueError):
            pass

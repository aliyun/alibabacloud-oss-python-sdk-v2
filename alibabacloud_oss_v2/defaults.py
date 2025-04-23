# Default transport 's connect timeout is 10, the unit is seconod
DEFAULT_CONNECT_TIMEOUT = 10

# Default transport 's request timeout is 20, the unit is seconod
DEFAULT_READWRITE_TIMEOUT = 20

# Default signature version is v4
DEFAULT_SIGNATURE_VERSION = "v4"

# Product for signing
DEFAULT_PRODUCT = "oss"

# CloudBoxProduct Product of cloud box for signing
CLOUD_BOX_PRODUCT = "oss-cloudbox"

# The URL's scheme, default is https
DEFAULT_ENDPOINT_SCHEME = "https"

DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_MAX_BACKOFF_S = 20.0
DEFAULT_BASE_DELAY_S = 0.2

DEFAULT_IDLE_CONNECTION_TIMEOUT = 50
DEFAULT_KEEP_ALIVE_TIMEOUT = 30
DEFAULT_EXPECT_CONTINUE_TIMEOUT = 30

DEFAULT_MAX_CONNECTIONS = 20

# TLS 1.2 for all HTTPS requests.
# DEFAULT_TLS_MIN_VERSION = 1.2

DEFAULT_BLOCK_SIZE = 16 * 1024

# Default part size, 6M
DEFAULT_PART_SIZE = 6 * 1024 * 1024

# Default part size for uploader uploads data
DEFAULT_UPLOAD_PART_SIZE = DEFAULT_PART_SIZE

# Default part size for downloader downloads object
DEFAULT_DOWNLOAD_PART_SIZE = DEFAULT_PART_SIZE

# Default part size for copier copys object, 64M
DEFAULT_COPY_PART_SIZE = 64 * 1024 * 1024

# Default parallel
DEFAULT_PARALLEL = 3

# Default parallel for uploader uploads data
DEFAULT_UPLOAD_PARALLEL = DEFAULT_PARALLEL

# Default parallel for downloader downloads object
DEFAULT_DOWNLOAD_PARALLEL = DEFAULT_PARALLEL

# Default parallel for copier copys object
DEFAULT_COPY_PARALLEL = DEFAULT_PARALLEL

# Default prefetch threshold to swith to async read in ReadOnlyFile
DEFAULT_PREFETCH_THRESHOLD  = 20 * 1024 * 1024

# Default prefetch number for async read in ReadOnlyFile
DEFAULT_PREFETCH_NUM = DEFAULT_PARALLEL

# Default prefetch chunk size for async read in ReadOnlyFile
DEFAULT_PREFETCH_CHUNK_SIZE = DEFAULT_PART_SIZE

# Default threshold to use muitipart copy in Copier, 200MiB
DEFAULT_COPY_THRESHOLD = 200 * 1024 * 1024

# Temp file suffix
DEFAULT_TEMP_FILE_SUFFIX = ".temp"

MAX_UPLOAD_PARTS = 10000

#Checkpoint file suffix for Downloader
CHECKPOINT_FILE_SUFFIX_DOWNLOADER = ".dcp"

#Checkpoint file suffix for Uploader
CHECKPOINT_FILE_SUFFIX_UPLOADER = ".ucp"

#Checkpoint file Magic
CHECKPOINT_MAGIC = "92611BED-89E2-46B6-89E5-72F273D4B0A3"

#Feature Flags
# FeatureCorrectClockSkew If the client time is different from server time by more than about 15 minutes,
# the requests your application makes will be signed with the incorrect time, and the server will reject them.
# The feature to help to identify this case, and SDK will correct for clock skew.
FF_CORRECT_CLOCK_SKEW = 0x00000001

FF_ENABLE_MD5 = 0x00000002

# FeatureAutoDetectMimeType Content-Type is automatically added based on the object name if not specified.
# This feature takes effect for PutObject, AppendObject and InitiateMultipartUpload
FF_AUTO_DETECT_MIME_TYPE = 0x00000004

# FeatureEnableCRC64CheckUpload check data integrity of uploads via the crc64.
# This feature takes effect for PutObject, AppendObject, UploadPart, Uploader.UploadFrom and Uploader.UploadFile
FF_ENABLE_CRC64_CHECK_UPLOAD = 0x00000008

# FeatureEnableCRC64CheckDownload check data integrity of downloads via the crc64.
# This feature takes effect for Downloader.DownloadFile
FF_ENABLE_CRC64_CHECK_DOWNLOAD = 0x00000010

# Default feature flags
FF_DEFAULT = (FF_CORRECT_CLOCK_SKEW + FF_AUTO_DETECT_MIME_TYPE +
              FF_ENABLE_CRC64_CHECK_UPLOAD + FF_ENABLE_CRC64_CHECK_DOWNLOAD)

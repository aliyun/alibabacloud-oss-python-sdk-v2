DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_READWRITE_TIMEOUT = 10

# Default signature version is v4
DEFAULT_SIGNATURE_VERSION = "v4"

# Product for signing
DEFAULT_PRODUCT = "oss"

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

DEFAULT_CHUNK_SIZE = 16 * 1024

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

# Temp file suffix
DEFAULT_TEMP_FILE_SUFFIX = ".temp"

MAX_UPLOAD_PARTS = 10000

#Checkpoint file suffix for Downloader
CHECKPOINT_FILE_SUFFIX_DOWNLOADER = ".dcp"

#Checkpoint file suffix for Uploader
CHECKPOINT_FILE_SUFFIX_UPLOADER = ".ucp"

#Checkpoint file Magic
CHECKPOINT_MAGIC = "92611BED-89E2-46B6-89E5-72F273D4B0A3"
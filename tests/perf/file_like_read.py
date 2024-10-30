import argparse
import time
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="download file test")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--enable_prefetch', help='The flag of enable prefetch.')
parser.add_argument('--chunk_size', help='The chunk size.')
parser.add_argument('--prefetch_num', help='The parallel num.')
parser.add_argument('--block_size', help='The block size.')

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

    kwargs = {'prefetch_threshold': 0}

    if args.enable_prefetch is not None:
        kwargs['enable_prefetch'] = bool(args.enable_prefetch)

    if args.prefetch_num is not None:
        kwargs['prefetch_num'] = int(args.prefetch_num)

    if args.chunk_size is not None:
        kwargs['chunk_size'] = int(args.chunk_size)

    if args.block_size is not None:
        kwargs['block_size'] = int(args.block_size)

    file = client.open_file(bucket=args.bucket, key=args.key, **kwargs)

    print(f'open_file {args.key}' \
          f' with enable_prefetch:{file._enable_prefetch}, prefetch_num:{file._prefetch_num}'\
          f', chunk_size:{file._chunk_size}, block_size:{file._block_size}')

    stime = time.time()

    read_size = 256 * 1024
    if args.block_size is not None:
        read_size = int(args.block_size)

    blob = memoryview(bytearray(read_size))
    got = 0
    while True:
        n = file.readinto(blob)
        if n == 0:
            break
        got += n

    etime = time.time()

    avg = got/(etime - stime)
    savg = ''
    if avg > 1024*1024*1024:
        savg = f'{avg/1024/1024/1024:.2f} GiB/s'
    if avg > 1024*1024:
        savg = f'{avg/1024/1024:.2f} MiB/s'
    elif avg > 1024:
        savg = f'{avg/1024:.2f} KiB/s'
    else:
        savg = f'{avg:.2f} B/s'

    print(f'finish read file, got size {got}, cost: {etime - stime:.2f} s, avg: {savg}')
    file.close()

if __name__ == "__main__":
    main()

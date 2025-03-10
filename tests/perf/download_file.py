import argparse
import time
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="download file test")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--part_size', help='The part size.')
parser.add_argument('--parallel_num', help='The parallel num.')
parser.add_argument('--block_size', help='The block size.')
parser.add_argument('--filepath', help='The file path.')

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

    cfg.disable_download_crc64_check = True
    client = oss.Client(cfg)

    kwargs = {'use_temp_file': False}

    if args.part_size is not None:
        kwargs['part_size'] = int(args.part_size)

    if args.parallel_num is not None:
        kwargs['parallel_num'] = int(args.parallel_num)

    if args.block_size is not None:
        kwargs['block_size'] = int(args.block_size)

    d = client.downloader(**kwargs)

    print(f'start download {args.filepath} with options={d._options.__dict__}')

    stime = time.time()

    result = d.download_file(oss.GetObjectRequest(bucket=args.bucket, key=args.key), args.filepath)

    etime = time.time()

    avg = result.written/(etime - stime)
    savg = ''
    if avg > 1024*1024*1024:
        savg = f'{avg/1024/1024/1024:.2f} GiB/s'
    if avg > 1024*1024:
        savg = f'{avg/1024/1024:.2f} MiB/s'
    elif avg > 1024:
        savg = f'{avg/1024:.2f} KiB/s'
    else:
        savg = f'{avg:.2f} B/s'

    print(f'finish download, got size {result.written}, cost: {etime - stime:.2f} s, avg: {savg}')

if __name__ == "__main__":
    main()

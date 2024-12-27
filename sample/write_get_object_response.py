# -*- coding: utf-8 -*-
import argparse
import alibabacloud_oss_v2 as oss
import logging
import json

parser = argparse.ArgumentParser(description="write get object response sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--fwd_status', default='200')
parser.add_argument('--fwd_header_content_type', default='application/octet-stream')
parser.add_argument('--fwd_header_etag', default='testetag')


# Fc function entry
def handler(event, context):
    headers = dict()
    headers['x-oss-fwd-header-Content-Type'] = 'application/octet-stream'
    headers['x-oss-fwd-header-ETag'] = 'testetag'

    logger = logging.getLogger()
    logger.info(event)
    logger.info("enter request")
    evt = json.loads(event)
    event_ctx = evt["getObjectContext"]
    route = event_ctx["outputRoute"]
    token = event_ctx["outputToken"]
    print('outputRoute: '+route)
    print('outputToken: '+token)

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = route

    client = oss.Client(cfg)

    content = 'a' * 1024

    result = client.write_get_object_response(oss.WriteGetObjectResponseRequest(
        request_route=route,
        request_token=token,
        fwd_status=args.fwd_status,
        # fwd_header_accept_ranges=args.fwd_header_accept_ranges,
        # fwd_header_cache_control=args.fwd_header_cache_control,
        # fwd_header_content_disposition=args.fwd_header_content_disposition,
        # fwd_header_content_encoding=args.fwd_header_content_encoding,
        # fwd_header_content_language=args.fwd_header_content_language,
        # fwd_header_content_range=args.fwd_header_content_range,
        fwd_header_content_type=args.fwd_header_content_type,
        fwd_header_etag=args.fwd_header_etag,
        # fwd_header_expires=args.fwd_header_expires,
        # fwd_header_last_modified=args.fwd_header_last_modified,
        body=content,
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          )

    logger.info(result)
    logger.info("end request")
    return 'success'






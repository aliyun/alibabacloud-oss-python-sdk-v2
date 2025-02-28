import argparse
import base64
import hashlib
import hmac
import json
import random
import requests
from datetime import datetime, timedelta
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="post object sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--key', help='The name of the object.', required=True)
parser.add_argument('--callback_url', help='Callback server address.', required=True)


def main():
    content = "hi oss"
    product = "oss"

    args = parser.parse_args()
    region = args.region
    bucket_name = args.bucket
    object_name = args.key

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    credential = credentials_provider.get_credentials()
    access_key_id = credential.access_key_id
    access_key_secret = credential.access_key_secret

    utc_time = datetime.utcnow()
    date = utc_time.strftime("%Y%m%d")
    expiration = utc_time + timedelta(hours=1)
    policy_map = {
        "expiration": expiration.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "conditions": [
            {"bucket": bucket_name},
            {"x-oss-signature-version": "OSS4-HMAC-SHA256"},
            {"x-oss-credential": f"{access_key_id}/{date}/{region}/{product}/aliyun_v4_request"},
            {"x-oss-date": utc_time.strftime("%Y%m%dT%H%M%SZ")},
            ["content-length-range", 1, 1024]
        ]
    }
    policy = json.dumps(policy_map)
    string_to_sign = base64.b64encode(policy.encode()).decode()

    def build_post_body(field_dict, boundary):
        post_body = ''

        # Encoding Form Fields
        for k, v in field_dict.items():
            if k != 'content' and k != 'content-type':
                post_body += '''--{0}\r\nContent-Disposition: form-data; name=\"{1}\"\r\n\r\n{2}\r\n'''.format(boundary, k, v)

        # The content of the uploaded file must be the last form field
        post_body += '''--{0}\r\nContent-Disposition: form-data; name=\"file\"\r\n\r\n{1}'''.format(
            boundary, field_dict['content'])

        # Add a form field terminator
        post_body += '\r\n--{0}--\r\n'.format(boundary)

        return post_body.encode('utf-8')

    signing_key = "aliyun_v4" + access_key_secret
    h1 = hmac.new(signing_key.encode(), date.encode(), hashlib.sha256)
    h1_key = h1.digest()
    h2 = hmac.new(h1_key, region.encode(), hashlib.sha256)
    h2_key = h2.digest()
    h3 = hmac.new(h2_key, product.encode(), hashlib.sha256)
    h3_key = h3.digest()
    h4 = hmac.new(h3_key, "aliyun_v4_request".encode(), hashlib.sha256)
    h4_key = h4.digest()

    h = hmac.new(h4_key, string_to_sign.encode(), hashlib.sha256)
    signature = h.hexdigest()

    field_dict = {}
    field_dict['key'] = object_name
    field_dict['policy'] = string_to_sign
    field_dict['x-oss-signature-version'] = "OSS4-HMAC-SHA256"
    field_dict['x-oss-credential'] = f"{access_key_id}/{date}/{region}/{product}/aliyun_v4_request"
    field_dict['x-oss-date'] = f"{utc_time.strftime('%Y%m%dT%H%M%SZ')}"
    field_dict['x-oss-signature'] = signature
    field_dict['content'] = content

    def encode_callback(callback_params):
        cb_str = json.dumps(callback_params).strip()
        return base64.b64encode(cb_str.encode()).decode()

    # Set upload callback parameters.
    callback_params = {}
    # Set the server address for callback requests, for example http://oss-demo.aliyuncs.com:23450 .
    callback_params['callbackUrl'] = args.callback_url
    # (Optional) Set the value of Host in the callback request header, which is the value configured for Host on your server.
    # callback_params['callbackHost'] = 'yourCallbackHost'
    # Set the value of the request body when initiating a callback.
    callback_params['callbackBody'] = 'bucket=${bucket}&object=${object}&my_var_1=${x:my_var1}&my_var_2=${x:my_var2}'
    # Set the Content Type for initiating callback requests.
    callback_params['callbackBodyType'] = 'application/x-www-form-urlencoded'
    encoded_callback = encode_callback(callback_params)
    # Set custom parameters for initiating callback requests, consisting of Key and Value, with Key starting with x:.
    callback_var_params = {'x:my_var1': 'my_val1', 'x:my_var2': 'my_val2'}


    # 上传回调。
    field_dict['callback'] = encoded_callback
    field_dict['x:my_var1'] = 'value1'
    field_dict['x:my_var2'] = 'value2'

    # The boundary string of the form field is usually a random string
    boundary = ''.join(random.choice('0123456789') for _ in range(11))
    # Send POST request
    body = build_post_body(field_dict, boundary)

    url = f"http://{bucket_name}.oss-{region}.aliyuncs.com"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    response = requests.post(url, data=body, headers=headers)

    if response.status_code // 100 != 2:
        print(f"Post Object Fail, status code: {response.status_code}, reason: {response.reason}")
    else:
        print(f"post object done, status code: {response.status_code}, request id: {response.headers.get('X-Oss-Request-Id')}")

    print(f"response: {response.text}")

if __name__ == "__main__":
    main()

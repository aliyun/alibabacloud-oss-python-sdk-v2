import datetime
from typing import Optional, List, Any, Union
from .. import serde


class IndexDocument(serde.Model):
    """
    The container that stores the default homepage.
    """

    _attribute_map = { 
        'suffix': {'tag': 'xml', 'rename': 'Suffix', 'type': 'str'},
        'support_sub_dir': {'tag': 'xml', 'rename': 'SupportSubDir', 'type': 'bool'},
        'type': {'tag': 'xml', 'rename': 'Type', 'type': 'int'},
    }

    _xml_map = {
        'name': 'IndexDocument'
    }

    def __init__(
        self,
        suffix: Optional[str] = None,
        support_sub_dir: Optional[bool] = None,
        type: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        suffix (str, optional): The default homepage.
        support_sub_dir (bool, optional): Specifies whether to redirect the access to the default homepage of the subdirectory when the subdirectory is accessed. Valid values:*   **true**: The access is redirected to the default homepage of the subdirectory.*   **false** (default): The access is redirected to the default homepage of the root directory.For example, the default homepage is set to index.html, and `bucket.oss-cn-hangzhou.aliyuncs.com/subdir/` is the site that you want to access. If **SupportSubDir** is set to false, the access is redirected to `bucket.oss-cn-hangzhou.aliyuncs.com/index.html`. If **SupportSubDir** is set to true, the access is redirected to `bucket.oss-cn-hangzhou.aliyuncs.com/subdir/index.html`.
        type (int, optional): The operation to perform when the default homepage is set, the name of the accessed object does not end with a forward slash (/), and the object does not exist. This parameter takes effect only when **SupportSubDir** is set to true. It takes effect after RoutingRule but before ErrorFile. For example, the default homepage is set to index.html, `bucket.oss-cn-hangzhou.aliyuncs.com/abc` is the site that you want to access, and the abc object does not exist. In this case, different operations are performed based on the value of **Type**.*   **0** (default): OSS checks whether the object named abc/index.html, which is in the `Object + Forward slash (/) + Homepage` format, exists. If the object exists, OSS returns HTTP status code 302 and the Location header value that contains URL-encoded `/abc/`. The URL-encoded /abc/ is in the `Forward slash (/) + Object + Forward slash (/)` format. If the object does not exist, OSS returns HTTP status code 404 and continues to check ErrorFile.*   **1**: OSS returns HTTP status code 404 and the NoSuchKey error code and continues to check ErrorFile.*   **2**: OSS checks whether abc/index.html exists. If abc/index.html exists, the content of the object is returned. If abc/index.html does not exist, OSS returns HTTP status code 404 and continues to check ErrorFile.
        """
        super().__init__(**kwargs)
        self.suffix = suffix
        self.support_sub_dir = support_sub_dir
        self.type = type


class MirrorHeadersSet(serde.Model):
    """
    The headers that are sent to the origin. The specified headers are configured in the data returned by the origin regardless of whether the headers are contained in the request. This parameter takes effect only when the value of RedirectType is Mirror. You can specify up to 10 headers.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Set'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        key (str, optional): The key of the header. The key can be up to 1,024 bytes in length and can contain only letters, digits, and hyphens (-). This parameter takes effect only when the value of RedirectType is Mirror.  This parameter must be specified if Set is specified.
        value (str, optional): The value of the header. The value can be up to 1,024 bytes in length and cannot contain `\r\n`. This parameter takes effect only when the value of RedirectType is Mirror.  This parameter must be specified if Set is specified.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


class ErrorDocument(serde.Model):
    """
    The container that stores the default 404 page.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'http_status': {'tag': 'xml', 'rename': 'HttpStatus', 'type': 'int'},
    }

    _xml_map = {
        'name': 'ErrorDocument'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        http_status: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        key (str, optional): The error page.
        http_status (int, optional): The HTTP status code returned with the error page.
        """
        super().__init__(**kwargs)
        self.key = key
        self.http_status = http_status


class RoutingRuleIncludeHeader(serde.Model):
    """
    只有请求中包含了指定Header且值为指定值时，才能匹配此规则。该容器最多可指定10个。
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'equals': {'tag': 'xml', 'rename': 'Equals', 'type': 'str'},
    }

    _xml_map = {
        'name': 'IncludeHeader'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        equals: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        key (str, optional): 只有请求中包含了此Header且值为Equals的指定值时，才能匹配此规则。
        equals (str, optional): 只有请求中包含了Key指定的Header且值为指定值时，才能匹配此规则。
        """
        super().__init__(**kwargs)
        self.key = key
        self.equals = equals


class RoutingRuleCondition(serde.Model):
    """
    The matching condition. If all of the specified conditions are met, the rule is run. A rule is considered matched only when the rule meets the conditions that are specified by all nodes in Condition.  This parameter must be specified if RoutingRule is specified.
    """

    _attribute_map = {
        'key_suffix_equals': {'tag': 'xml', 'rename': 'KeySuffixEquals', 'type': 'str'},
        'http_error_code_returned_equals': {'tag': 'xml', 'rename': 'HttpErrorCodeReturnedEquals', 'type': 'int'},
        'include_headers': {'tag': 'xml', 'rename': 'IncludeHeader', 'type': '[IncludeHeader]'},
        'key_prefix_equals': {'tag': 'xml', 'rename': 'KeyPrefixEquals', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Condition'
    }

    _dependency_map = {
        'IncludeHeader': {'new': lambda: RoutingRuleIncludeHeader()},
    }

    def __init__(
        self,
        key_suffix_equals: Optional[str] = None,
        http_error_code_returned_equals: Optional[int] = None,
        include_headers: Optional[List[RoutingRuleIncludeHeader]] = None,
        key_prefix_equals: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        key_suffix_equals (str, optional): 只有匹配此后缀的Object才能匹配此规则。
        http_error_code_returned_equals (int, optional): The HTTP status code. The rule is matched only when the specified object is accessed and the specified HTTP status code is returned. If the redirection rule is the mirroring-based back-to-origin rule, the value of this parameter is 404.
        include_headers (List[IncludeHeader], optional): 只有请求中包含了指定Header且值为指定值时，才能匹配此规则。该容器最多可指定10个。
        key_prefix_equals (str, optional): The prefix of object names. Only objects whose names contain the specified prefix match the rule.
        """
        super().__init__(**kwargs)
        self.key_suffix_equals = key_suffix_equals
        self.http_error_code_returned_equals = http_error_code_returned_equals
        self.include_headers = include_headers
        self.key_prefix_equals = key_prefix_equals


class MirrorHeaders(serde.Model):
    """
    The headers contained in the response that is returned when you use mirroring-based back-to-origin. This parameter takes effect only when the value of RedirectType is Mirror.
    """

    _attribute_map = {
        'pass_all': {'tag': 'xml', 'rename': 'PassAll', 'type': 'bool'},
        'passs': {'tag': 'xml', 'rename': 'Pass', 'type': '[str]'},
        'removes': {'tag': 'xml', 'rename': 'Remove', 'type': '[str]'},
        'sets': {'tag': 'xml', 'rename': 'Set', 'type': '[Set]'},
    }

    _xml_map = {
        'name': 'MirrorHeaders'
    }

    _dependency_map = {
        'Set': {'new': lambda: MirrorHeadersSet()},
    }

    def __init__(
        self,
        pass_all: Optional[bool] = None,
        passs: Optional[List[str]] = None,
        removes: Optional[List[str]] = None,
        sets: Optional[List[MirrorHeadersSet]] = None,
        **kwargs: Any
    ) -> None:
        """
        pass_all (bool, optional): Specifies whether to pass through all request headers other than the following headers to the origin. This parameter takes effect only when the value of RedirectType is Mirror.*   Headers such as content-length, authorization2, authorization, range, and date*   Headers that start with oss-, x-oss-, and x-drs-Default value: false.Valid values:*   true            *   false
        passs (List[str], optional): The headers to pass through to the origin. This parameter takes effect only when the value of RedirectType is Mirror. Each specified header can be up to 1,024 bytes in length and can contain only letters, digits, and hyphens (-). You can specify up to 10 headers.
        removes (List[str], optional): The headers that are not allowed to pass through to the origin. This parameter takes effect only when the value of RedirectType is Mirror. Each header can be up to 1,024 bytes in length and can contain only letters, digits, and hyphens (-). You can specify up to 10 headers. This parameter is used together with PassAll.
        sets (List[Set], optional): The headers that are sent to the origin. The specified headers are configured in the data returned by the origin regardless of whether the headers are contained in the request. This parameter takes effect only when the value of RedirectType is Mirror. You can specify up to 10 headers.
        """
        super().__init__(**kwargs)
        self.pass_all = pass_all
        self.passs = passs
        self.removes = removes
        self.sets = sets


class RoutingRuleRedirect(serde.Model):
    """
    The operation to perform after the rule is matched.  This parameter must be specified if RoutingRule is specified.
    """

    _attribute_map = {
        'mirror_url': {'tag': 'xml', 'rename': 'MirrorURL', 'type': 'str'},
        'replace_key_with': {'tag': 'xml', 'rename': 'ReplaceKeyWith', 'type': 'str'},
        'enable_replace_prefix': {'tag': 'xml', 'rename': 'EnableReplacePrefix', 'type': 'bool'},
        'pass_query_string': {'tag': 'xml', 'rename': 'PassQueryString', 'type': 'bool'},
        'mirror_headers': {'tag': 'xml', 'rename': 'MirrorHeaders', 'type': 'MirrorHeaders'},
        'http_redirect_code': {'tag': 'xml', 'rename': 'HttpRedirectCode', 'type': 'int'},
        'mirror_sni': {'tag': 'xml', 'rename': 'MirrorSNI', 'type': 'bool'},
        'protocol': {'tag': 'xml', 'rename': 'Protocol', 'type': 'str'},
        'replace_key_prefix_with': {'tag': 'xml', 'rename': 'ReplaceKeyPrefixWith', 'type': 'str'},
        'redirect_type': {'tag': 'xml', 'rename': 'RedirectType', 'type': 'str'},
        'mirror_pass_query_string': {'tag': 'xml', 'rename': 'MirrorPassQueryString', 'type': 'bool'},
        'host_name': {'tag': 'xml', 'rename': 'HostName', 'type': 'str'},
        'mirror_follow_redirect': {'tag': 'xml', 'rename': 'MirrorFollowRedirect', 'type': 'bool'},
        'mirror_check_md5': {'tag': 'xml', 'rename': 'MirrorCheckMd5', 'type': 'bool'},
        'mirror_pass_original_slashes': {'tag': 'xml', 'rename': 'MirrorPassOriginalSlashes', 'type': 'bool'},
    }

    _xml_map = {
        'name': 'Redirect'
    }

    _dependency_map = {
        'MirrorHeaders': {'new': lambda: MirrorHeaders()},
    }

    def __init__(
        self,
        mirror_url: Optional[str] = None,
        replace_key_with: Optional[str] = None,
        enable_replace_prefix: Optional[bool] = None,
        pass_query_string: Optional[bool] = None,
        mirror_headers: Optional[MirrorHeaders] = None,
        http_redirect_code: Optional[int] = None,
        mirror_sni: Optional[bool] = None,
        protocol: Optional[str] = None,
        replace_key_prefix_with: Optional[str] = None,
        redirect_type: Optional[str] = None,
        mirror_pass_query_string: Optional[bool] = None,
        host_name: Optional[str] = None,
        mirror_follow_redirect: Optional[bool] = None,
        mirror_check_md5: Optional[bool] = None,
        mirror_pass_original_slashes: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        """
        mirror_url (str, optional): The origin URL for mirroring-based back-to-origin. This parameter takes effect only when the value of RedirectType is Mirror. The origin URL must start with \*\*http://** or **https://\*\* and end with a forward slash (/). OSS adds an object name to the end of the URL to generate a back-to-origin URL. For example, the name of the object to access is myobject. If MirrorURL is set to `http://example.com/`, the back-to-origin URL is `http://example.com/myobject`. If MirrorURL is set to `http://example.com/dir1/`, the back-to-origin URL is `http://example.com/dir1/myobject`.  This parameter must be specified if RedirectType is set to Mirror.Valid values:*   true            *   false
        replace_key_with (str, optional): The string that is used to replace the requested object name when the request is redirected. This parameter can be set to the ${key} variable, which indicates the object name in the request. For example, if ReplaceKeyWith is set to `prefix/${key}.suffix` and the object to access is test, the value of the Location header is `http://example.com/prefix/test.suffix`.
        enable_replace_prefix (bool, optional): If this parameter is set to true, the prefix of the object names is replaced with the value specified by ReplaceKeyPrefixWith. If this parameter is not specified or empty, the prefix of object names is truncated.  When the ReplaceKeyWith parameter is not empty, the EnableReplacePrefix parameter cannot be set to true.Default value: false.
        pass_query_string (bool, optional): Specifies whether to include parameters of the original request in the redirection request when the system runs the redirection rule or mirroring-based back-to-origin rule. For example, if the **PassQueryString** parameter is set to true, the `?a=b&c=d` parameter string is included in a request sent to OSS, and the redirection mode is 302, this parameter is added to the Location header. For example, if the request is `Location:example.com?a=b&c=d` and the redirection type is mirroring-based back-to-origin, the ?a=b\&c=d parameter string is also included in the back-to-origin request. Valid values: true and false (default).
        mirror_headers (MirrorHeaders, optional): The headers contained in the response that is returned when you use mirroring-based back-to-origin. This parameter takes effect only when the value of RedirectType is Mirror.
        http_redirect_code (int, optional): The HTTP redirect code in the response. This parameter takes effect only when RedirectType is set to External or AliCDN. Valid values: 301, 302, and 307.
        mirror_sni (bool, optional): 是否透传SNI
        protocol (str, optional): The protocol used for redirection. This parameter takes effect only when RedirectType is set to External or AliCDN. For example, if you access an object named test, Protocol is set to https, and Hostname is set to `example.com`, the value of the Location header is `https://example.com/test`. Valid values: **http** and **https**.
        replace_key_prefix_with (str, optional): The string that is used to replace the prefix of the object name during redirection. If the prefix of an object name is empty, the string precedes the object name.  You can specify only one of the ReplaceKeyWith and ReplaceKeyPrefixWith parameters in a rule. For example, if you access an object named abc/test.txt, KeyPrefixEquals is set to abc/, ReplaceKeyPrefixWith is set to def/, the value of the Location header is `http://example.com/def/test.txt`.
        redirect_type (str, optional): The redirection type. Valid values:*   **Mirror**: mirroring-based back-to-origin.*   **External**: external redirection. OSS returns an HTTP 3xx status code and returns an address for you to redirect to.*   **AliCDN**: redirection based on Alibaba Cloud CDN. Compared with external redirection, OSS adds an additional header to the request. After Alibaba Cloud CDN identifies the header, Alibaba Cloud CDN redirects the access to the specified address and returns the obtained data instead of the HTTP 3xx status code that redirects the access to another address.  This parameter must be specified if Redirect is specified.
        mirror_pass_query_string (bool, optional): This parameter plays the same role as PassQueryString and has a higher priority than PassQueryString. This parameter takes effect only when the value of RedirectType is Mirror. Default value: false.Valid values:*   true            *   false
        host_name (str, optional): The domain name used for redirection. The domain name must comply with the domain naming rules. For example, if you access an object named test, Protocol is set to https, and Hostname is set to `example.com`, the value of the Location header is `https://example.com/test`.
        mirror_follow_redirect (bool, optional): Specifies whether to redirect the access to the address specified by Location if the origin returns an HTTP 3xx status code. This parameter takes effect only when the value of RedirectType is Mirror. For example, when a mirroring-based back-to-origin request is initiated, the origin returns 302 and Location is specified.*   If you set MirrorFollowRedirect to true, OSS continues requesting the resource at the address specified by Location. The access can be redirected up to 10 times. If the access is redirected more than 10 times, the mirroring-based back-to-origin request fails.*   If you set MirrorFollowRedirect to false, OSS returns 302 and passes through Location.Default value: true.
        mirror_check_md5 (bool, optional): Specifies whether to check the MD5 hash of the body of the response returned by the origin. This parameter takes effect only when the value of RedirectType is Mirror. When **MirrorCheckMd5** is set to true and the response returned by the origin includes the Content-Md5 header, OSS checks whether the MD5 hash of the obtained data matches the header value. If the MD5 hash of the obtained data does not match the header value, the obtained data is not stored in OSS. Default value: false.
        mirror_pass_original_slashes (bool, optional): 是否透传/到源站
        """
        super().__init__(**kwargs)
        self.mirror_url = mirror_url
        self.replace_key_with = replace_key_with
        self.enable_replace_prefix = enable_replace_prefix
        self.pass_query_string = pass_query_string
        self.mirror_headers = mirror_headers
        self.http_redirect_code = http_redirect_code
        self.mirror_sni = mirror_sni
        self.protocol = protocol
        self.replace_key_prefix_with = replace_key_prefix_with
        self.redirect_type = redirect_type
        self.mirror_pass_query_string = mirror_pass_query_string
        self.host_name = host_name
        self.mirror_follow_redirect = mirror_follow_redirect
        self.mirror_check_md5 = mirror_check_md5
        self.mirror_pass_original_slashes = mirror_pass_original_slashes


class RoutingRule(serde.Model):
    """
    The container for the redirection rule or mirroring-based back-to-origin rule. You can specify up to 20 rules.
    """

    _attribute_map = {
        'rule_number': {'tag': 'xml', 'rename': 'RuleNumber', 'type': 'int'},
        'condition': {'tag': 'xml', 'rename': 'Condition', 'type': 'RoutingRuleCondition'},
        'redirect': {'tag': 'xml', 'rename': 'Redirect', 'type': 'RoutingRuleRedirect'},
    }

    _xml_map = {
        'name': 'RoutingRule'
    }

    _dependency_map = {
        'RoutingRuleCondition': {'new': lambda: RoutingRuleCondition()},
        'RoutingRuleRedirect': {'new': lambda: RoutingRuleRedirect()},
    }

    def __init__(
        self,
        rule_number: Optional[int] = None,
        condition: Optional[RoutingRuleCondition] = None,
        redirect: Optional[RoutingRuleRedirect] = None,
        **kwargs: Any
    ) -> None:
        """
        rule_number (int, optional): The sequence number that is used to match and run the redirection rules. OSS matches redirection rules based on this parameter. If a match succeeds, only the rule is run and the subsequent rules are not run.  This parameter must be specified if RoutingRule is specified.
        condition (RoutingRuleCondition, optional): The matching condition. If all of the specified conditions are met, the rule is run. A rule is considered matched only when the rule meets the conditions that are specified by all nodes in Condition.  This parameter must be specified if RoutingRule is specified.
        redirect (RoutingRuleRedirect, optional): The operation to perform after the rule is matched.  This parameter must be specified if RoutingRule is specified.
        """
        super().__init__(**kwargs)
        self.rule_number = rule_number
        self.condition = condition
        self.redirect = redirect


class RoutingRules(serde.Model):
    """
    The container that stores the redirection rules.  You must specify at least one of the following containers: IndexDocument, ErrorDocument, and RoutingRules.
    """

    _attribute_map = {
        'routing_rules': {'tag': 'xml', 'rename': 'RoutingRule', 'type': '[RoutingRule]'},
    }

    _xml_map = {
        'name': 'RoutingRules'
    }

    _dependency_map = {
        'RoutingRule': {'new': lambda: RoutingRule()},
    }

    def __init__(
        self,
        routing_rules: Optional[List[RoutingRule]] = None,
        **kwargs: Any
    ) -> None:
        """
        routing_rules (List[RoutingRule], optional): The specified redirection rule or mirroring-based back-to-origin rule. You can specify up to 20 rules.
        """
        super().__init__(**kwargs)
        self.routing_rules = routing_rules


class WebsiteConfiguration(serde.Model):
    """
    The root node for website configuration.
    """

    _attribute_map = { 
        'index_document': {'tag': 'xml', 'rename': 'IndexDocument', 'type': 'IndexDocument'},
        'error_document': {'tag': 'xml', 'rename': 'ErrorDocument', 'type': 'ErrorDocument'},
        'routing_rules': {'tag': 'xml', 'rename': 'RoutingRules', 'type': 'RoutingRules'},
    }

    _xml_map = {
        'name': 'WebsiteConfiguration'
    }

    _dependency_map = { 
        'IndexDocument': {'new': lambda: IndexDocument()},
        'ErrorDocument': {'new': lambda: ErrorDocument()},
        'RoutingRules': {'new': lambda: RoutingRules()},
    }

    def __init__(
        self,
        index_document: Optional[IndexDocument] = None,
        error_document: Optional[ErrorDocument] = None,
        routing_rules: Optional[RoutingRules] = None,
        **kwargs: Any
    ) -> None:
        """
        index_document (IndexDocument, optional): The container that stores the default homepage.  You must specify at least one of the following containers: IndexDocument, ErrorDocument, and RoutingRules.
        error_document (ErrorDocument, optional): The container that stores the default 404 page.  You must specify at least one of the following containers: IndexDocument, ErrorDocument, and RoutingRules.
        routing_rules (RoutingRules, optional): The container that stores the redirection rules.  You must specify at least one of the following containers: IndexDocument, ErrorDocument, and RoutingRules.
        """
        super().__init__(**kwargs)
        self.index_document = index_document
        self.error_document = error_document
        self.routing_rules = routing_rules





class GetBucketWebsiteRequest(serde.RequestModel):
    """
    The request for the GetBucketWebsite operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetBucketWebsiteResult(serde.ResultModel):
    """
    The request for the GetBucketWebsite operation.
    """

    _attribute_map = { 
        'website_configuration': {'tag': 'output', 'position': 'body', 'rename': 'WebsiteConfiguration', 'type': 'WebsiteConfiguration,xml'},
    }

    _dependency_map = { 
        'WebsiteConfiguration': {'new': lambda: WebsiteConfiguration()},
    }

    def __init__(
        self,
        website_configuration: Optional[WebsiteConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        website_configuration (WebsiteConfiguration, optional): The containers of the website configuration.
        """
        super().__init__(**kwargs)
        self.website_configuration = website_configuration

class PutBucketWebsiteRequest(serde.RequestModel):
    """
    The request for the PutBucketWebsite operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'website_configuration': {'tag': 'input', 'position': 'body', 'rename': 'WebsiteConfiguration', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        website_configuration: Optional[WebsiteConfiguration] = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        website_configuration (WebsiteConfiguration, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.website_configuration = website_configuration


class PutBucketWebsiteResult(serde.ResultModel):
    """
    The request for the PutBucketWebsite operation.
    """

class DeleteBucketWebsiteRequest(serde.RequestModel):
    """
    The request for the DeleteBucketWebsite operation.
    """

    _attribute_map = { 
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        **kwargs: Any
    ) -> None:
        """
        bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class DeleteBucketWebsiteResult(serde.ResultModel):
    """
    The request for the DeleteBucketWebsite operation.
    """

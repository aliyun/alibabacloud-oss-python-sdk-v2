import datetime
from typing import Optional, List, Any, Union
from enum import Enum
from .. import serde


class MetaQueryOrderType(str, Enum):
    """
    A short description of struct
    """

    ASC = 'asc'
    DESC = 'desc'


class MetaQueryAudioStream(serde.Model):
    """
        audio streams
    """

    _attribute_map = {
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'sample_rate': {'tag': 'xml', 'rename': 'SampleRate', 'type': 'int'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'channels': {'tag': 'xml', 'rename': 'Channels', 'type': 'int'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'codec_name': {'tag': 'xml', 'rename': 'CodecName', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryRespAudioStream'
    }

    def __init__(
            self,
            bitrate: Optional[int] = None,
            sample_rate: Optional[int] = None,
            start_time: Optional[float] = None,
            duration: Optional[float] = None,
            channels: Optional[int] = None,
            language: Optional[str] = None,
            codec_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        bitrate (int, optional): The bitrate. Unit: bit/s.
        sample_rate (int, optional): The sampling rate.
        start_time (float, optional): The start time of the video stream.
        duration (float, optional): The duration of the video stream.
        channels (int, optional): The number of sound channels.
        language (str, optional): The language used in the audio stream. The value follows the BCP 47 format.
        codec_name (str, optional): The abbreviated name of the codec.
        """
        super().__init__(**kwargs)
        self.bitrate = bitrate
        self.sample_rate = sample_rate
        self.start_time = start_time
        self.duration = duration
        self.channels = channels
        self.language = language
        self.codec_name = codec_name


class MetaQueryVideoStream(serde.Model):
    """
        video streams.
    """

    _attribute_map = {
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'frame_rate': {'tag': 'xml', 'rename': 'FrameRate', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'frame_count': {'tag': 'xml', 'rename': 'FrameCount', 'type': 'int'},
        'height': {'tag': 'xml', 'rename': 'Height', 'type': 'int'},
        'width': {'tag': 'xml', 'rename': 'Width', 'type': 'int'},
        'codec_name': {'tag': 'xml', 'rename': 'CodecName', 'type': 'str'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'bit_depth': {'tag': 'xml', 'rename': 'BitDepth', 'type': 'int'},
        'pixel_format': {'tag': 'xml', 'rename': 'PixelFormat', 'type': 'str'},
        'color_space': {'tag': 'xml', 'rename': 'ColorSpace', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryRespVideoStream'
    }

    def __init__(
            self,
            bitrate: Optional[int] = None,
            frame_rate: Optional[str] = None,
            start_time: Optional[float] = None,
            duration: Optional[float] = None,
            frame_count: Optional[int] = None,
            height: Optional[int] = None,
            width: Optional[int] = None,
            codec_name: Optional[str] = None,
            language: Optional[str] = None,
            bit_depth: Optional[int] = None,
            pixel_format: Optional[str] = None,
            color_space: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        bitrate (int, optional): The bitrate. Unit: bit/s.
        frame_rate (str, optional): The frame rate of the video stream.
        start_time (float, optional): The start time of the audio stream in seconds.
        duration (float, optional): The duration of the audio stream in seconds.
        frame_count (int, optional): The number of video frames.
        height (int, optional): The image height of the video stream. Unit: pixel.
        width (int, optional): The image width of the video stream. Unit: pixels.
        codec_name (str, optional): The abbreviated name of the codec.
        language (str, optional): The language used in the audio stream. The value follows the BCP 47 format.
        bit_depth (int, optional): The bit depth.
        pixel_format (str, optional): The pixel format of the video stream.
        color_space (str, optional): The color space.
        """
        super().__init__(**kwargs)
        self.bitrate = bitrate
        self.frame_rate = frame_rate
        self.start_time = start_time
        self.duration = duration
        self.frame_count = frame_count
        self.height = height
        self.width = width
        self.codec_name = codec_name
        self.language = language
        self.bit_depth = bit_depth
        self.pixel_format = pixel_format
        self.color_space = color_space


class MetaQuerySubtitle(serde.Model):
    """
        subtitle streams
    """

    _attribute_map = {
        'codec_name': {'tag': 'xml', 'rename': 'CodecName', 'type': 'str'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
    }

    _xml_map = {
        'name': 'MetaQueryRespSubtitle'
    }

    def __init__(
            self,
            codec_name: Optional[str] = None,
            language: Optional[str] = None,
            start_time: Optional[float] = None,
            duration: Optional[float] = None,
            **kwargs: Any
    ) -> None:
        """
        codec_name (str, optional): The abbreviated name of the codec.
        language (str, optional): The language of the subtitle. The value follows the BCP 47 format.
        start_time (float, optional): The start time of the subtitle stream in seconds.
        duration (float, optional): The duration of the subtitle stream in seconds.
        """
        super().__init__(**kwargs)
        self.codec_name = codec_name
        self.language = language
        self.start_time = start_time
        self.duration = duration


class MetaQueryGroup(serde.Model):
    """
        grouped aggregations
    """

    _attribute_map = {
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
        'count': {'tag': 'xml', 'rename': 'Count', 'type': 'int'},
    }

    _xml_map = {
        'name': 'Group'
    }

    def __init__(
            self,
            value: Optional[str] = None,
            count: Optional[int] = None,
            **kwargs: Any
    ) -> None:
        """
        value (str, optional): The value for the grouped aggregation.
        count (int, optional): The number of results in the grouped aggregation.
        """
        super().__init__(**kwargs)
        self.value = value
        self.count = count


class MetaQueryGroups(serde.Model):
    """
        grouped aggregations
    """

    _attribute_map = {
        'groups': {'tag': 'xml', 'rename': 'Group', 'type': '[Group]'},
    }

    _xml_map = {
        'name': 'Groups'
    }

    _dependency_map = {
        'Group': {'new': lambda: MetaQueryGroup()},
    }

    def __init__(
            self,
            groups: Optional[List[MetaQueryGroup]] = None,
            **kwargs: Any
    ) -> None:
        """
        groups (List[Group], optional): The grouped aggregations.
        """
        super().__init__(**kwargs)
        self.groups = groups


class MetaQueryAddress(serde.Model):
    """
        The addresses
    """

    _attribute_map = {
        'township': {'tag': 'xml', 'rename': 'Township', 'type': 'str'},
        'address_line': {'tag': 'xml', 'rename': 'AddressLine', 'type': 'str'},
        'city': {'tag': 'xml', 'rename': 'City', 'type': 'str'},
        'country': {'tag': 'xml', 'rename': 'Country', 'type': 'str'},
        'district': {'tag': 'xml', 'rename': 'District', 'type': 'str'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'province': {'tag': 'xml', 'rename': 'Province', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryRespAddress'
    }

    def __init__(
            self,
            township: Optional[str] = None,
            address_line: Optional[str] = None,
            city: Optional[str] = None,
            country: Optional[str] = None,
            district: Optional[str] = None,
            language: Optional[str] = None,
            province: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        township (str, optional): The street.
        address_line (str, optional): The full address.
        city (str, optional): The city.
        country (str, optional): The country.
        district (str, optional): The district.
        language (str, optional): The language of the address. The value follows the BCP 47 format.
        province (str, optional): The province.
        """
        super().__init__(**kwargs)
        self.township = township
        self.address_line = address_line
        self.city = city
        self.country = country
        self.district = district
        self.language = language
        self.province = province


class MetaQueryAudioStreams(serde.Model):
    """
        audio streams
    """

    _attribute_map = {
        'audio_stream': {'tag': 'xml', 'rename': 'AudioStream', 'type': '[MetaQueryRespAudioStream]'},
    }

    _xml_map = {
        'name': 'AudioStreams'
    }

    _dependency_map = {
        'MetaQueryRespAudioStream': {'new': lambda: MetaQueryAudioStream()},
    }

    def __init__(
            self,
            audio_stream: Optional[List[MetaQueryAudioStream]] = None,
            **kwargs: Any
    ) -> None:
        """
        audio_stream (List[MetaQueryRespAudioStream], optional):  The list of audio streams.
        """
        super().__init__(**kwargs)
        self.audio_stream = audio_stream


class MetaQuerySubtitles(serde.Model):
    """
        subtitle streams
    """

    _attribute_map = {
        'subtitle': {'tag': 'xml', 'rename': 'Subtitle', 'type': '[MetaQueryRespSubtitle]'},
    }

    _xml_map = {
        'name': 'Subtitles'
    }

    _dependency_map = {
        'MetaQueryRespSubtitle': {'new': lambda: MetaQuerySubtitle()},
    }

    def __init__(
            self,
            subtitle: Optional[List[MetaQuerySubtitle]] = None,
            **kwargs: Any
    ) -> None:
        """
        subtitle (List[MetaQueryRespSubtitle], optional): The subtitle streams.
        """
        super().__init__(**kwargs)
        self.subtitle = subtitle


class MetaQueryAddresses(serde.Model):
    """
        The addresses
    """

    _attribute_map = {
        'address': {'tag': 'xml', 'rename': 'Address', 'type': '[MetaQueryRespAddress]'},
    }

    _xml_map = {
        'name': 'Addresses'
    }

    _dependency_map = {
        'MetaQueryRespAddress': {'new': lambda: MetaQueryAddress()},
    }

    def __init__(
            self,
            address: Optional[List[MetaQueryAddress]] = None,
            **kwargs: Any
    ) -> None:
        """
        address (List[MetaQueryRespAddress], optional): The addresses
        """
        super().__init__(**kwargs)
        self.address = address


class MetaQueryVideoStreams(serde.Model):
    """
        video streams
    """

    _attribute_map = {
        'video_stream': {'tag': 'xml', 'rename': 'VideoStream', 'type': '[MetaQueryRespVideoStream]'},
    }

    _xml_map = {
        'name': 'VideoStreams'
    }

    _dependency_map = {
        'MetaQueryRespVideoStream': {'new': lambda: MetaQueryVideoStream()},
    }

    def __init__(
            self,
            video_stream: Optional[List[MetaQueryVideoStream]] = None,
            **kwargs: Any
    ) -> None:
        """
        video_stream (List[MetaQueryRespVideoStream], optional): The list of video streams.
        """
        super().__init__(**kwargs)
        self.video_stream = video_stream



class MetaQueryStatus(serde.Model):
    """
    The container that stores the metadata information.
    """

    _attribute_map = { 
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'update_time': {'tag': 'xml', 'rename': 'UpdateTime', 'type': 'str'},
        'state': {'tag': 'xml', 'rename': 'State', 'type': 'str'},
        'phase': {'tag': 'xml', 'rename': 'Phase', 'type': 'str'},
        'meta_query_mode': {'tag': 'xml', 'rename': 'MetaQueryMode', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryStatus'
    }

    def __init__(
        self,
        create_time: Optional[str] = None,
        update_time: Optional[str] = None,
        state: Optional[str] = None,
        phase: Optional[str] = None,
        meta_query_mode: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            create_time (str, optional): The time when the metadata index library was created. The value follows the RFC 3339 standard in the YYYY-MM-DDTHH:mm:ss+TIMEZONE format. YYYY-MM-DD indicates the year, month, and day. T indicates the beginning of the time element. HH:mm:ss indicates the hour, minute, and second. TIMEZONE indicates the time zone.
            update_time (str, optional): The time when the metadata index library was updated. The value follows the RFC 3339 standard in the YYYY-MM-DDTHH:mm:ss+TIMEZONE format. YYYY-MM-DD indicates the year, month, and day. T indicates the beginning of the time element. HH:mm:ss indicates the hour, minute, and second. TIMEZONE indicates the time zone.
            state (str, optional): The status of the metadata index library. Valid values:- Ready: The metadata index library is being prepared after it is created.In this case, the metadata index library cannot be used to query data.- Stop: The metadata index library is paused.- Running: The metadata index library is running.- Retrying: The metadata index library failed to be created and is being created again.- Failed: The metadata index library failed to be created.- Deleted: The metadata index library is deleted.
            phase (str, optional): The scan type. Valid values:- FullScanning: Full scanning is in progress.- IncrementalScanning: Incremental scanning is in progress.
            meta_query_mode (str, optional): Retrieval modes: basic: Scalar search, semantic: Vector search.
        """
        super().__init__(**kwargs)
        self.create_time = create_time
        self.update_time = update_time
        self.state = state
        self.phase = phase
        self.meta_query_mode = meta_query_mode


class MetaQueryAggregation(serde.Model):
    """
    The container that stores the information about a single aggregate operation.
    """

    _attribute_map = { 
        'field': {'tag': 'xml', 'rename': 'Field', 'type': 'str'},
        'operation': {'tag': 'xml', 'rename': 'Operation', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'float'},
        'groups': {'tag': 'xml', 'rename': 'Groups', 'type': 'Groups'},
    }

    _xml_map = {
        'name': 'Aggregation'
    }

    _dependency_map = {
        'Groups': {'new': lambda: MetaQueryGroups()},
    }

    def __init__(
        self,
        field: Optional[str] = None,
        operation: Optional[str] = None,
        value: Optional[float] = None,
        groups: Optional[MetaQueryGroups] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            field (str, optional): The field name.
            operation (str, optional): The operator for aggregate operations.*   min*   max*   average*   sum*   count*   distinct*   group
            value (float, optional): The result of the aggregate operation.
            groups (Groups, optional): The grouped aggregations.
        """
        super().__init__(**kwargs)
        self.field = field
        self.operation = operation
        self.value = value
        self.groups = groups


class MetaQueryTagging(serde.Model):
    """
    The container that stores the tag information.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQueryTagging'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The tag key.
            value (str, optional): The tag value.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


class MetaQueryUserMeta(serde.Model):
    """
    The container that stores user metadata.
    """

    _attribute_map = { 
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'UserMeta'
    }

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            key (str, optional): The key of the user metadata item.
            value (str, optional): The value of the user metadata item.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


class MetaQueryOSSTagging(serde.Model):
    """
    The tags.
    """

    _attribute_map = { 
        'taggings': {'tag': 'xml', 'rename': 'Tagging', 'type': '[MetaQueryTagging]'},
    }

    _xml_map = {
        'name': 'OSSTagging'
    }

    _dependency_map = { 
        'MetaQueryTagging': {'new': lambda: MetaQueryTagging()},
    }

    def __init__(
        self,
        taggings: Optional[List[MetaQueryTagging]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            taggings (List[MetaQueryTagging], optional): The tags.
        """
        super().__init__(**kwargs)
        self.taggings = taggings


class MetaQueryAggregations(serde.Model):
    """
    The container that stores the information about aggregate operations.
    """

    _attribute_map = { 
        'aggregations': {'tag': 'xml', 'rename': 'Aggregation', 'type': '[Aggregation]'},
    }

    _xml_map = {
        'name': 'Aggregations'
    }

    _dependency_map = { 
        'Aggregation': {'new': lambda: MetaQueryAggregation()},
    }

    def __init__(
        self,
        aggregations: Optional[List[MetaQueryAggregation]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            aggregations (List[Aggregation], optional): The container that stores the information about aggregate operations.
        """
        super().__init__(**kwargs)
        self.aggregations = aggregations

class MetaQueryMediaTypes(serde.Model):
    """
    Multimedia metadata retrieval criteria.
    """

    _attribute_map = {
        'media_type': {'tag': 'xml', 'rename': 'MediaType', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'MediaTypes'
    }

    def __init__(
        self,
        media_type: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            media_type (List[str], optional): The type of multimedia that you want to query. Valid values: image, video, audio, document
        """
        super().__init__(**kwargs)
        self.media_type = media_type


class MetaQuery(serde.Model):
    """
    The container that stores the query conditions.
    """

    _attribute_map = { 
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'Aggregations'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str'},
        'max_results': {'tag': 'xml', 'rename': 'MaxResults', 'type': 'int'},
        'query': {'tag': 'xml', 'rename': 'Query', 'type': 'str'},
        'sort': {'tag': 'xml', 'rename': 'Sort', 'type': 'str'},
        'order': {'tag': 'xml', 'rename': 'Order', 'type': 'str'},
        'media_types': {'tag': 'xml', 'rename': 'MediaTypes', 'type': 'MetaQueryMediaTypes'},
        'simple_query': {'tag': 'xml', 'rename': 'SimpleQuery', 'type': 'str'},
    }

    _xml_map = {
        'name': 'MetaQuery'
    }

    _dependency_map = { 
        'Aggregations': {'new': lambda: MetaQueryAggregations()},
    }

    def __init__(
        self,
        aggregations: Optional[MetaQueryAggregations] = None,
        next_token: Optional[str] = None,
        max_results: Optional[int] = None,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        order: Optional[Union[str, MetaQueryOrderType]] = None,
        media_types: Optional[MetaQueryMediaTypes] = None,
        simple_query: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            aggregations (Aggregations, optional): The container that stores the information about aggregate operations.
            next_token (str, optional): The pagination token used to obtain information in the next request. The object information is returned in alphabetical order starting from the value of NextToken.
            max_results (int, optional): The maximum number of objects to return. Valid values: 0 to 100. If this parameter is not set or is set to 0, up to 100 objects are returned.
            query (str, optional): The query conditions. A query condition includes the following elements:*   Operation: the operator. Valid values: eq (equal to), gt (greater than), gte (greater than or equal to), lt (less than), lte (less than or equal to), match (fuzzy query), prefix (prefix query), and (AND), or (OR), and not (NOT).*   Field: the field name.*   Value: the field value.*   SubQueries: the subquery conditions. Options that are included in this element are the same as those of simple query. You need to set subquery conditions only when Operation is set to and, or, or not.
            sort (str, optional): The field based on which the results are sorted.
            order (str | MetaQueryOrderType, optional): The sort order.
            media_types (MetaQueryMediaTypes, optional): Container for multimedia metadata retrieval conditions
            simple_query (str, optional): The query conditions
        """
        super().__init__(**kwargs)
        self.aggregations = aggregations
        self.next_token = next_token
        self.max_results = max_results
        self.query = query
        self.sort = sort
        self.order = order
        self.media_types = media_types
        self.simple_query = simple_query



class MetaQueryOSSUserMeta(serde.Model):
    """
    The user metadata items.
    """

    _attribute_map = { 
        'user_metas': {'tag': 'xml', 'rename': 'UserMeta', 'type': '[UserMeta]'},
    }

    _xml_map = {
        'name': 'OSSUserMeta'
    }

    _dependency_map = { 
        'UserMeta': {'new': lambda: MetaQueryUserMeta()},
    }

    def __init__(
        self,
        user_metas: Optional[List[MetaQueryUserMeta]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            user_metas (List[UserMeta], optional): The user metadata items.
        """
        super().__init__(**kwargs)
        self.user_metas = user_metas


class MetaQueryFile(serde.Model):
    """
    File information.
    """

    _attribute_map = {
        'file_modified_time': {'tag': 'xml', 'rename': 'FileModifiedTime', 'type': 'str'},
        'etag': {'tag': 'xml', 'rename': 'ETag', 'type': 'str'},
        'server_side_encryption': {'tag': 'xml', 'rename': 'ServerSideEncryption', 'type': 'str'},
        'oss_tagging_count': {'tag': 'xml', 'rename': 'OSSTaggingCount', 'type': 'int'},
        'oss_tagging': {'tag': 'xml', 'rename': 'OSSTagging', 'type': 'OSSTagging'},
        'oss_user_meta': {'tag': 'xml', 'rename': 'OSSUserMeta', 'type': 'OSSUserMeta'},
        'filename': {'tag': 'xml', 'rename': 'Filename', 'type': 'str'},
        'size': {'tag': 'xml', 'rename': 'Size', 'type': 'int'},
        'oss_object_type': {'tag': 'xml', 'rename': 'OSSObjectType', 'type': 'str'},
        'oss_storage_class': {'tag': 'xml', 'rename': 'OSSStorageClass', 'type': 'str'},
        'object_acl': {'tag': 'xml', 'rename': 'ObjectACL', 'type': 'str'},
        'oss_crc64': {'tag': 'xml', 'rename': 'OSSCRC64', 'type': 'str'},
        'server_side_encryption_customer_algorithm': {'tag': 'xml', 'rename': 'ServerSideEncryptionCustomerAlgorithm', 'type': 'str'},
        'cache_control': {'tag': 'xml', 'rename': 'CacheControl', 'type': 'str'},
        'content_disposition': {'tag': 'xml', 'rename': 'ContentDisposition', 'type': 'str'},
        'content_type': {'tag': 'xml', 'rename': 'ContentType', 'type': 'str'},
        'lat_long': {'tag': 'xml', 'rename': 'LatLong', 'type': 'str'},
        'server_side_encryption_key_id': {'tag': 'xml', 'rename': 'ServerSideEncryptionKeyId', 'type': 'str'},
        'video_height': {'tag': 'xml', 'rename': 'VideoHeight', 'type': 'int'},
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'meta_query_audio_streams': {'tag': 'xml', 'rename': 'AudioStreams', 'type': 'AudioStreams'},
        'meta_query_addresses': {'tag': 'xml', 'rename': 'Addresses', 'type': 'Addresses'},
        'uri': {'tag': 'xml', 'rename': 'URI', 'type': 'str'},
        'access_control_request_method': {'tag': 'xml', 'rename': 'AccessControlRequestMethod', 'type': 'str'},
        'image_width': {'tag': 'xml', 'rename': 'ImageWidth', 'type': 'int'},
        'title': {'tag': 'xml', 'rename': 'Title', 'type': 'str'},
        'access_control_allow_origin': {'tag': 'xml', 'rename': 'AccessControlAllowOrigin', 'type': 'str'},
        'image_height': {'tag': 'xml', 'rename': 'ImageHeight', 'type': 'int'},
        'album_artist': {'tag': 'xml', 'rename': 'AlbumArtist', 'type': 'str'},
        'content_encoding': {'tag': 'xml', 'rename': 'ContentEncoding', 'type': 'str'},
        'content_language': {'tag': 'xml', 'rename': 'ContentLanguage', 'type': 'str'},
        'artist': {'tag': 'xml', 'rename': 'Artist', 'type': 'str'},
        'performer': {'tag': 'xml', 'rename': 'Performer', 'type': 'str'},
        'meta_query_video_streams': {'tag': 'xml', 'rename': 'VideoStreams', 'type': 'VideoStreams'},
        'produce_time': {'tag': 'xml', 'rename': 'ProduceTime', 'type': 'str'},
        'video_width': {'tag': 'xml', 'rename': 'VideoWidth', 'type': 'int'},
        'album': {'tag': 'xml', 'rename': 'Album', 'type': 'str'},
        'media_type': {'tag': 'xml', 'rename': 'MediaType', 'type': 'str'},
        'oss_expiration': {'tag': 'xml', 'rename': 'OSSExpiration', 'type': 'str'},
        'server_side_data_encryption': {'tag': 'xml', 'rename': 'ServerSideDataEncryption', 'type': 'str'},
        'composer': {'tag': 'xml', 'rename': 'Composer', 'type': 'str'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'meta_query_subtitles': {'tag': 'xml', 'rename': 'Subtitles', 'type': 'Subtitles'},
    }

    _xml_map = {
        'name': 'File'
    }

    _dependency_map = {
        'OSSTagging': {'new': lambda: MetaQueryOSSTagging()},
        'OSSUserMeta': {'new': lambda: MetaQueryOSSUserMeta()},
        'AudioStreams': {'new': lambda: MetaQueryAudioStreams()},
        'Addresses': {'new': lambda: MetaQueryAddresses()},
        'VideoStreams': {'new': lambda: MetaQueryVideoStreams()},
        'Subtitles': {'new': lambda: MetaQuerySubtitles()},
    }

    def __init__(
        self,
        file_modified_time: Optional[str] = None,
        etag: Optional[str] = None,
        server_side_encryption: Optional[str] = None,
        oss_tagging_count: Optional[int] = None,
        oss_tagging: Optional[MetaQueryOSSTagging] = None,
        oss_user_meta: Optional[MetaQueryOSSUserMeta] = None,
        filename: Optional[str] = None,
        size: Optional[int] = None,
        oss_object_type: Optional[str] = None,
        oss_storage_class: Optional[str] = None,
        object_acl: Optional[str] = None,
        oss_crc64: Optional[str] = None,
        server_side_encryption_customer_algorithm: Optional[str] = None,
        cache_control: Optional[str] = None,
        content_disposition: Optional[str] = None,
        content_type: Optional[str] = None,
        lat_long: Optional[str] = None,
        server_side_encryption_key_id: Optional[str] = None,
        video_height: Optional[int] = None,
        bitrate: Optional[int] = None,
        meta_query_audio_streams: Optional[MetaQueryAudioStreams] = None,
        meta_query_addresses: Optional[MetaQueryAddresses] = None,
        uri: Optional[str] = None,
        access_control_request_method: Optional[str] = None,
        image_width: Optional[int] = None,
        title: Optional[str] = None,
        access_control_allow_origin: Optional[str] = None,
        image_height: Optional[int] = None,
        album_artist: Optional[str] = None,
        content_encoding: Optional[str] = None,
        content_language: Optional[str] = None,
        artist: Optional[str] = None,
        performer: Optional[str] = None,
        meta_query_video_streams: Optional[MetaQueryVideoStreams] = None,
        produce_time: Optional[str] = None,
        video_width: Optional[int] = None,
        album: Optional[str] = None,
        media_type: Optional[str] = None,
        oss_expiration: Optional[str] = None,
        server_side_data_encryption: Optional[str] = None,
        composer: Optional[str] = None,
        duration: Optional[float] = None,
        meta_query_subtitles: Optional[MetaQuerySubtitles] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            file_modified_time (str, optional): The time when the object was last modified.
            etag (str, optional): The ETag of the object.
            server_side_encryption (str, optional): The server-side encryption algorithm used when the object was created.
            oss_tagging_count (int, optional): The number of the tags of the object.
            oss_tagging (OSSTagging, optional): The tags.
            oss_user_meta (OSSUserMeta, optional): The user metadata items.
            filename (str, optional): The full path of the object.
            size (int, optional): The object size.
            oss_object_type (str, optional): The type of the object.Valid values:
                Multipart: The object is uploaded by using multipart upload.
                Symlink: The object is a symbolic link that was created by calling the PutSymlink operation.
                Appendable: The object is uploaded by using AppendObject.
                Normal: The object is uploaded by using PutObject.
            oss_storage_class (str, optional): The storage class of the object.Valid values:
                Archive: the Archive storage class.
                ColdArchive: the Cold Archive storage class.
                IA: the Infrequent Access (IA) storage class.
                Standard: The Standard storage class
            object_acl (str, optional): The access control list (ACL) of the object.Valid values:
                default: the ACL of the bucket.
                private: private.
                public-read: public-read.
                public-read-write: public-read-write.
            oss_crc64 (str, optional): The CRC-64 value of the object.
            server_side_encryption_customer_algorithm (str, optional): The server-side encryption of the object.
            cache_control (str, optional): The web page caching behavior that is performed when the object is downloaded.
            content_disposition (str, optional): The name of the object when it is downloaded.
            content_type (str, optional): The Multipurpose Internet Mail Extensions (MIME) type of the object.
            lat_long (str, optional): The longitude and latitude information.
            server_side_encryption_key_id (str, optional): The ID of the customer master key (CMK) that is managed by Key Management Service (KMS).
            video_height (int, optional): The height of the video image. Unit: pixel.
            bitrate (int, optional): The bitrate. Unit: bit/s.
            meta_query_audio_streams (AudioStreams, optional): The list of audio streams.
            meta_query_addresses (Addresses, optional): The addresses.
            uri (str, optional): The full path of the object.
            access_control_request_method (str, optional): The cross-origin request methods that are allowed.
            image_width (int, optional): The width of the image. Unit: pixel.
            title (str, optional): The title of the object.
            access_control_allow_origin (str, optional): The origins allowed in cross-origin requests.
            image_height (int, optional): The height of the image. Unit: pixel.
            album_artist (str, optional): The singer.
            content_encoding (str, optional): The content encoding format of the object when the object is downloaded.
            content_language (str, optional): The language of the object content.
            artist (str, optional): The artist.
            performer (str, optional): The player.
            meta_query_video_streams (VideoStreams, optional): The list of video streams.
            produce_time (str, optional): The time when the image or video was taken.
            video_width (int, optional): The width of the video image. Unit: pixel.
            album (str, optional): The album.
            media_type (str, optional): The type of multimedia.
            oss_expiration (str, optional): The time when the object expires.
            server_side_data_encryption (str, optional): The algorithm used to encrypt objects.
            composer (str, optional): The composer.
            duration (float, optional): The total duration of the video. Unit: seconds.
            meta_query_subtitles (Subtitles, optional): The list of subtitle streams.
        """
        super().__init__(**kwargs)
        self.file_modified_time = file_modified_time
        self.etag = etag
        self.server_side_encryption = server_side_encryption
        self.oss_tagging_count = oss_tagging_count
        self.oss_tagging = oss_tagging
        self.oss_user_meta = oss_user_meta
        self.filename = filename
        self.size = size
        self.oss_object_type = oss_object_type
        self.oss_storage_class = oss_storage_class
        self.object_acl = object_acl
        self.oss_crc64 = oss_crc64
        self.server_side_encryption_customer_algorithm = server_side_encryption_customer_algorithm
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_type = content_type
        self.lat_long = lat_long
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.video_height = video_height
        self.bitrate = bitrate
        self.meta_query_audio_streams = meta_query_audio_streams
        self.meta_query_addresses = meta_query_addresses
        self.uri = uri
        self.access_control_request_method = access_control_request_method
        self.image_width = image_width
        self.title = title
        self.access_control_allow_origin = access_control_allow_origin
        self.image_height = image_height
        self.album_artist = album_artist
        self.content_encoding = content_encoding
        self.content_language = content_language
        self.artist = artist
        self.performer = performer
        self.meta_query_video_streams = meta_query_video_streams
        self.produce_time = produce_time
        self.video_width = video_width
        self.album = album
        self.media_type = media_type
        self.oss_expiration = oss_expiration
        self.server_side_data_encryption = server_side_data_encryption
        self.composer = composer
        self.duration = duration
        self.meta_query_subtitles = meta_query_subtitles


class MetaQueryFiles(serde.Model):
    """
    The list of file information.
    """

    _attribute_map = { 
        'file': {'tag': 'xml', 'rename': 'File', 'type': '[MetaQueryFile]'},
    }

    _xml_map = {
        'name': 'Files'
    }

    _dependency_map = { 
        'File': {'new': lambda: MetaQueryFile()},
    }

    def __init__(
        self,
        file: Optional[List[MetaQueryFile]] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            file (List[MetaQueryFile], optional):
        """
        super().__init__(**kwargs)
        self.file = file




class OpenMetaQueryRequest(serde.RequestModel):
    """
    The request for the OpenMetaQuery operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'mode': {'tag': 'input', 'position': 'query', 'rename': 'mode', 'type': 'str'},
    }

    def __init__(
        self,
        bucket: str = None,
        mode: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            mode (str, optional): Specify search mode
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.mode = mode


class OpenMetaQueryResult(serde.ResultModel):
    """
    The request for the OpenMetaQuery operation.
    """


class GetMetaQueryStatusRequest(serde.RequestModel):
    """
    The request for the GetMetaQueryStatus operation.
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
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class GetMetaQueryStatusResult(serde.ResultModel):
    """
    The request for the GetMetaQueryStatus operation.
    """

    _attribute_map = { 
        'meta_query_status': {'tag': 'output', 'position': 'body', 'rename': 'MetaQueryStatus', 'type': 'MetaQueryStatus,xml'},
    }

    _dependency_map = { 
        'MetaQueryStatus': {'new': lambda: MetaQueryStatus()},
    }

    def __init__(
        self,
        meta_query_status: Optional[MetaQueryStatus] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            meta_query_status (MetaQueryStatus, optional): The container that stores the metadata information.
        """
        super().__init__(**kwargs)
        self.meta_query_status = meta_query_status



class DoMetaQueryRequest(serde.RequestModel):
    """
    The request for the DoMetaQuery operation.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'mode': {'tag': 'input', 'position': 'query', 'rename': 'mode', 'type': 'str'},
        'meta_query': {'tag': 'input', 'position': 'body', 'rename': 'MetaQuery', 'type': 'xml'},
    }

    def __init__(
        self,
        bucket: str = None,
        mode: Optional[str] = None,
        meta_query: Optional[MetaQuery] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            mode (str, optional): Specify search mode
            meta_query (MetaQuery, optional): The request body schema.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.mode = mode
        self.meta_query = meta_query


class DoMetaQueryResult(serde.ResultModel):
    """
    The request for the DoMetaQuery operation.
    """

    _attribute_map = {
        'files': {'tag': 'xml', 'rename': 'Files', 'type': 'Files,xml'},
        'aggregations': {'tag': 'xml', 'rename': 'Aggregations', 'type': 'Aggregations,xml'},
        'next_token': {'tag': 'xml', 'rename': 'NextToken', 'type': 'str,xml'},
    }

    _dependency_map = {
        'Files': {'new': lambda: MetaQueryFiles()},
        'Aggregations': {'new': lambda: MetaQueryAggregations()},
    }

    def __init__(
        self,
        files: Optional[MetaQueryFiles] = None,
        aggregations: Optional[MetaQueryAggregations] = None,
        next_token: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            files (Files, optional): The list of file information.
            aggregations (Aggregations, optional): The list of file information.
            next_token (str, optional): The token that is used for the next query when the total number of objects exceeds the value of MaxResults.The value of NextToken is used to return the unreturned results in the next query.This parameter has a value only when not all objects are returned.
        """
        super().__init__(**kwargs)
        self.files = files
        self.aggregations = aggregations
        self.next_token = next_token


class CloseMetaQueryRequest(serde.RequestModel):
    """
    The request for the CloseMetaQuery operation.
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
        Args:
            bucket (str, required): The name of the bucket.
        """
        super().__init__(**kwargs)
        self.bucket = bucket


class CloseMetaQueryResult(serde.ResultModel):
    """
    The request for the CloseMetaQuery operation.
    """

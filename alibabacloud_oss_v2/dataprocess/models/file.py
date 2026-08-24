# -*- coding: utf-8 -*-
"""File models for OSS DataProcess module.

These models describe the ``File`` element returned by the DoMetaQuery,
SimpleQuery and SemanticQuery operations, aligned with the Java SDK.
"""

from typing import Optional, List, Any
from ... import serde


class PointInt64(serde.Model):
    """A 2D point with int64 coordinates."""

    _attribute_map = {
        'x': {'tag': 'xml', 'rename': 'X', 'type': 'int'},
        'y': {'tag': 'xml', 'rename': 'Y', 'type': 'int'},
    }

    _xml_map = {
        'name': 'PointInt64'
    }

    def __init__(
            self,
            x: Optional[int] = None,
            y: Optional[int] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            x (int, optional): The x coordinate.
            y (int, optional): The y coordinate.
        """
        super().__init__(**kwargs)
        self.x = x
        self.y = y


class Boundary(serde.Model):
    """A bounding region within an image."""

    _attribute_map = {
        'width': {'tag': 'xml', 'rename': 'Width', 'type': 'int'},
        'height': {'tag': 'xml', 'rename': 'Height', 'type': 'int'},
        'left': {'tag': 'xml', 'rename': 'Left', 'type': 'int'},
        'top': {'tag': 'xml', 'rename': 'Top', 'type': 'int'},
        'polygon': {'tag': 'xml', 'rename': 'Polygon/PointInt64', 'type': '[PointInt64]'},
    }

    _xml_map = {
        'name': 'Boundary'
    }

    def __init__(
            self,
            width: Optional[int] = None,
            height: Optional[int] = None,
            left: Optional[int] = None,
            top: Optional[int] = None,
            polygon: Optional[List[PointInt64]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            width (int, optional): The width of the boundary.
            height (int, optional): The height of the boundary.
            left (int, optional): The left offset of the boundary.
            top (int, optional): The top offset of the boundary.
            polygon (List[PointInt64], optional): The polygon points of the boundary.
        """
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.polygon = polygon


class HeadPose(serde.Model):
    """Head pose estimation of a figure."""

    _attribute_map = {
        'pitch': {'tag': 'xml', 'rename': 'Pitch', 'type': 'float'},
        'roll': {'tag': 'xml', 'rename': 'Roll', 'type': 'float'},
        'yaw': {'tag': 'xml', 'rename': 'Yaw', 'type': 'float'},
    }

    _xml_map = {
        'name': 'HeadPose'
    }

    def __init__(
            self,
            pitch: Optional[float] = None,
            roll: Optional[float] = None,
            yaw: Optional[float] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            pitch (float, optional): The pitch angle.
            roll (float, optional): The roll angle.
            yaw (float, optional): The yaw angle.
        """
        super().__init__(**kwargs)
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw


class Address(serde.Model):
    """Address information extracted from a file."""

    _attribute_map = {
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'address_line': {'tag': 'xml', 'rename': 'AddressLine', 'type': 'str'},
        'country': {'tag': 'xml', 'rename': 'Country', 'type': 'str'},
        'province': {'tag': 'xml', 'rename': 'Province', 'type': 'str'},
        'city': {'tag': 'xml', 'rename': 'City', 'type': 'str'},
        'district': {'tag': 'xml', 'rename': 'District', 'type': 'str'},
        'township': {'tag': 'xml', 'rename': 'Township', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Address'
    }

    def __init__(
            self,
            language: Optional[str] = None,
            address_line: Optional[str] = None,
            country: Optional[str] = None,
            province: Optional[str] = None,
            city: Optional[str] = None,
            district: Optional[str] = None,
            township: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            language (str, optional): The language of the address.
            address_line (str, optional): The full address line.
            country (str, optional): The country.
            province (str, optional): The province.
            city (str, optional): The city.
            district (str, optional): The district.
            township (str, optional): The township.
        """
        super().__init__(**kwargs)
        self.language = language
        self.address_line = address_line
        self.country = country
        self.province = province
        self.city = city
        self.district = district
        self.township = township


class Figure(serde.Model):
    """A figure (person) detected in a file."""

    _attribute_map = {
        'figure_id': {'tag': 'xml', 'rename': 'FigureId', 'type': 'str'},
        'figure_confidence': {'tag': 'xml', 'rename': 'FigureConfidence', 'type': 'float'},
        'figure_cluster_id': {'tag': 'xml', 'rename': 'FigureClusterId', 'type': 'str'},
        'figure_cluster_confidence': {'tag': 'xml', 'rename': 'FigureClusterConfidence', 'type': 'float'},
        'figure_type': {'tag': 'xml', 'rename': 'FigureType', 'type': 'str'},
        'age': {'tag': 'xml', 'rename': 'Age', 'type': 'int'},
        'age_sd': {'tag': 'xml', 'rename': 'AgeSD', 'type': 'float'},
        'gender': {'tag': 'xml', 'rename': 'Gender', 'type': 'str'},
        'gender_confidence': {'tag': 'xml', 'rename': 'GenderConfidence', 'type': 'float'},
        'emotion': {'tag': 'xml', 'rename': 'Emotion', 'type': 'str'},
        'emotion_confidence': {'tag': 'xml', 'rename': 'EmotionConfidence', 'type': 'float'},
        'face_quality': {'tag': 'xml', 'rename': 'FaceQuality', 'type': 'float'},
        'boundary': {'tag': 'xml', 'rename': 'Boundary', 'type': 'Boundary'},
        'mouth': {'tag': 'xml', 'rename': 'Mouth', 'type': 'str'},
        'mouth_confidence': {'tag': 'xml', 'rename': 'MouthConfidence', 'type': 'float'},
        'beard': {'tag': 'xml', 'rename': 'Beard', 'type': 'str'},
        'beard_confidence': {'tag': 'xml', 'rename': 'BeardConfidence', 'type': 'float'},
        'hat': {'tag': 'xml', 'rename': 'Hat', 'type': 'str'},
        'hat_confidence': {'tag': 'xml', 'rename': 'HatConfidence', 'type': 'float'},
        'mask': {'tag': 'xml', 'rename': 'Mask', 'type': 'str'},
        'mask_confidence': {'tag': 'xml', 'rename': 'MaskConfidence', 'type': 'float'},
        'glasses': {'tag': 'xml', 'rename': 'Glasses', 'type': 'str'},
        'glasses_confidence': {'tag': 'xml', 'rename': 'GlassesConfidence', 'type': 'float'},
        'sharpness': {'tag': 'xml', 'rename': 'Sharpness', 'type': 'float'},
        'attractive': {'tag': 'xml', 'rename': 'Attractive', 'type': 'float'},
        'head_pose': {'tag': 'xml', 'rename': 'HeadPose', 'type': 'HeadPose'},
    }

    _xml_map = {
        'name': 'Figure'
    }

    def __init__(
            self,
            figure_id: Optional[str] = None,
            figure_confidence: Optional[float] = None,
            figure_cluster_id: Optional[str] = None,
            figure_cluster_confidence: Optional[float] = None,
            figure_type: Optional[str] = None,
            age: Optional[int] = None,
            age_sd: Optional[float] = None,
            gender: Optional[str] = None,
            gender_confidence: Optional[float] = None,
            emotion: Optional[str] = None,
            emotion_confidence: Optional[float] = None,
            face_quality: Optional[float] = None,
            boundary: Optional[Boundary] = None,
            mouth: Optional[str] = None,
            mouth_confidence: Optional[float] = None,
            beard: Optional[str] = None,
            beard_confidence: Optional[float] = None,
            hat: Optional[str] = None,
            hat_confidence: Optional[float] = None,
            mask: Optional[str] = None,
            mask_confidence: Optional[float] = None,
            glasses: Optional[str] = None,
            glasses_confidence: Optional[float] = None,
            sharpness: Optional[float] = None,
            attractive: Optional[float] = None,
            head_pose: Optional[HeadPose] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            figure_id (str, optional): The ID of the figure.
            figure_confidence (float, optional): The confidence of the figure.
            figure_cluster_id (str, optional): The cluster ID of the figure.
            figure_cluster_confidence (float, optional): The cluster confidence of the figure.
            figure_type (str, optional): The type of the figure.
            age (int, optional): The estimated age.
            age_sd (float, optional): The standard deviation of the estimated age.
            gender (str, optional): The estimated gender.
            gender_confidence (float, optional): The confidence of the estimated gender.
            emotion (str, optional): The detected emotion.
            emotion_confidence (float, optional): The confidence of the detected emotion.
            face_quality (float, optional): The face quality score.
            boundary (Boundary, optional): The boundary of the figure.
            mouth (str, optional): The mouth state.
            mouth_confidence (float, optional): The confidence of the mouth state.
            beard (str, optional): The beard state.
            beard_confidence (float, optional): The confidence of the beard state.
            hat (str, optional): The hat state.
            hat_confidence (float, optional): The confidence of the hat state.
            mask (str, optional): The mask state.
            mask_confidence (float, optional): The confidence of the mask state.
            glasses (str, optional): The glasses state.
            glasses_confidence (float, optional): The confidence of the glasses state.
            sharpness (float, optional): The sharpness score.
            attractive (float, optional): The attractive score.
            head_pose (HeadPose, optional): The head pose of the figure.
        """
        super().__init__(**kwargs)
        self.figure_id = figure_id
        self.figure_confidence = figure_confidence
        self.figure_cluster_id = figure_cluster_id
        self.figure_cluster_confidence = figure_cluster_confidence
        self.figure_type = figure_type
        self.age = age
        self.age_sd = age_sd
        self.gender = gender
        self.gender_confidence = gender_confidence
        self.emotion = emotion
        self.emotion_confidence = emotion_confidence
        self.face_quality = face_quality
        self.boundary = boundary
        self.mouth = mouth
        self.mouth_confidence = mouth_confidence
        self.beard = beard
        self.beard_confidence = beard_confidence
        self.hat = hat
        self.hat_confidence = hat_confidence
        self.mask = mask
        self.mask_confidence = mask_confidence
        self.glasses = glasses
        self.glasses_confidence = glasses_confidence
        self.sharpness = sharpness
        self.attractive = attractive
        self.head_pose = head_pose


class Clip(serde.Model):
    """A time clip of a label."""

    _attribute_map = {
        'time_range': {'tag': 'xml', 'rename': 'TimeRange', 'type': '[int]'},
    }

    _xml_map = {
        'name': 'Clip'
    }

    def __init__(
            self,
            time_range: Optional[List[int]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            time_range (List[int], optional): The time range of the clip in milliseconds.
        """
        super().__init__(**kwargs)
        self.time_range = time_range


class Label(serde.Model):
    """A label attached to a file."""

    _attribute_map = {
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'label_name': {'tag': 'xml', 'rename': 'LabelName', 'type': 'str'},
        'label_level': {'tag': 'xml', 'rename': 'LabelLevel', 'type': 'int'},
        'label_confidence': {'tag': 'xml', 'rename': 'LabelConfidence', 'type': 'float'},
        'parent_label_name': {'tag': 'xml', 'rename': 'ParentLabelName', 'type': 'str'},
        'centric_score': {'tag': 'xml', 'rename': 'CentricScore', 'type': 'float'},
        'label_alias': {'tag': 'xml', 'rename': 'LabelAlias', 'type': 'str'},
        'clips': {'tag': 'xml', 'rename': 'Clips', 'type': 'Clips'},
    }

    _xml_map = {
        'name': 'Label'
    }

    def __init__(
            self,
            language: Optional[str] = None,
            label_name: Optional[str] = None,
            label_level: Optional[int] = None,
            label_confidence: Optional[float] = None,
            parent_label_name: Optional[str] = None,
            centric_score: Optional[float] = None,
            label_alias: Optional[str] = None,
            clips: Optional['Clips'] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            language (str, optional): The language of the label.
            label_name (str, optional): The name of the label.
            label_level (int, optional): The level of the label.
            label_confidence (float, optional): The confidence of the label.
            parent_label_name (str, optional): The name of the parent label.
            centric_score (float, optional): The centric score of the label.
            label_alias (str, optional): The alias of the label.
            clips (Clips, optional): The clips of the label.
        """
        super().__init__(**kwargs)
        self.language = language
        self.label_name = label_name
        self.label_level = label_level
        self.label_confidence = label_confidence
        self.parent_label_name = parent_label_name
        self.centric_score = centric_score
        self.label_alias = label_alias
        self.clips = clips


class ImageScore(serde.Model):
    """Quality score of an image."""

    _attribute_map = {
        'overall_quality_score': {'tag': 'xml', 'rename': 'OverallQualityScore', 'type': 'float'},
    }

    _xml_map = {
        'name': 'ImageScore'
    }

    def __init__(
            self,
            overall_quality_score: Optional[float] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            overall_quality_score (float, optional): The overall quality score of the image.
        """
        super().__init__(**kwargs)
        self.overall_quality_score = overall_quality_score


class CroppingSuggestion(serde.Model):
    """A cropping suggestion for an image."""

    _attribute_map = {
        'aspect_ratio': {'tag': 'xml', 'rename': 'AspectRatio', 'type': 'str'},
        'confidence': {'tag': 'xml', 'rename': 'Confidence', 'type': 'float'},
        'boundary': {'tag': 'xml', 'rename': 'Boundary', 'type': 'Boundary'},
    }

    _xml_map = {
        'name': 'CroppingSuggestion'
    }

    def __init__(
            self,
            aspect_ratio: Optional[str] = None,
            confidence: Optional[float] = None,
            boundary: Optional[Boundary] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            aspect_ratio (str, optional): The aspect ratio of the cropping.
            confidence (float, optional): The confidence of the suggestion.
            boundary (Boundary, optional): The suggested cropping boundary.
        """
        super().__init__(**kwargs)
        self.aspect_ratio = aspect_ratio
        self.confidence = confidence
        self.boundary = boundary


class OCRContents(serde.Model):
    """OCR recognition contents of an image."""

    _attribute_map = {
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'contents': {'tag': 'xml', 'rename': 'Contents', 'type': 'str'},
        'confidence': {'tag': 'xml', 'rename': 'Confidence', 'type': 'float'},
        'boundary': {'tag': 'xml', 'rename': 'Boundary', 'type': 'Boundary'},
    }

    _xml_map = {
        'name': 'OCRContents'
    }

    def __init__(
            self,
            language: Optional[str] = None,
            contents: Optional[str] = None,
            confidence: Optional[float] = None,
            boundary: Optional[Boundary] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            language (str, optional): The language of the recognized text.
            contents (str, optional): The recognized text contents.
            confidence (float, optional): The confidence of the recognition.
            boundary (Boundary, optional): The boundary of the recognized text.
        """
        super().__init__(**kwargs)
        self.language = language
        self.contents = contents
        self.confidence = confidence
        self.boundary = boundary


class Tagging(serde.Model):
    """A key-value tagging entry."""

    _attribute_map = {
        'key': {'tag': 'xml', 'rename': 'Key', 'type': 'str'},
        'value': {'tag': 'xml', 'rename': 'Value', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Tagging'
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


class OSSTagging(serde.Model):
    """OSS object tagging entries container."""

    _attribute_map = {
        'tagging': {'tag': 'xml', 'rename': 'Tagging', 'type': '[Tagging]'},
    }

    _xml_map = {
        'name': 'OSSTagging'
    }

    def __init__(
            self,
            tagging: Optional[List[Tagging]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            tagging (List[Tagging], optional): The list of tagging entries.
        """
        super().__init__(**kwargs)
        self.tagging = tagging


class UserMeta(serde.Model):
    """A key-value user metadata entry."""

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
            key (str, optional): The metadata key.
            value (str, optional): The metadata value.
        """
        super().__init__(**kwargs)
        self.key = key
        self.value = value


class OSSUserMeta(serde.Model):
    """OSS user-defined metadata entries container."""

    _attribute_map = {
        'user_meta': {'tag': 'xml', 'rename': 'UserMeta', 'type': '[UserMeta]'},
    }

    _xml_map = {
        'name': 'OSSUserMeta'
    }

    def __init__(
            self,
            user_meta: Optional[List[UserMeta]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            user_meta (List[UserMeta], optional): The list of user metadata entries.
        """
        super().__init__(**kwargs)
        self.user_meta = user_meta


class AudioStream(serde.Model):
    """An audio stream of a media file."""

    _attribute_map = {
        'index': {'tag': 'xml', 'rename': 'Index', 'type': 'int'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'codec_name': {'tag': 'xml', 'rename': 'CodecName', 'type': 'str'},
        'codec_long_name': {'tag': 'xml', 'rename': 'CodecLongName', 'type': 'str'},
        'codec_time_base': {'tag': 'xml', 'rename': 'CodecTimeBase', 'type': 'str'},
        'codec_tag_string': {'tag': 'xml', 'rename': 'CodecTagString', 'type': 'str'},
        'codec_tag': {'tag': 'xml', 'rename': 'CodecTag', 'type': 'str'},
        'time_base': {'tag': 'xml', 'rename': 'TimeBase', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'frame_count': {'tag': 'xml', 'rename': 'FrameCount', 'type': 'int'},
        'lyric': {'tag': 'xml', 'rename': 'Lyric', 'type': 'str'},
        'sample_format': {'tag': 'xml', 'rename': 'SampleFormat', 'type': 'str'},
        'sample_rate': {'tag': 'xml', 'rename': 'SampleRate', 'type': 'int'},
        'channels': {'tag': 'xml', 'rename': 'Channels', 'type': 'int'},
        'channel_layout': {'tag': 'xml', 'rename': 'ChannelLayout', 'type': 'str'},
    }

    _xml_map = {
        'name': 'AudioStream'
    }

    def __init__(
            self,
            index: Optional[int] = None,
            language: Optional[str] = None,
            codec_name: Optional[str] = None,
            codec_long_name: Optional[str] = None,
            codec_time_base: Optional[str] = None,
            codec_tag_string: Optional[str] = None,
            codec_tag: Optional[str] = None,
            time_base: Optional[str] = None,
            start_time: Optional[float] = None,
            duration: Optional[float] = None,
            bitrate: Optional[int] = None,
            frame_count: Optional[int] = None,
            lyric: Optional[str] = None,
            sample_format: Optional[str] = None,
            sample_rate: Optional[int] = None,
            channels: Optional[int] = None,
            channel_layout: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            index (int, optional): The index of the audio stream.
            language (str, optional): The language of the audio stream.
            codec_name (str, optional): The codec name.
            codec_long_name (str, optional): The codec long name.
            codec_time_base (str, optional): The codec time base.
            codec_tag_string (str, optional): The codec tag string.
            codec_tag (str, optional): The codec tag.
            time_base (str, optional): The time base.
            start_time (float, optional): The start time in seconds.
            duration (float, optional): The duration in seconds.
            bitrate (int, optional): The bitrate.
            frame_count (int, optional): The frame count.
            lyric (str, optional): The lyric.
            sample_format (str, optional): The sample format.
            sample_rate (int, optional): The sample rate.
            channels (int, optional): The channel count.
            channel_layout (str, optional): The channel layout.
        """
        super().__init__(**kwargs)
        self.index = index
        self.language = language
        self.codec_name = codec_name
        self.codec_long_name = codec_long_name
        self.codec_time_base = codec_time_base
        self.codec_tag_string = codec_tag_string
        self.codec_tag = codec_tag
        self.time_base = time_base
        self.start_time = start_time
        self.duration = duration
        self.bitrate = bitrate
        self.frame_count = frame_count
        self.lyric = lyric
        self.sample_format = sample_format
        self.sample_rate = sample_rate
        self.channels = channels
        self.channel_layout = channel_layout


class VideoStream(serde.Model):
    """A video stream of a media file."""

    _attribute_map = {
        'index': {'tag': 'xml', 'rename': 'Index', 'type': 'int'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'codec_name': {'tag': 'xml', 'rename': 'CodecName', 'type': 'str'},
        'codec_long_name': {'tag': 'xml', 'rename': 'CodecLongName', 'type': 'str'},
        'profile': {'tag': 'xml', 'rename': 'Profile', 'type': 'str'},
        'codec_time_base': {'tag': 'xml', 'rename': 'CodecTimeBase', 'type': 'str'},
        'codec_tag_string': {'tag': 'xml', 'rename': 'CodecTagString', 'type': 'str'},
        'codec_tag': {'tag': 'xml', 'rename': 'CodecTag', 'type': 'str'},
        'width': {'tag': 'xml', 'rename': 'Width', 'type': 'int'},
        'height': {'tag': 'xml', 'rename': 'Height', 'type': 'int'},
        'has_b_frames': {'tag': 'xml', 'rename': 'HasBFrames', 'type': 'int'},
        'sample_aspect_ratio': {'tag': 'xml', 'rename': 'SampleAspectRatio', 'type': 'str'},
        'display_aspect_ratio': {'tag': 'xml', 'rename': 'DisplayAspectRatio', 'type': 'str'},
        'pixel_format': {'tag': 'xml', 'rename': 'PixelFormat', 'type': 'str'},
        'level': {'tag': 'xml', 'rename': 'Level', 'type': 'int'},
        'frame_rate': {'tag': 'xml', 'rename': 'FrameRate', 'type': 'str'},
        'average_frame_rate': {'tag': 'xml', 'rename': 'AverageFrameRate', 'type': 'str'},
        'time_base': {'tag': 'xml', 'rename': 'TimeBase', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'frame_count': {'tag': 'xml', 'rename': 'FrameCount', 'type': 'int'},
        'rotate': {'tag': 'xml', 'rename': 'Rotate', 'type': 'str'},
        'bit_depth': {'tag': 'xml', 'rename': 'BitDepth', 'type': 'int'},
        'color_space': {'tag': 'xml', 'rename': 'ColorSpace', 'type': 'str'},
        'color_range': {'tag': 'xml', 'rename': 'ColorRange', 'type': 'str'},
        'color_transfer': {'tag': 'xml', 'rename': 'ColorTransfer', 'type': 'str'},
        'color_primaries': {'tag': 'xml', 'rename': 'ColorPrimaries', 'type': 'str'},
    }

    _xml_map = {
        'name': 'VideoStream'
    }

    def __init__(
            self,
            index: Optional[int] = None,
            language: Optional[str] = None,
            codec_name: Optional[str] = None,
            codec_long_name: Optional[str] = None,
            profile: Optional[str] = None,
            codec_time_base: Optional[str] = None,
            codec_tag_string: Optional[str] = None,
            codec_tag: Optional[str] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            has_b_frames: Optional[int] = None,
            sample_aspect_ratio: Optional[str] = None,
            display_aspect_ratio: Optional[str] = None,
            pixel_format: Optional[str] = None,
            level: Optional[int] = None,
            frame_rate: Optional[str] = None,
            average_frame_rate: Optional[str] = None,
            time_base: Optional[str] = None,
            start_time: Optional[float] = None,
            duration: Optional[float] = None,
            bitrate: Optional[int] = None,
            frame_count: Optional[int] = None,
            rotate: Optional[str] = None,
            bit_depth: Optional[int] = None,
            color_space: Optional[str] = None,
            color_range: Optional[str] = None,
            color_transfer: Optional[str] = None,
            color_primaries: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            index (int, optional): The index of the video stream.
            language (str, optional): The language of the video stream.
            codec_name (str, optional): The codec name.
            codec_long_name (str, optional): The codec long name.
            profile (str, optional): The codec profile.
            codec_time_base (str, optional): The codec time base.
            codec_tag_string (str, optional): The codec tag string.
            codec_tag (str, optional): The codec tag.
            width (int, optional): The width of the video.
            height (int, optional): The height of the video.
            has_b_frames (int, optional): Whether the stream has B frames.
            sample_aspect_ratio (str, optional): The sample aspect ratio.
            display_aspect_ratio (str, optional): The display aspect ratio.
            pixel_format (str, optional): The pixel format.
            level (int, optional): The codec level.
            frame_rate (str, optional): The frame rate.
            average_frame_rate (str, optional): The average frame rate.
            time_base (str, optional): The time base.
            start_time (float, optional): The start time in seconds.
            duration (float, optional): The duration in seconds.
            bitrate (int, optional): The bitrate.
            frame_count (int, optional): The frame count.
            rotate (str, optional): The rotation.
            bit_depth (int, optional): The bit depth.
            color_space (str, optional): The color space.
            color_range (str, optional): The color range.
            color_transfer (str, optional): The color transfer.
            color_primaries (str, optional): The color primaries.
        """
        super().__init__(**kwargs)
        self.index = index
        self.language = language
        self.codec_name = codec_name
        self.codec_long_name = codec_long_name
        self.profile = profile
        self.codec_time_base = codec_time_base
        self.codec_tag_string = codec_tag_string
        self.codec_tag = codec_tag
        self.width = width
        self.height = height
        self.has_b_frames = has_b_frames
        self.sample_aspect_ratio = sample_aspect_ratio
        self.display_aspect_ratio = display_aspect_ratio
        self.pixel_format = pixel_format
        self.level = level
        self.frame_rate = frame_rate
        self.average_frame_rate = average_frame_rate
        self.time_base = time_base
        self.start_time = start_time
        self.duration = duration
        self.bitrate = bitrate
        self.frame_count = frame_count
        self.rotate = rotate
        self.bit_depth = bit_depth
        self.color_space = color_space
        self.color_range = color_range
        self.color_transfer = color_transfer
        self.color_primaries = color_primaries


class SubtitleStream(serde.Model):
    """A subtitle stream of a media file."""

    _attribute_map = {
        'index': {'tag': 'xml', 'rename': 'Index', 'type': 'int'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'codec_name': {'tag': 'xml', 'rename': 'CodecName', 'type': 'str'},
        'codec_long_name': {'tag': 'xml', 'rename': 'CodecLongName', 'type': 'str'},
        'codec_tag_string': {'tag': 'xml', 'rename': 'CodecTagString', 'type': 'str'},
        'codec_tag': {'tag': 'xml', 'rename': 'CodecTag', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'content': {'tag': 'xml', 'rename': 'Content', 'type': 'str'},
        'width': {'tag': 'xml', 'rename': 'Width', 'type': 'int'},
        'height': {'tag': 'xml', 'rename': 'Height', 'type': 'int'},
    }

    _xml_map = {
        'name': 'SubtitleStream'
    }

    def __init__(
            self,
            index: Optional[int] = None,
            language: Optional[str] = None,
            codec_name: Optional[str] = None,
            codec_long_name: Optional[str] = None,
            codec_tag_string: Optional[str] = None,
            codec_tag: Optional[str] = None,
            start_time: Optional[float] = None,
            duration: Optional[float] = None,
            bitrate: Optional[int] = None,
            content: Optional[str] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            index (int, optional): The index of the subtitle stream.
            language (str, optional): The language of the subtitle stream.
            codec_name (str, optional): The codec name.
            codec_long_name (str, optional): The codec long name.
            codec_tag_string (str, optional): The codec tag string.
            codec_tag (str, optional): The codec tag.
            start_time (float, optional): The start time in seconds.
            duration (float, optional): The duration in seconds.
            bitrate (int, optional): The bitrate.
            content (str, optional): The subtitle content.
            width (int, optional): The width.
            height (int, optional): The height.
        """
        super().__init__(**kwargs)
        self.index = index
        self.language = language
        self.codec_name = codec_name
        self.codec_long_name = codec_long_name
        self.codec_tag_string = codec_tag_string
        self.codec_tag = codec_tag
        self.start_time = start_time
        self.duration = duration
        self.bitrate = bitrate
        self.content = content
        self.width = width
        self.height = height



class VideoInsight(serde.Model):
    """Video insight information."""

    _attribute_map = {
        'caption': {'tag': 'xml', 'rename': 'Caption', 'type': 'str'},
        'description': {'tag': 'xml', 'rename': 'Description', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Video'
    }

    def __init__(
            self,
            caption: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            caption (str, optional): The video caption.
            description (str, optional): The video description.
        """
        super().__init__(**kwargs)
        self.caption = caption
        self.description = description


class ImageInsight(serde.Model):
    """Image insight information."""

    _attribute_map = {
        'caption': {'tag': 'xml', 'rename': 'Caption', 'type': 'str'},
        'description': {'tag': 'xml', 'rename': 'Description', 'type': 'str'},
    }

    _xml_map = {
        'name': 'Image'
    }

    def __init__(
            self,
            caption: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            caption (str, optional): The image caption.
            description (str, optional): The image description.
        """
        super().__init__(**kwargs)
        self.caption = caption
        self.description = description


class Insights(serde.Model):
    """Insights information of a file."""

    _attribute_map = {
        'video': {'tag': 'xml', 'rename': 'Video', 'type': 'VideoInsight'},
        'image': {'tag': 'xml', 'rename': 'Image', 'type': 'ImageInsight'},
    }

    _xml_map = {
        'name': 'Insights'
    }

    def __init__(
            self,
            video: Optional[VideoInsight] = None,
            image: Optional[ImageInsight] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            video (VideoInsight, optional): The video insight.
            image (ImageInsight, optional): The image insight.
        """
        super().__init__(**kwargs)
        self.video = video
        self.image = image


class Image(serde.Model):
    """Image information, e.g. an audio cover."""

    _attribute_map = {
        'image_width': {'tag': 'xml', 'rename': 'ImageWidth', 'type': 'int'},
        'image_height': {'tag': 'xml', 'rename': 'ImageHeight', 'type': 'int'},
        'exif': {'tag': 'xml', 'rename': 'EXIF', 'type': 'str'},
        'image_score': {'tag': 'xml', 'rename': 'ImageScore', 'type': 'ImageScore'},
        'cropping_suggestions': {'tag': 'xml', 'rename': 'CroppingSuggestions', 'type': 'CroppingSuggestions'},
        'ocr_contents': {'tag': 'xml', 'rename': 'OCRContents', 'type': 'OCRContentsWrapper'},
    }

    _xml_map = {
        'name': 'Image'
    }

    def __init__(
            self,
            image_width: Optional[int] = None,
            image_height: Optional[int] = None,
            exif: Optional[str] = None,
            image_score: Optional[ImageScore] = None,
            cropping_suggestions: Optional['CroppingSuggestions'] = None,
            ocr_contents: Optional['OCRContentsWrapper'] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            image_width (int, optional): The width of the image.
            image_height (int, optional): The height of the image.
            exif (str, optional): The EXIF information.
            image_score (ImageScore, optional): The image quality score.
            cropping_suggestions (CroppingSuggestions, optional): The cropping suggestions.
            ocr_contents (OCRContentsWrapper, optional): The OCR contents.
        """
        super().__init__(**kwargs)
        self.image_width = image_width
        self.image_height = image_height
        self.exif = exif
        self.image_score = image_score
        self.cropping_suggestions = cropping_suggestions
        self.ocr_contents = ocr_contents


class ElementContent(serde.Model):
    """Content of an element."""

    _attribute_map = {
        'type': {'tag': 'xml', 'rename': 'Type', 'type': 'str'},
        'content': {'tag': 'xml', 'rename': 'Content', 'type': 'str'},
        'url': {'tag': 'xml', 'rename': 'Url', 'type': 'str'},
        'time_range': {'tag': 'xml', 'rename': 'TimeRange', 'type': '[int]'},
    }

    _xml_map = {
        'name': 'ElementContent'
    }

    def __init__(
            self,
            type: Optional[str] = None,
            content: Optional[str] = None,
            url: Optional[str] = None,
            time_range: Optional[List[int]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            type (str, optional): The content type.
            content (str, optional): The content.
            url (str, optional): The content URL.
            time_range (List[int], optional): The time range in milliseconds.
        """
        super().__init__(**kwargs)
        self.type = type
        self.content = content
        self.url = url
        self.time_range = time_range


class ElementRelation(serde.Model):
    """Relation between elements."""

    _attribute_map = {
        'type': {'tag': 'xml', 'rename': 'Type', 'type': 'str'},
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
    }

    _xml_map = {
        'name': 'ElementRelation'
    }

    def __init__(
            self,
            type: Optional[str] = None,
            object_id: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            type (str, optional): The relation type.
            object_id (str, optional): The related object ID.
        """
        super().__init__(**kwargs)
        self.type = type
        self.object_id = object_id


class Element(serde.Model):
    """An element of a file."""

    _attribute_map = {
        'element_contents': {'tag': 'xml', 'rename': 'ElementContents', 'type': 'ElementContents'},
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
        'element_type': {'tag': 'xml', 'rename': 'ElementType', 'type': 'str'},
        'semantic_similarity': {'tag': 'xml', 'rename': 'SemanticSimilarity', 'type': 'float'},
        'element_relations': {'tag': 'xml', 'rename': 'ElementRelations', 'type': 'ElementRelations'},
    }

    _xml_map = {
        'name': 'Element'
    }

    def __init__(
            self,
            element_contents: Optional['ElementContents'] = None,
            object_id: Optional[str] = None,
            element_type: Optional[str] = None,
            semantic_similarity: Optional[float] = None,
            element_relations: Optional['ElementRelations'] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            element_contents (ElementContents, optional): The element contents.
            object_id (str, optional): The object ID.
            element_type (str, optional): The element type.
            semantic_similarity (float, optional): The semantic similarity.
            element_relations (ElementRelations, optional): The element relations.
        """
        super().__init__(**kwargs)
        self.element_contents = element_contents
        self.object_id = object_id
        self.element_type = element_type
        self.semantic_similarity = semantic_similarity
        self.element_relations = element_relations


class SceneElement(serde.Model):
    """A scene element of a video file."""

    _attribute_map = {
        'time_range': {'tag': 'xml', 'rename': 'TimeRange', 'type': '[int]'},
        'frame_times': {'tag': 'xml', 'rename': 'FrameTimes', 'type': '[int]'},
        'video_stream_index': {'tag': 'xml', 'rename': 'VideoStreamIndex', 'type': 'int'},
        'labels': {'tag': 'xml', 'rename': 'Labels', 'type': 'Labels'},
    }

    _xml_map = {
        'name': 'SceneElement'
    }

    def __init__(
            self,
            time_range: Optional[List[int]] = None,
            frame_times: Optional[List[int]] = None,
            video_stream_index: Optional[int] = None,
            labels: Optional['Labels'] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            time_range (List[int], optional): The time range in milliseconds.
            frame_times (List[int], optional): The frame times in milliseconds.
            video_stream_index (int, optional): The video stream index.
            labels (Labels, optional): The labels of the scene element.
        """
        super().__init__(**kwargs)
        self.time_range = time_range
        self.frame_times = frame_times
        self.video_stream_index = video_stream_index
        self.labels = labels


class File(serde.Model):
    """A file entry returned by MetaQuery/Query operations."""

    _attribute_map = {
        'owner_id': {'tag': 'xml', 'rename': 'OwnerId', 'type': 'str'},
        'dataset_name': {'tag': 'xml', 'rename': 'DatasetName', 'type': 'str'},
        'object_type': {'tag': 'xml', 'rename': 'ObjectType', 'type': 'str'},
        'object_id': {'tag': 'xml', 'rename': 'ObjectId', 'type': 'str'},
        'update_time': {'tag': 'xml', 'rename': 'UpdateTime', 'type': 'str'},
        'create_time': {'tag': 'xml', 'rename': 'CreateTime', 'type': 'str'},
        'uri': {'tag': 'xml', 'rename': 'URI', 'type': 'str'},
        'oss_uri': {'tag': 'xml', 'rename': 'OSSURI', 'type': 'str'},
        'filename': {'tag': 'xml', 'rename': 'Filename', 'type': 'str'},
        'media_type': {'tag': 'xml', 'rename': 'MediaType', 'type': 'str'},
        'content_type': {'tag': 'xml', 'rename': 'ContentType', 'type': 'str'},
        'size': {'tag': 'xml', 'rename': 'Size', 'type': 'int'},
        'file_hash': {'tag': 'xml', 'rename': 'FileHash', 'type': 'str'},
        'file_modified_time': {'tag': 'xml', 'rename': 'FileModifiedTime', 'type': 'str'},
        'file_create_time': {'tag': 'xml', 'rename': 'FileCreateTime', 'type': 'str'},
        'file_access_time': {'tag': 'xml', 'rename': 'FileAccessTime', 'type': 'str'},
        'produce_time': {'tag': 'xml', 'rename': 'ProduceTime', 'type': 'str'},
        'lat_long': {'tag': 'xml', 'rename': 'LatLong', 'type': 'str'},
        'timezone': {'tag': 'xml', 'rename': 'Timezone', 'type': 'str'},
        'addresses': {'tag': 'xml', 'rename': 'Addresses', 'type': 'Addresses'},
        'travel_cluster_id': {'tag': 'xml', 'rename': 'TravelClusterId', 'type': 'str'},
        'orientation': {'tag': 'xml', 'rename': 'Orientation', 'type': 'int'},
        'figures': {'tag': 'xml', 'rename': 'Figures', 'type': 'Figures'},
        'figure_count': {'tag': 'xml', 'rename': 'FigureCount', 'type': 'int'},
        'labels': {'tag': 'xml', 'rename': 'Labels', 'type': 'Labels'},
        'title': {'tag': 'xml', 'rename': 'Title', 'type': 'str'},
        'image_width': {'tag': 'xml', 'rename': 'ImageWidth', 'type': 'int'},
        'image_height': {'tag': 'xml', 'rename': 'ImageHeight', 'type': 'int'},
        'exif': {'tag': 'xml', 'rename': 'EXIF', 'type': 'str'},
        'image_score': {'tag': 'xml', 'rename': 'ImageScore', 'type': 'ImageScore'},
        'cropping_suggestions': {'tag': 'xml', 'rename': 'CroppingSuggestions', 'type': 'CroppingSuggestions'},
        'ocr_contents': {'tag': 'xml', 'rename': 'OCRContents', 'type': 'OCRContentsWrapper'},
        'video_width': {'tag': 'xml', 'rename': 'VideoWidth', 'type': 'int'},
        'video_height': {'tag': 'xml', 'rename': 'VideoHeight', 'type': 'int'},
        'video_streams': {'tag': 'xml', 'rename': 'VideoStreams', 'type': 'VideoStreams'},
        'subtitles': {'tag': 'xml', 'rename': 'Subtitles', 'type': 'Subtitles'},
        'audio_streams': {'tag': 'xml', 'rename': 'AudioStreams', 'type': 'AudioStreams'},
        'artist': {'tag': 'xml', 'rename': 'Artist', 'type': 'str'},
        'album_artist': {'tag': 'xml', 'rename': 'AlbumArtist', 'type': 'str'},
        'audio_covers': {'tag': 'xml', 'rename': 'AudioCovers', 'type': 'AudioCovers'},
        'composer': {'tag': 'xml', 'rename': 'Composer', 'type': 'str'},
        'performer': {'tag': 'xml', 'rename': 'Performer', 'type': 'str'},
        'language': {'tag': 'xml', 'rename': 'Language', 'type': 'str'},
        'album': {'tag': 'xml', 'rename': 'Album', 'type': 'str'},
        'page_count': {'tag': 'xml', 'rename': 'PageCount', 'type': 'int'},
        'e_tag': {'tag': 'xml', 'rename': 'ETag', 'type': 'str'},
        'cache_control': {'tag': 'xml', 'rename': 'CacheControl', 'type': 'str'},
        'content_disposition': {'tag': 'xml', 'rename': 'ContentDisposition', 'type': 'str'},
        'content_encoding': {'tag': 'xml', 'rename': 'ContentEncoding', 'type': 'str'},
        'content_language': {'tag': 'xml', 'rename': 'ContentLanguage', 'type': 'str'},
        'access_control_allow_origin': {'tag': 'xml', 'rename': 'AccessControlAllowOrigin', 'type': 'str'},
        'access_control_request_method': {'tag': 'xml', 'rename': 'AccessControlRequestMethod', 'type': 'str'},
        'server_side_encryption_customer_algorithm': {'tag': 'xml', 'rename': 'ServerSideEncryptionCustomerAlgorithm', 'type': 'str'},
        'server_side_encryption': {'tag': 'xml', 'rename': 'ServerSideEncryption', 'type': 'str'},
        'server_side_data_encryption': {'tag': 'xml', 'rename': 'ServerSideDataEncryption', 'type': 'str'},
        'server_side_encryption_key_id': {'tag': 'xml', 'rename': 'ServerSideEncryptionKeyId', 'type': 'str'},
        'oss_storage_class': {'tag': 'xml', 'rename': 'OSSStorageClass', 'type': 'str'},
        'oss_crc64': {'tag': 'xml', 'rename': 'OSSCRC64', 'type': 'str'},
        'object_acl': {'tag': 'xml', 'rename': 'ObjectACL', 'type': 'str'},
        'content_md5': {'tag': 'xml', 'rename': 'ContentMd5', 'type': 'str'},
        'oss_user_meta': {'tag': 'xml', 'rename': 'OSSUserMeta', 'type': 'OSSUserMeta'},
        'oss_tagging_count': {'tag': 'xml', 'rename': 'OSSTaggingCount', 'type': 'int'},
        'oss_tagging': {'tag': 'xml', 'rename': 'OSSTagging', 'type': 'OSSTagging'},
        'oss_expiration': {'tag': 'xml', 'rename': 'OSSExpiration', 'type': 'str'},
        'oss_version_id': {'tag': 'xml', 'rename': 'OSSVersionId', 'type': 'str'},
        'oss_delete_marker': {'tag': 'xml', 'rename': 'OSSDeleteMarker', 'type': 'str'},
        'oss_object_type': {'tag': 'xml', 'rename': 'OSSObjectType', 'type': 'str'},
        'custom_id': {'tag': 'xml', 'rename': 'CustomId', 'type': 'str'},
        'stream_count': {'tag': 'xml', 'rename': 'StreamCount', 'type': 'int'},
        'program_count': {'tag': 'xml', 'rename': 'ProgramCount', 'type': 'int'},
        'format_name': {'tag': 'xml', 'rename': 'FormatName', 'type': 'str'},
        'format_long_name': {'tag': 'xml', 'rename': 'FormatLongName', 'type': 'str'},
        'start_time': {'tag': 'xml', 'rename': 'StartTime', 'type': 'float'},
        'bitrate': {'tag': 'xml', 'rename': 'Bitrate', 'type': 'int'},
        'duration': {'tag': 'xml', 'rename': 'Duration', 'type': 'float'},
        'semantic_types': {'tag': 'xml', 'rename': 'SemanticTypes', 'type': 'SemanticTypes'},
        'elements': {'tag': 'xml', 'rename': 'Elements', 'type': 'Elements'},
        'scene_elements': {'tag': 'xml', 'rename': 'SceneElements', 'type': 'SceneElements'},
        'ocr_texts': {'tag': 'xml', 'rename': 'OCRTexts', 'type': 'str'},
        'reason': {'tag': 'xml', 'rename': 'Reason', 'type': 'str'},
        'object_status': {'tag': 'xml', 'rename': 'ObjectStatus', 'type': 'str'},
        'insights': {'tag': 'xml', 'rename': 'Insights', 'type': 'Insights'},
    }

    _xml_map = {
        'name': 'File'
    }

    def __init__(
            self,
            owner_id: Optional[str] = None,
            dataset_name: Optional[str] = None,
            object_type: Optional[str] = None,
            object_id: Optional[str] = None,
            update_time: Optional[str] = None,
            create_time: Optional[str] = None,
            uri: Optional[str] = None,
            oss_uri: Optional[str] = None,
            filename: Optional[str] = None,
            media_type: Optional[str] = None,
            content_type: Optional[str] = None,
            size: Optional[int] = None,
            file_hash: Optional[str] = None,
            file_modified_time: Optional[str] = None,
            file_create_time: Optional[str] = None,
            file_access_time: Optional[str] = None,
            produce_time: Optional[str] = None,
            lat_long: Optional[str] = None,
            timezone: Optional[str] = None,
            addresses: Optional['Addresses'] = None,
            travel_cluster_id: Optional[str] = None,
            orientation: Optional[int] = None,
            figures: Optional['Figures'] = None,
            figure_count: Optional[int] = None,
            labels: Optional['Labels'] = None,
            title: Optional[str] = None,
            image_width: Optional[int] = None,
            image_height: Optional[int] = None,
            exif: Optional[str] = None,
            image_score: Optional[ImageScore] = None,
            cropping_suggestions: Optional['CroppingSuggestions'] = None,
            ocr_contents: Optional['OCRContentsWrapper'] = None,
            video_width: Optional[int] = None,
            video_height: Optional[int] = None,
            video_streams: Optional['VideoStreams'] = None,
            subtitles: Optional['Subtitles'] = None,
            audio_streams: Optional['AudioStreams'] = None,
            artist: Optional[str] = None,
            album_artist: Optional[str] = None,
            audio_covers: Optional['AudioCovers'] = None,
            composer: Optional[str] = None,
            performer: Optional[str] = None,
            language: Optional[str] = None,
            album: Optional[str] = None,
            page_count: Optional[int] = None,
            e_tag: Optional[str] = None,
            cache_control: Optional[str] = None,
            content_disposition: Optional[str] = None,
            content_encoding: Optional[str] = None,
            content_language: Optional[str] = None,
            access_control_allow_origin: Optional[str] = None,
            access_control_request_method: Optional[str] = None,
            server_side_encryption_customer_algorithm: Optional[str] = None,
            server_side_encryption: Optional[str] = None,
            server_side_data_encryption: Optional[str] = None,
            server_side_encryption_key_id: Optional[str] = None,
            oss_storage_class: Optional[str] = None,
            oss_crc64: Optional[str] = None,
            object_acl: Optional[str] = None,
            content_md5: Optional[str] = None,
            oss_user_meta: Optional[OSSUserMeta] = None,
            oss_tagging_count: Optional[int] = None,
            oss_tagging: Optional[OSSTagging] = None,
            oss_expiration: Optional[str] = None,
            oss_version_id: Optional[str] = None,
            oss_delete_marker: Optional[str] = None,
            oss_object_type: Optional[str] = None,
            custom_id: Optional[str] = None,
            stream_count: Optional[int] = None,
            program_count: Optional[int] = None,
            format_name: Optional[str] = None,
            format_long_name: Optional[str] = None,
            start_time: Optional[float] = None,
            bitrate: Optional[int] = None,
            duration: Optional[float] = None,
            semantic_types: Optional['SemanticTypes'] = None,
            elements: Optional['Elements'] = None,
            scene_elements: Optional['SceneElements'] = None,
            ocr_texts: Optional[str] = None,
            reason: Optional[str] = None,
            object_status: Optional[str] = None,
            insights: Optional[Insights] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            owner_id (str, optional): The owner ID.
            dataset_name (str, optional): The dataset name.
            object_type (str, optional): The object type.
            object_id (str, optional): The object ID.
            update_time (str, optional): The update time.
            create_time (str, optional): The create time.
            uri (str, optional): The URI of the file.
            oss_uri (str, optional): The OSS URI of the file.
            filename (str, optional): The filename.
            media_type (str, optional): The media type.
            content_type (str, optional): The content type.
            size (int, optional): The file size in bytes.
            file_hash (str, optional): The file hash.
            file_modified_time (str, optional): The file modified time.
            file_create_time (str, optional): The file create time.
            file_access_time (str, optional): The file access time.
            produce_time (str, optional): The produce time.
            lat_long (str, optional): The latitude and longitude.
            timezone (str, optional): The timezone.
            addresses (Addresses, optional): The addresses.
            travel_cluster_id (str, optional): The travel cluster ID.
            orientation (int, optional): The image orientation.
            figures (Figures, optional): The figures.
            figure_count (int, optional): The figure count.
            labels (Labels, optional): The labels.
            title (str, optional): The title.
            image_width (int, optional): The image width.
            image_height (int, optional): The image height.
            exif (str, optional): The EXIF information.
            image_score (ImageScore, optional): The image quality score.
            cropping_suggestions (CroppingSuggestions, optional): The cropping suggestions.
            ocr_contents (OCRContentsWrapper, optional): The OCR contents.
            video_width (int, optional): The video width.
            video_height (int, optional): The video height.
            video_streams (VideoStreams, optional): The video streams.
            subtitles (Subtitles, optional): The subtitle streams.
            audio_streams (AudioStreams, optional): The audio streams.
            artist (str, optional): The artist.
            album_artist (str, optional): The album artist.
            audio_covers (AudioCovers, optional): The audio covers.
            composer (str, optional): The composer.
            performer (str, optional): The performer.
            language (str, optional): The language.
            album (str, optional): The album.
            page_count (int, optional): The page count.
            e_tag (str, optional): The ETag.
            cache_control (str, optional): The Cache-Control.
            content_disposition (str, optional): The Content-Disposition.
            content_encoding (str, optional): The Content-Encoding.
            content_language (str, optional): The Content-Language.
            access_control_allow_origin (str, optional): The Access-Control-Allow-Origin.
            access_control_request_method (str, optional): The Access-Control-Request-Method.
            server_side_encryption_customer_algorithm (str, optional): The SSE customer algorithm.
            server_side_encryption (str, optional): The server side encryption.
            server_side_data_encryption (str, optional): The server side data encryption.
            server_side_encryption_key_id (str, optional): The SSE key ID.
            oss_storage_class (str, optional): The OSS storage class.
            oss_crc64 (str, optional): The OSS CRC64.
            object_acl (str, optional): The object ACL.
            content_md5 (str, optional): The Content-MD5.
            oss_user_meta (OSSUserMeta, optional): The OSS user metadata.
            oss_tagging_count (int, optional): The OSS tagging count.
            oss_tagging (OSSTagging, optional): The OSS tagging.
            oss_expiration (str, optional): The OSS expiration.
            oss_version_id (str, optional): The OSS version ID.
            oss_delete_marker (str, optional): The OSS delete marker.
            oss_object_type (str, optional): The OSS object type.
            custom_id (str, optional): The custom ID.
            stream_count (int, optional): The stream count.
            program_count (int, optional): The program count.
            format_name (str, optional): The format name.
            format_long_name (str, optional): The format long name.
            start_time (float, optional): The start time in seconds.
            bitrate (int, optional): The bitrate.
            duration (float, optional): The duration in seconds.
            semantic_types (SemanticTypes, optional): The semantic types.
            elements (Elements, optional): The elements.
            scene_elements (SceneElements, optional): The scene elements.
            ocr_texts (str, optional): The OCR texts.
            reason (str, optional): The reason.
            object_status (str, optional): The object status.
            insights (Insights, optional): The insights information.
        """
        super().__init__(**kwargs)
        self.owner_id = owner_id
        self.dataset_name = dataset_name
        self.object_type = object_type
        self.object_id = object_id
        self.update_time = update_time
        self.create_time = create_time
        self.uri = uri
        self.oss_uri = oss_uri
        self.filename = filename
        self.media_type = media_type
        self.content_type = content_type
        self.size = size
        self.file_hash = file_hash
        self.file_modified_time = file_modified_time
        self.file_create_time = file_create_time
        self.file_access_time = file_access_time
        self.produce_time = produce_time
        self.lat_long = lat_long
        self.timezone = timezone
        self.addresses = addresses
        self.travel_cluster_id = travel_cluster_id
        self.orientation = orientation
        self.figures = figures
        self.figure_count = figure_count
        self.labels = labels
        self.title = title
        self.image_width = image_width
        self.image_height = image_height
        self.exif = exif
        self.image_score = image_score
        self.cropping_suggestions = cropping_suggestions
        self.ocr_contents = ocr_contents
        self.video_width = video_width
        self.video_height = video_height
        self.video_streams = video_streams
        self.subtitles = subtitles
        self.audio_streams = audio_streams
        self.artist = artist
        self.album_artist = album_artist
        self.audio_covers = audio_covers
        self.composer = composer
        self.performer = performer
        self.language = language
        self.album = album
        self.page_count = page_count
        self.e_tag = e_tag
        self.cache_control = cache_control
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_language = content_language
        self.access_control_allow_origin = access_control_allow_origin
        self.access_control_request_method = access_control_request_method
        self.server_side_encryption_customer_algorithm = server_side_encryption_customer_algorithm
        self.server_side_encryption = server_side_encryption
        self.server_side_data_encryption = server_side_data_encryption
        self.server_side_encryption_key_id = server_side_encryption_key_id
        self.oss_storage_class = oss_storage_class
        self.oss_crc64 = oss_crc64
        self.object_acl = object_acl
        self.content_md5 = content_md5
        self.oss_user_meta = oss_user_meta
        self.oss_tagging_count = oss_tagging_count
        self.oss_tagging = oss_tagging
        self.oss_expiration = oss_expiration
        self.oss_version_id = oss_version_id
        self.oss_delete_marker = oss_delete_marker
        self.oss_object_type = oss_object_type
        self.custom_id = custom_id
        self.stream_count = stream_count
        self.program_count = program_count
        self.format_name = format_name
        self.format_long_name = format_long_name
        self.start_time = start_time
        self.bitrate = bitrate
        self.duration = duration
        self.semantic_types = semantic_types
        self.elements = elements
        self.scene_elements = scene_elements
        self.ocr_texts = ocr_texts
        self.reason = reason
        self.object_status = object_status
        self.insights = insights


class Files(serde.Model):
    """The list of files."""

    _attribute_map = {
        'file': {'tag': 'xml', 'rename': 'File', 'type': '[File]'},
    }

    _xml_map = {
        'name': 'Files'
    }

    def __init__(
            self,
            file: Optional[List[File]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            file (List[File], optional): The list of files.
        """
        super().__init__(**kwargs)
        self.file = file


class Labels(serde.Model):
    """The list of labels."""

    _attribute_map = {
        'label': {'tag': 'xml', 'rename': 'Label', 'type': '[Label]'},
    }

    _xml_map = {
        'name': 'Labels'
    }

    def __init__(
            self,
            label: Optional[List[Label]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            label (List[Label], optional): The list of labels.
        """
        super().__init__(**kwargs)
        self.label = label


class Clips(serde.Model):
    """The list of clips."""

    _attribute_map = {
        'clip': {'tag': 'xml', 'rename': 'Clip', 'type': '[Clip]'},
    }

    _xml_map = {
        'name': 'Clips'
    }

    def __init__(
            self,
            clip: Optional[List[Clip]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            clip (List[Clip], optional): The list of clips.
        """
        super().__init__(**kwargs)
        self.clip = clip


class Addresses(serde.Model):
    """The list of addresses."""

    _attribute_map = {
        'address': {'tag': 'xml', 'rename': 'Address', 'type': '[Address]'},
    }

    _xml_map = {
        'name': 'Addresses'
    }

    def __init__(
            self,
            address: Optional[List[Address]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            address (List[Address], optional): The list of addresses.
        """
        super().__init__(**kwargs)
        self.address = address


class Figures(serde.Model):
    """The list of figures."""

    _attribute_map = {
        'figure': {'tag': 'xml', 'rename': 'Figure', 'type': '[Figure]'},
    }

    _xml_map = {
        'name': 'Figures'
    }

    def __init__(
            self,
            figure: Optional[List[Figure]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            figure (List[Figure], optional): The list of figures.
        """
        super().__init__(**kwargs)
        self.figure = figure


class AudioStreams(serde.Model):
    """The list of audio streams."""

    _attribute_map = {
        'audio_stream': {'tag': 'xml', 'rename': 'AudioStream', 'type': '[AudioStream]'},
    }

    _xml_map = {
        'name': 'AudioStreams'
    }

    def __init__(
            self,
            audio_stream: Optional[List[AudioStream]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            audio_stream (List[AudioStream], optional): The list of audio streams.
        """
        super().__init__(**kwargs)
        self.audio_stream = audio_stream


class VideoStreams(serde.Model):
    """The list of video streams."""

    _attribute_map = {
        'video_stream': {'tag': 'xml', 'rename': 'VideoStream', 'type': '[VideoStream]'},
    }

    _xml_map = {
        'name': 'VideoStreams'
    }

    def __init__(
            self,
            video_stream: Optional[List[VideoStream]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            video_stream (List[VideoStream], optional): The list of video streams.
        """
        super().__init__(**kwargs)
        self.video_stream = video_stream


class Subtitles(serde.Model):
    """The list of subtitle streams."""

    _attribute_map = {
        'subtitle': {'tag': 'xml', 'rename': 'Subtitle', 'type': '[SubtitleStream]'},
    }

    _xml_map = {
        'name': 'Subtitles'
    }

    def __init__(
            self,
            subtitle: Optional[List[SubtitleStream]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            subtitle (List[SubtitleStream], optional): The list of subtitle streams.
        """
        super().__init__(**kwargs)
        self.subtitle = subtitle


class AudioCovers(serde.Model):
    """The list of audio covers."""

    _attribute_map = {
        'audio_cover': {'tag': 'xml', 'rename': 'AudioCover', 'type': '[Image]'},
    }

    _xml_map = {
        'name': 'AudioCovers'
    }

    def __init__(
            self,
            audio_cover: Optional[List[Image]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            audio_cover (List[Image], optional): The list of audio covers.
        """
        super().__init__(**kwargs)
        self.audio_cover = audio_cover


class CroppingSuggestions(serde.Model):
    """The list of cropping suggestions."""

    _attribute_map = {
        'cropping_suggestion': {'tag': 'xml', 'rename': 'CroppingSuggestion', 'type': '[CroppingSuggestion]'},
    }

    _xml_map = {
        'name': 'CroppingSuggestions'
    }

    def __init__(
            self,
            cropping_suggestion: Optional[List[CroppingSuggestion]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            cropping_suggestion (List[CroppingSuggestion], optional): The list of cropping suggestions.
        """
        super().__init__(**kwargs)
        self.cropping_suggestion = cropping_suggestion


class OCRContentsWrapper(serde.Model):
    """The list of OCR contents."""

    _attribute_map = {
        'ocr_contents': {'tag': 'xml', 'rename': 'OCRContents', 'type': '[OCRContents]'},
    }

    _xml_map = {
        'name': 'OCRContents'
    }

    def __init__(
            self,
            ocr_contents: Optional[List[OCRContents]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            ocr_contents (List[OCRContents], optional): The list of OCR contents.
        """
        super().__init__(**kwargs)
        self.ocr_contents = ocr_contents


class Elements(serde.Model):
    """The list of elements."""

    _attribute_map = {
        'element': {'tag': 'xml', 'rename': 'Element', 'type': '[Element]'},
    }

    _xml_map = {
        'name': 'Elements'
    }

    def __init__(
            self,
            element: Optional[List[Element]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            element (List[Element], optional): The list of elements.
        """
        super().__init__(**kwargs)
        self.element = element


class SemanticTypes(serde.Model):
    """The list of semantic types."""

    _attribute_map = {
        'semantic_type': {'tag': 'xml', 'rename': 'SemanticType', 'type': '[str]'},
    }

    _xml_map = {
        'name': 'SemanticTypes'
    }

    def __init__(
            self,
            semantic_type: Optional[List[str]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            semantic_type (List[str], optional): The list of semantic types.
        """
        super().__init__(**kwargs)
        self.semantic_type = semantic_type


class SceneElements(serde.Model):
    """The list of scene elements."""

    _attribute_map = {
        'scene_element': {'tag': 'xml', 'rename': 'SceneElement', 'type': '[SceneElement]'},
    }

    _xml_map = {
        'name': 'SceneElements'
    }

    def __init__(
            self,
            scene_element: Optional[List[SceneElement]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            scene_element (List[SceneElement], optional): The list of scene elements.
        """
        super().__init__(**kwargs)
        self.scene_element = scene_element


class ElementContents(serde.Model):
    """The list of element contents."""

    _attribute_map = {
        'element_content': {'tag': 'xml', 'rename': 'ElementContent', 'type': '[ElementContent]'},
    }

    _xml_map = {
        'name': 'ElementContents'
    }

    def __init__(
            self,
            element_content: Optional[List[ElementContent]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            element_content (List[ElementContent], optional): The list of element contents.
        """
        super().__init__(**kwargs)
        self.element_content = element_content


class ElementRelations(serde.Model):
    """The list of element relations."""

    _attribute_map = {
        'element_relation': {'tag': 'xml', 'rename': 'ElementRelation', 'type': '[ElementRelation]'},
    }

    _xml_map = {
        'name': 'ElementRelations'
    }

    def __init__(
            self,
            element_relation: Optional[List[ElementRelation]] = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            element_relation (List[ElementRelation], optional): The list of element relations.
        """
        super().__init__(**kwargs)
        self.element_relation = element_relation

# -*- coding: utf-8 -*-
"""Helpers for building the JSON values of DataProcess query parameters.

The JSON shape is declared field by field in each model's ``_to_json_obj``.
It is deliberately independent of ``_attribute_map``, which describes the XML
wire format and carries wrapper elements that must not appear in JSON.
"""
from typing import Any, Dict, List, Optional


def compact(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Drop the keys whose value is None."""
    return {k: v for k, v in obj.items() if v is not None}


def to_obj(value: Any) -> Optional[Dict[str, Any]]:
    """Convert a nested model to its JSON object, keeping None as None."""
    return None if value is None else value._to_json_obj()


def to_list(values: Any) -> Optional[List[Any]]:
    """Convert a list of models to a list of JSON objects, keeping None as None."""
    return None if values is None else [v._to_json_obj() for v in values]

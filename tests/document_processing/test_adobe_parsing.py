import pytest
import pandas as pd
from typing import Dict, Any
from piqa.document_processing import flatten_and_preprocess_adobe_json

def test_flatten_and_preprocess_adobe_json_valid_data():
    json_data: Dict[Any, Any] = {
        'elements': [
            {
                "Bounds": [168.30999755859375, 338.8500061035156, 560.6693267822266, 378.80999755859375],
                "Font": {
                    "alt_family_name": "Calibri",
                    "embedded": True,
                    "encoding": "WinAnsiEncoding",
                    "family_name": "Calibri",
                    "font_type": "TrueType",
                    "italic": False,
                    "monospaced": False,
                    "name": "ABCDEE+Calibri,Bold",
                    "subset": True,
                    "weight": 700
                },
                "HasClip": False,
                "Lang": "en",
                "Page": 0,
                "Path": "//Document/P",
                "Text": "Foooobarrrrrrr",
                "TextSize": 39.96000671386719,
                "attributes": {
                    "LineHeight": 48,
                    "SpaceAfter": 6,
                    "TextAlign": "Center"
                },
                "PercentileBounds": {
                    "left": 0.23376388549804689,
                    "top": 0.2985000045211227,
                    "right": 0.778707398308648,
                    "bottom": 0.3724999886971933
                }
            },
            {
                "Bounds": [108.30999755859375, 238.8500061035156, 560.6693267822266, 360.80999755859375],
                "Font": {
                    "alt_family_name": "Arial",
                    "embedded": True,
                    "encoding": "WinAnsiEncoding",
                    "family_name": "Arial",
                    "font_type": "TrueType",
                    "italic": True,
                    "monospaced": False,
                    "name": "ABCDEE+Arial",
                    "subset": True,
                    "weight": 400
                },
                "HasClip": False,
                "Lang": "fr",
                "Page": 1,
                "Path": "//Document/P",
                "Text": "This is text, fantastic text, and it's in English!",
                "TextSize": 30,
                "attributes": {
                    "LineHeight": 36,
                    "SpaceAfter": 8,
                    "TextAlign": "Right"
                },
                "PercentileBounds": {
                    "left": 0.1,
                    "top": 0.2,
                    "right": 0.8,
                    "bottom": 0.3
                }
            }
        ]
    }
    result: pd.DataFrame = flatten_and_preprocess_adobe_json(json_data)
    assert result.shape == (2, 24)
    assert 'Text' in result.columns.to_list()
    assert 'Foooobarrrrrrr' in result['Text'].to_list()
    assert "This is text, fantastic text, and it's in English!" in result['Text'].to_list()



def test_flatten_and_preprocess_adobe_json_empty_text():
    json_data: Dict[Any, Any] = {
        'elements': [
            {
                # similar to above, but with 'Text' set to None
                "Text": None
                # remaining fields omitted for brevity
            },
        ]
    }
    result: pd.DataFrame = flatten_and_preprocess_adobe_json(json_data)
    assert result.empty


def test_flatten_and_preprocess_adobe_json_short_text():
    json_data: Dict[Any, Any] = {
        'elements': [
            {
                # similar to above, but with 'Text' shorter than 3 characters
                "Text": "ab"
                # remaining fields omitted for brevity
            },
        ]
    }
    result: pd.DataFrame = flatten_and_preprocess_adobe_json(json_data)
    assert result.empty


def test_flatten_and_preprocess_adobe_json_missing_text_key():
    json_data: Dict[Any, Any] = {
        'elements': [
            {
                "Bounds": [168.30999755859375, 338.8500061035156, 560.6693267822266, 378.80999755859375],
                "Font": {
                    "alt_family_name": "Arial",
                    "embedded": True,
                    "encoding": "WinAnsiEncoding",
                    "family_name": "Arial",
                    "font_type": "TrueType",
                    "italic": True,
                    "monospaced": False,
                    "name": "ABCDEE+Arial",
                    "subset": True,
                    "weight": 400
                },
                "HasClip": False,
                "Lang": "fr",
                "Page": 1,
                "Path": "//Document/P",
                # 'Text' key is missing entirely
                "TextSize": 30,
                "attributes": {
                    "LineHeight": 36,
                    "SpaceAfter": 8,
                    "TextAlign": "Right"
                },
                "PercentileBounds": {
                    "left": 0.1,
                    "top": 0.2,
                    "right": 0.8,
                    "bottom": 0.3
                }
            },
        ]
    }
    with pytest.raises(KeyError):
        flatten_and_preprocess_adobe_json(json_data)

import json
import os
import shutil
import pytest
from unittest import mock
from typing import Dict, Any

from piqa.document_processing import (process_pdf, _update_bounds, _preprocess_pdf, _call_adobe_service, _extract_data_from_result, _postprocess_elements) # type: ignore

def test_update_bounds():
    element = {
        "Bounds": [100, 200, 300, 400],
        "Page": 1,
    }
    page_sizes = [
        {"page_index": 0, "width": 500, "height": 1000},
    ]
    _update_bounds(element, page_sizes, 72)
    assert element["PercentileBounds"] == {"left": 0.2, "top": 0.6, "right": 0.6, "bottom": 0.8}

def test_preprocess_pdf():
    # provide input_file_path and output_file_path for testing
    # assuming the PDF has 10 pages, the first 5 pages should be processed
    page_sizes = _preprocess_pdf("tests/data/documents/moz.pdf", "tests/data/documents/moz.pdf", 5, False)
    assert len(page_sizes) == 5

def test_call_adobe_service():
    file_path = "tests/data/documents/moz.pdf"
    result = _call_adobe_service(file_path)
    assert result != None

def test_extract_data_from_result():
    # assuming a correct result and op_zip_file_path
    with open("tests/data/adobe_outputs/moz-output_transformed.json", "r") as f:
        result = json.loads(f.read())

    json_data = _extract_data_from_result(result, "tests/data/tmp-output.zip")
    assert json_data != None

def test_postprocess_elements():
    # assuming correct json_data and page_sizes
    with open("tests/data/tmp/structuredData.json", "r") as f:
        json_data = json.loads(f.read())

    processed_json_data = _postprocess_elements(json_data, page_sizes)
    assert processed_json_data != None

def test_process_pdf():
    # assuming a correct input_file_path
    result = process_pdf("tests/data/documents/moz.pdf")
    assert result != None

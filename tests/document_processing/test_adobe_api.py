import json
import os
import shutil
import pytest
from unittest import mock
from typing import Dict, Any

from piqa.document_processing.adobe_api import (process_pdf, _update_bounds, _preprocess_pdf, _call_adobe_service, _extract_data_from_result, _postprocess_elements) # type: ignore

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
    page_sizes = _preprocess_pdf("tests/data/documents/moz.pdf", "tests/data/tmp/documents/moz.pdf", 5, False)
    assert len(page_sizes) == 5

def test_call_adobe_service_and_extract_data_from_result():

    file_path = "tests/data/tmp/documents/moz.pdf"
    result = _call_adobe_service(file_path)

    json_data = _extract_data_from_result(result, "tests/data/tmp/tmp-output.zip")
    assert json_data != None

def test_postprocess_elements():
    # assuming correct json_data and page_sizes
    with open("tests/data/tmp/tmp-output.json", "r") as f:
        json_data = json.loads(f.read())

    # Todo: Improvement -> Share state between these tests to not duplicate logic
    page_sizes = _preprocess_pdf("tests/data/documents/moz.pdf", "tests/data/tmp/documents/moz.pdf", 5, False)
    processed_json_data = _postprocess_elements(json_data, page_sizes)
    assert processed_json_data != None

def test_process_pdf():
    # assuming a correct input_file_path
    result = process_pdf("tests/data/documents/moz.pdf")
    assert result != None

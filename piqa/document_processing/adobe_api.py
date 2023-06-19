# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
# Standard library imports
import json
import os
import shutil
import time
from glob import glob
from typing import Any, Dict, List, Optional
import zipfile

# Third party imports
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import (
    SdkException,
    ServiceApiException,
    ServiceUsageException,
)
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import (
    ExtractElementType,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import (
    ExtractPDFOptions,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import (
    ExtractRenditionsElementType,
)
from pdfrw import PdfReader, PdfWriter

# Local application imports
from piqa.config import logging

TMP_PATH = 'data/tmp'

def _update_bounds(element: Dict[str, Any], page_sizes: List[Dict[str, int]], dpi: int) -> None:
    bounds = element["Bounds"]
    page_index = element["Page"]
    page_size = page_sizes[page_index - 1]

    height = page_size["height"]
    width = page_size["width"]

    element["PercentileBounds"] = {
        "left": bounds[0] / width,
        "top": (height - bounds[3]) / height,
        "right": bounds[2] / width,
        "bottom": (height - bounds[1]) / height,
    }

    if element.get("CharBounds"):
        new_bounds = []
        for bound in element.get("CharBounds", []):
            new_bounds.append(
                {
                    "left": bounds[0] / width,
                    "top": (height - bounds[3]) / height,
                    "right": bounds[2] / width,
                    "bottom": (height - bounds[1]) / height,
                }
            )

        element["PercentileCharBounds"] = new_bounds


def _preprocess_pdf(input_file_path: str, output_file_path: str, max_number_pages: int, tail: bool) -> List[Dict[str, int]]:
    pdf_input = PdfReader(input_file_path)
    pdf_output_writer = PdfWriter()
    pages = pdf_input.pages[-max_number_pages:] if tail else pdf_input.pages[:max_number_pages] #type: ignore

    for page in pages: #type: ignore
        pdf_output_writer.addPage(page)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    pdf_output_writer.write(output_file_path)

    pdf_output = PdfReader(output_file_path)
    page_sizes = []

    for page_index, page in enumerate(pdf_output.pages): #type: ignore
        width, height = page.inheritable.MediaBox[-2:]
        width = int(float(width))
        height = int(float(height))
        page_sizes.append({"page_index": page_index, "width": width, "height": height})

    return page_sizes


def _call_adobe_service(file_path: str):
    credentials = (
        Credentials.service_account_credentials_builder()
            .from_file("credentials/pdfservices-api-credentials.json")
            .build()
    )

    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()

    source = FileRef.create_from_local_file(file_path)
    extract_pdf_operation.set_input(source)

    extract_pdf_options: ExtractPDFOptions = (
        ExtractPDFOptions.builder()
            .with_elements_to_extract(
                [
                    ExtractElementType.TEXT,
                    ExtractElementType.TABLES,
                ]
            )
            .with_elements_to_extract_renditions(
                [
                    ExtractRenditionsElementType.TABLES,
                    ExtractRenditionsElementType.FIGURES,
                ]
            )
            .build()
    )
    extract_pdf_operation.set_options(extract_pdf_options)

    result: FileRef = extract_pdf_operation.execute(execution_context)

    return result


def _extract_data_from_result(result, op_zip_file_path: str) -> Optional[Dict[str, Any]]:
    if os.path.exists(op_zip_file_path):
        os.remove(op_zip_file_path)

    result.save_as(op_zip_file_path)

    json_data = None
    with zipfile.ZipFile(op_zip_file_path, "r") as zip_ref:
        names = zip_ref.namelist()
        for name in names:
            if name.find("structuredData.json") == -1:
                continue
            with open("/tmp/structuredData.json", "wb") as f:
                json_data = json.loads(zip_ref.read(name))
                break

    logging.debug("Saved zip file to {op_zip_file_path}")

    return json_data


def _postprocess_elements(json_data: Dict[str, Any], page_sizes: List[Dict[str, int]], dpi: int = 72) -> Dict[str, Any]:
    for element in json_data["elements"]:
        if element.get("Bounds"):
            _update_bounds(element, page_sizes, dpi)

        if element.get("Kids"):
            for kid in element["Kids"]:
                if kid.get("Bounds"):
                    _update_bounds(kid, page_sizes, dpi)

    os.makedirs("data/adobe_outputs", exist_ok=True)
    return json_data

def process_pdf(input_file_path: str, max_number_pages: int = 1, tail: bool = False) -> Optional[Dict[str, Any]]:
    start_time = time.perf_counter()

    os.makedirs(TMP_PATH, exist_ok=True)

    root, _ = os.path.splitext(input_file_path)
    file_name = os.path.basename(root)
    output_file_path = f"data/processed_documents/{file_name}.pdf"

    existing_files = glob(f"data/adobe_outputs/{file_name}*.json")

    if existing_files:
        logging.debug("Not calling Adobe SDK, file already processed")
        shutil.rmtree(TMP_PATH)

        with open(existing_files[0]) as json_file:
            return json.load(json_file)

    page_sizes = _preprocess_pdf(input_file_path, output_file_path, max_number_pages, tail)

    logging.debug(f"[{round(time.perf_counter() - start_time, 2)}s] Starting...")

    try:
        result = _call_adobe_service(output_file_path)

        op_zip_file_path = f'{output_file_path.replace("processed_documents", "tmp")}-output.zip'
        json_data = _extract_data_from_result(result, op_zip_file_path)

        if not json_data:
            logging.warning(f"[{round(time.perf_counter() - start_time, 2)}s] No data extracted")
            return None

        processed_json_data = _postprocess_elements(json_data, page_sizes)

        op_json_file_path = (
            op_zip_file_path.replace(".zip", "_transformed.json").replace("tmp", "adobe_outputs").replace(".pdf", "")
        )

        with open(op_json_file_path, "w+") as f:
            f.write(json.dumps(processed_json_data))

        logging.debug(f"[{round(time.perf_counter() - start_time, 2)}s] Transformed JSON data and written to {op_json_file_path}")

        logging.debug(f"[{round(time.perf_counter() - start_time, 2)}s] Finished")
        logging.debug(
            "--------------------------------------------------------------------------------------------------------------"
        )

        # shutil.rmtree(TMP_PATH)

    except (SdkException, ServiceApiException, ServiceUsageException) as err:
        logging.error(f"[{round(time.perf_counter() - start_time, 2)}s] Exception encountered: {err}")
        shutil.rmtree(TMP_PATH)

        return None

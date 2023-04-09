# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from io import BytesIO
import logging
import os
from glob import glob
import shutil
import time
import zipfile
import json
from typing import List, Optional, Dict,  Any

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import (
    ServiceApiException,
    ServiceUsageException,
    SdkException,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import (
    ExtractPDFOptions,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import (
    ExtractElementType,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import (
    ExtractRenditionsElementType,
)
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from pdfrw import PdfReader, PdfWriter

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

TMP_PATH = "data/tmp"

def _update_bounds(element: Dict[str, Any], page_sizes: List[Dict[str, int]], dpi: int) -> None:
    """Update bounds in the given element.

    Args:
        element (Dict[str, Any]): The element to update.
        page_sizes (List[Dict[str, int]]): The list of page sizes.
        dpi (int): The DPI value for calculations.
    """
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
        for bound in element.get("CharBounds"):
            new_bounds.append(
                {
                    "left": bounds[0] / width,
                    "top": (height - bounds[3]) / height,
                    "right": bounds[2] / width,
                    "bottom": (height - bounds[1]) / height,
                }
            )

        element["PercentileCharBounds"] = new_bounds

def _preprocess_pdf(input_file_path: str, output_file_path: str, file_name: str, max_number_pages: int, tail: bool) -> List[Dict[str, int]]:
    """Preprocess a PDF file by selecting a specified number of pages from the beginning or end.

    Args:
        input_file_path (str): Path to the input PDF file.
        output_file_path (str): Path to the output preprocessed PDF file.
        file_name (str): The base name of the input file without extension.
        max_number_pages (int): Maximum number of pages to extract from the input file.
        tail (bool): If True, extract pages from the end, otherwise from the beginning.

    Returns:
        List[Dict[str, int]]: A list of dictionaries containing page indices and sizes.
    """
    pdf_input = PdfReader(input_file_path)

    pdf_output_writer = PdfWriter()
    pages = pdf_input.pages[-max_number_pages:] if tail else pdf_input.pages[:max_number_pages]

    for page in pages:
        pdf_output_writer.addPage(page)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    pdf_output_writer.write(output_file_path)

    pdf_output = PdfReader(output_file_path)

    page_sizes = []

    for page_index, page in enumerate(pdf_output.pages):
        width, height = page.inheritable.MediaBox[-2:]
        width = int(float(width))
        height = int(float(height))

        page_sizes.append({"page_index": page_index, "width": width, "height": height})

    return page_sizes

def process_pdf(input_file_path: str, max_number_pages: int = 1, tail: bool = False) -> Optional[None]:
    """Process a PDF file using Adobe PDF Services SDK.

    Args:
        input_file_path (str): Path to the input PDF file.
        max_number_pages (int, optional): Maximum number of pages to process. Defaults to 1.
        tail (bool, optional): If True, process pages from the end, otherwise from the beginning. Defaults to False.

    Returns:
        Optional[None]: None if the file has already been processed.
    """
    os.makedirs(TMP_PATH, exist_ok=True)

    root, _ = os.path.splitext(input_file_path)
    file_name = os.path.basename(root)
    output_file_path = f"data/processed_documents/{file_name}.pdf"

    existing_files = glob(f"data/adobe_outputs/{file_name}*.json")

    if existing_files:
        logging.info("Not calling Adobe SDK, file already processed")
        shutil.rmtree(TMP_PATH)
        return None

    page_sizes = _preprocess_pdf(input_file_path, output_file_path, file_name, max_number_pages, tail)

    start_time = time.perf_counter()

    try:
        logging.info(f"[{round(time.perf_counter() - start_time, 2)}s] Starting...")

        credentials = (
            Credentials.service_account_credentials_builder()
            .from_file("config/pdfservices-api-credentials.json")
            .build()
        )

        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        source = FileRef.create_from_local_file(output_file_path)
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

        op_zip_file_path = f'{output_file_path.replace("processed_documents", "tmp")}-output.zip'

        if os.path.exists(op_zip_file_path):
            os.remove(op_zip_file_path)

        result.save_as(op_zip_file_path)

        logging.info(f"[{round(time.perf_counter() - start_time, 2)}s] Saved zip file to {op_zip_file_path}")

        with zipfile.ZipFile(op_zip_file_path, "r") as zip_ref:
            names = zip_ref.namelist()
            for name in names:
                if name.find("structuredData.json") == -1:
                    continue
                with open("/tmp/structuredData.json", "wb") as f:
                    json_data = json.loads(zip_ref.read(name))
                    break

        op_json_file_path = (
            op_zip_file_path.replace(".zip", "_transformed.json").replace("tmp", "adobe_outputs").replace(".pdf", "")
        )

        dpi = 72

        for element in json_data["elements"]:

            if element.get("Bounds"):
                _update_bounds(element, page_sizes, dpi)

            if element.get("Kids"):
                for kid in element["Kids"]:
                    if kid.get("Bounds"):
                        _update_bounds(kid, page_sizes, dpi)

        os.makedirs("data/adobe_outputs", exist_ok=True)

        with open(op_json_file_path, "w+") as f:
            f.write(json.dumps(json_data))

        logging.info(f"[{round(time.perf_counter() - start_time, 2)}s] Transformed JSON data and written to {op_json_file_path}")

        logging.info(f"[{round(time.perf_counter() - start_time, 2)}s] finished")
        logging.info(
            "--------------------------------------------------------------------------------------------------------------"
        )

        shutil.rmtree(TMP_PATH)

    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")
        shutil.rmtree(TMP_PATH)

if __name__ == "__main__":
    log_level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(level=log_level)

    file_path = "data/documents/buffer.pdf"
    process_pdf(file_path, max_number_pages=5, tail=False)

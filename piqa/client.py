import os
from dotenv import load_dotenv
from typing import Optional, Union

from .config import logging
from .document_processing import (process_pdf,
                                  convert_pdf_to_images,
                                  flatten_and_preprocess_adobe_json)
from .image_processing import detect_paragraphs
from .large_language_models import get_chat_completion

load_dotenv()

class PiQaClient:
    """Client to handle Pitch Deck operations.

    Args:
        max_number_pages (int, optional): Maximum number of pages. Defaults to 5.
        tail (bool, optional): Tail option for page processing. Defaults to False.

    Attributes:
        max_number_pages (int): Maximum number of pages.
        tail (bool): Tail option for page processing.
    """
    def __init__(self, max_number_pages: int = 5, tail: bool = False):
        self.max_number_pages = max_number_pages
        self.tail = tail

    def generate_pitchdeck_metrics(self, file_path: str) -> Union[str, dict]:
        """Generate pitch deck metrics.

        Args:
            file_path (str): Path to the input file.

        Returns:
            Union[str, dict]: Metrics result or error message.
        """
        try:
            adobe_json_data = process_pdf(file_path, self.max_number_pages, self.tail)

            if not adobe_json_data:
                return "No data extracted"

            df = flatten_and_preprocess_adobe_json(adobe_json_data)
            completion_result = get_chat_completion(df)

            return completion_result

        except Exception as e:
            logging.error(f"Error generating pitch deck metrics: {e}")
            return "Error generating pitch deck metrics"

    def _optional_enhancements(self, file_path: str) -> Optional[str]:
        """Optional enhancements like image conversion and paragraph detection.

        Args:
            file_path (str): Path to the input file.

        Returns:
            Optional[str]: Error message, if any.
        """
        try:
            page_image_paths = convert_pdf_to_images(file_path)

            for page_image_path in page_image_paths:
                detect_paragraphs(page_image_path)

        except Exception as e:
            logging.error(f"Error in optional enhancements: {e}")
            return "Error in optional enhancements"

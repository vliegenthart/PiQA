from pdf2image import convert_from_path
from typing import List
from PIL import Image
import os


def convert_pdf_to_images(path: str) -> List[str]:
    """
    Converts each page of a PDF file into separate images and saves them.

    The images are saved in the PNG format with names in the pattern 'output_{i}.png',
    where '{i}' is the page number starting from 0.

    Args:
        path (str): The path to the PDF file to be converted.

    Returns:
        int: The number of pages of the PDF
    """
    images = convert_from_path(path)

    filename_with_extension = os.path.basename(path)
    filename_without_extension = os.path.splitext(filename_with_extension)[0]

    page_image_paths = []
    for i, image in enumerate(images):
        image_path = f'data/images/{filename_without_extension}_{i}.png'

        image.save(image_path, 'PNG')
        page_image_paths.append(image_path)

    return page_image_paths

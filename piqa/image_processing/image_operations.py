import cv2
import numpy as np
from typing import Tuple, List

from piqa.config import logging

def detect_paragraphs(image_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[Tuple[int, int, int, int]]]:
    """
    Detect paragraphs in a text document image and draw bounding rectangles around them.

    This function detects paragraphs in a text document image with non-consistent text
    structure using image processing techniques like grayscaling, Gaussian blur,
    Otsu's thresholding, and dilation.

    Args:
        image_path: The path to the input image file.

    Returns:
        Tuple of the generated images (thresholded, dilated, and original with rectangles)
        and a list of the rectangles drawn on top of the image.
    """

    # Load image, grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=12)

    # Find contours and draw rectangle
    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    rectangles = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + width, y + height), (36, 255, 12), 2)
        rectangles.append((x, y, width, height))

    cv2.imshow('thresh', thresh)
    cv2.imshow('dilate', dilate)
    cv2.imshow('image', image)
    cv2.waitKey()

    return thresh, dilate, image, rectangles


# How to read the text:
# 1. Take bounding boxes above
# 2. OCR: Get all text elements
# 3. Sort by left, then top coordinate
# 4. Aggregate that list

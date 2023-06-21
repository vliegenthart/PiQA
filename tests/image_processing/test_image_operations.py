import cv2
import numpy as np
import pytest
from PIL import Image, ImageDraw, ImageFont

from piqa.image_processing import detect_paragraphs

def create_test_image(text: str, width: int, height: int, font_size: int, filename: str) -> None:
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))
    image.save(f"tests/data/images/{filename}")

def generate_test_images() -> None:
    print("CREATING TEST IMAGES")
    text_single_paragraph = "This is a single paragraph. It has multiple lines and sentences, but it is still a single paragraph."
    text_two_paragraphs = "This is the first paragraph.\n\nThis is the second paragraph."
    text_paragraphs_with_space = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"

    create_test_image(text_single_paragraph, 300, 100, 16, "single_paragraph.png")
    create_test_image(text_two_paragraphs, 300, 150, 16, "two_paragraphs.png")
    create_test_image(text_paragraphs_with_space, 300, 200, 16, "paragraphs_with_space.png")

# Temporarily disabled; This feature is to be built in the future

# def test_detect_paragraphs_empty_image() -> None:
#     empty_image = np.zeros((100, 100), dtype=np.uint8)
#     cv2.imwrite("data/images/empty_image.png", empty_image)

#     thresh, dilate, image = detect_paragraphs("data/images/empty_image.png")

#     assert np.array_equal(thresh, empty_image)
#     assert np.array_equal(dilate, empty_image)
#     assert np.array_equal(image, cv2.cvtColor(empty_image, cv2.COLOR_GRAY2BGR))

# def test_detect_paragraphs_no_text_image() -> None:
#     no_text_image = np.ones((100, 100), dtype=np.uint8) * 255
#     cv2.imwrite("data/images/no_text_image.png", no_text_image)

#     thresh, dilate, image = detect_paragraphs("data/images/no_text_image.png")

#     assert np.array_equal(thresh, no_text_image)
#     assert np.array_equal(dilate, no_text_image)
#     assert np.array_equal(image, cv2.cvtColor(no_text_image, cv2.COLOR_GRAY2BGR))

# def test_detect_paragraphs_invalid_path() -> None:
#     with pytest.raises(cv2.error):
#         detect_paragraphs("invalid_path.png")

# def test_detect_paragraphs_single_paragraph() -> None:
#     single_paragraph = cv2.imread("data/images/single_paragraph.png")

#     _, _, _, rectangles = detect_paragraphs("data/images/single_paragraph.png")

#     assert len(rectangles) == 1

# def test_detect_paragraphs_two_paragraphs() -> None:
#     two_paragraphs = cv2.imread("data/images/two_paragraphs.png")

#     _, _, _, rectangles = detect_paragraphs("data/images/two_paragraphs.png")

#     assert len(rectangles) == 2

# def test_detect_paragraphs_paragraphs_with_space() -> None:
#     paragraphs_with_space = cv2.imread("data/images/paragraphs_with_space.png")

#     _, _, _, rectangles = detect_paragraphs("data/images/paragraphs_with_space.png")

#     assert len(rectangles) == 3

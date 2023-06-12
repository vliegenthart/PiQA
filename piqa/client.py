
from .document_processing import process_pdf, convert_pdf_to_images, flatten_and_preprocess_adobe_json
from .image_processing import detect_paragraphs
from .large_language_models import get_chat_completion



from .utils import relative_path
from .config import logging

class PiQaClient:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def generate_pitchdeck_metrics(self, max_number_pages=5, tail=False):

        # TODO: Parallelize this
        # Processing the PDF
        adobe_json_data = process_pdf(self.pdf_path, max_number_pages, tail)

        df = flatten_and_preprocess_adobe_json(adobe_json_data)

        result = get_chat_completion(df)
        print(result)
        # Optional Enhancements
        # # Generate images from PDF
        # page_image_paths = convert_pdf_to_images(self.pdf_path)

        # # Detecting paragraphs
        # for page_image_path in page_image_paths:
        #     detect_paragraphs(page_image_path)



# from document_processing import process_pdf


# file_paths = glob(os.path.splitext(folder_path)[0] + "*.pdf")

# print(f"Processing {len(file_paths)} PDFs, with max number of pages each of {max_number_pages}")

# for path in file_paths:
#     process_pdf(...)



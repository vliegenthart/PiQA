
from adobe_utils import process_pdf


file_paths = glob(os.path.splitext(folder_path)[0] + "*.pdf")

print(f"Processing {len(file_paths)} PDFs, with max number of pages each of {max_number_pages}")

for path in file_paths:
    process_pdf(...)

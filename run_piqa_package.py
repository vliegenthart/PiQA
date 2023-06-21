import os
from dotenv import load_dotenv
load_dotenv()

from piqa import PiQaClient
from piqa.config import logging

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if __name__ == "__main__":
    input_name = "moz"
    file_path = f"data/documents/{input_name}.pdf"

    client = PiQaClient()
    output = client.generate_pitchdeck_metrics(file_path)

    output_folder = "data/final_output"
    os.makedirs(output_folder, exist_ok=True)

    final_output_path = f"{output_folder}/{input_name}_{OPENAI_MODEL}_result.md"
    with open(final_output_path, "w") as f:
        f.write(output)

        logging.info(f"The final output was written to {final_output_path}")



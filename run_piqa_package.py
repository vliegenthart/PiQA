import os
from dotenv import load_dotenv
load_dotenv()

from piqa import PiQaClient

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if __name__ == "__main__":
    input_name = "moz"
    file_path = f"data/documents/{input_name}.pdf"

    client = PiQaClient()
    output = client.generate_pitchdeck_metrics(file_path)

    output_folder = "data/final_output"
    os.makedirs(output_folder, exist_ok=True)

    with open(f"{output_folder}/{input_name}_{OPENAI_MODEL}_result.md", "w") as f:
        f.write(output)



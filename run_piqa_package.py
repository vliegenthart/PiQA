from piqa import PiQaClient
import pandas as pd
import json

if __name__ == "__main__":
    name = "intercom"
    file_path = f"data/documents/{name}.pdf"
    client = PiQaClient(file_path)
    client.generate_pitchdeck_metrics()



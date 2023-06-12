import json
import pandas as pd
from typing import Dict, Any

def flatten_and_preprocess_adobe_json(json_data: Dict[Any, Any]) -> pd.DataFrame:
    # Create DataFrame
    df = pd.json_normalize(json_data['elements'])

    # Filter rows based on Text column
    df_filtered = df.dropna(subset=['Text'])
    df_filtered = df_filtered[df_filtered['Text'].str.len() >= 3]

    return df_filtered


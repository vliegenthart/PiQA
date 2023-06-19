from typing import Dict, Any

import pandas as pd

def flatten_and_preprocess_adobe_json(json_data: Dict[Any, Any]) -> pd.DataFrame:
    """
    Flatten the input JSON data and filter out the rows based on the 'Text' column.

    Args:
        json_data (Dict[Any, Any]): The input JSON data.

    Returns:
        pd.DataFrame: The preprocessed dataframe after flattening and filtering.
    """
    try:
        # Create DataFrame
        df = pd.json_normalize(json_data, 'elements')

        # Filter rows based on Text column
        df_filtered = df.dropna(subset=['Text'])
        df_filtered = df_filtered[df_filtered['Text'].str.len() >= 3]

        return df_filtered

    except KeyError as e:
        raise KeyError(f"Key not found in the provided JSON data: {e}") from e
    except Exception as e:
        raise Exception(f"An error occurred while processing the JSON data: {e}") from e

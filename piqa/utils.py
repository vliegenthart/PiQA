import os

def relative_path(file: str, path: str) -> str:
    """Get the absolute path of a file relative to the current file's directory.

    Args:
        path (str): The relative path to the file.

    Returns:
        str: The absolute path to the file.
    """

    # Get the path of the current file
    current_file_path = os.path.abspath(file)

    # Get the directory containing the current file
    current_directory = os.path.dirname(current_file_path)

    return os.path.join(current_directory, path)

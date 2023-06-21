import os
import shutil

from image_processing.test_image_operations import generate_test_images

TMP_PATH = 'tests/data/tmp'

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    # Reset temporary folder to save outputs from test run


    _reset_folder(TMP_PATH)
    _reset_folder("tests/data/images")

    generate_test_images()

def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """

    _reset_folder(TMP_PATH)
    _reset_folder("tests/data/images")

def _reset_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path, exist_ok=True)



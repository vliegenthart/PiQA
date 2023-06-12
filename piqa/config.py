import os
import logging

log_level = os.environ.get("LOGLEVEL", "INFO")
logging.basicConfig(level=log_level)

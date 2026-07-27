import logging
import os
import sys

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "hirunews_tagline.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_logger = logging.getLogger("HiruTagline")


def log_info(msg):
    _logger.info(msg)


def log_warning(msg):
    _logger.warning(msg)


def log_error(context, error):
    _logger.error(f"{context}: {error}", exc_info=True)


def get_logger():
    return _logger

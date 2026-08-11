import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "redring.log"

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def configure_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("redring")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
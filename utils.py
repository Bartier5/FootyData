import logging
import time
import os
from config import LOG_DIR, LOG_PATH, LOG_LEVEL

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(stream=open(1, "w", encoding="utf-8", closefd=False))
    ]
)

logger = logging.getLogger("FOOTYDATA")
def log_call(func):
    def wrapper(*args, **kwargs):
        logger.info(f"▶ Running: {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = round(time.time() - start, 2)
        logger.info(f"✓ Done: {func.__name__} | took {elapsed}s")
        return result
    return wrapper
def row_generator(data: list):
    for row in data:
        yield row
        
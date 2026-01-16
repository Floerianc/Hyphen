import logging
from typing import Callable

logging.basicConfig(
    filename="./log.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s (%(filename)s, L. %(lineno)d)"
)
log = logging.getLogger(__name__)

def log_event(msg: str):
    """Simple logging function

    Logs a message and the function name

    Args:
        msg (str): Message
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            log.info(f"{func.__name__}: {msg}")
            result = func(*args, **kwargs) # type: ignore
            return result
        return wrapper
    return decorator
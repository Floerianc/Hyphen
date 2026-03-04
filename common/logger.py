import logging
from typing import (
    Callable,
    Union
)
from core.dates import DateHandler

def setup_logger(
    log_name: str,
    log_file: str,
    level=logging.INFO,
    filemode: str = "w"
) -> logging.Logger:
    handler = logging.FileHandler(filename=log_file, mode=filemode)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(log_name)
    
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

def log_event(
    msg: str,
    _level: Union[int, str] = logging.NOTSET
) -> None:
    # log.info(f"{func.__name__}: {msg}")
    if isinstance(_level, str):
        level = logging._nameToLevel.get(_level, logging.NOTSET)
    else:
        level = _level
    
    if level >= logging.ERROR:
        error_logger = setup_logger(
            log_name="error logger",
            log_file=get_exception_log(),
            level=logging.ERROR,
            filemode="a"
        )
        logger.exception(msg=msg)
        error_logger.exception(msg=msg)
        del error_logger
    else:
        logger.log(level=level, msg=msg)

def log_decorator(
    msg: str,
    _level: int | str = logging.INFO,
):
    """Simple logging function

    Logs a message and the function name with a specified level

    Args:
        msg (str): Message
        _level: (logging._Level): logging level
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            log_event(msg=msg, _level=_level)
            return func(*args, **kwargs) # type: ignore
        return wrapper
    return decorator

def cleanup() -> None:
    open(LOG1_FILE, "w").close()

def get_exception_log() -> str:
    return f"./logs/{date.date.strftime("%Y_%m_%d_log.log")}"


date = DateHandler()
LOG1_FILE = "./logs/NEWESTLOG.log"
LOG2_FILE = get_exception_log()

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

logger = setup_logger(
    log_name=__name__,
    log_file=LOG1_FILE,
    filemode="w"
)
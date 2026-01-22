import os
from datetime import datetime

INCLUDE_PATH    = "./include/"
ASSETS_PATH     = "./assets/"
BIN_PATH        = os.path.join(INCLUDE_PATH, "rgbmatrix/")
FONT_PATH       = os.path.join(ASSETS_PATH, "fonts/")
ICON_PATH       = os.path.join(ASSETS_PATH, "icons/")

# def wrap_idx_around(idx1: int, idx2: int, start: int, end: int) -> List[int]:
#     excess = (end * (idx1 // end))
#     idx1 -= excess
#     idx2 -= excess

#     before_wrap = end - idx1
#     valid_indeces = round(start, end)

def tz_date() -> datetime:
    tz = datetime.now().astimezone().tzinfo
    return datetime.now(tz)

def resolve_path(path: str) -> str:
    path = os.path.abspath(path)
    if os.path.exists(path):
        return path
    else:
        raise OSError(f"Can't find file.\nPath: {path}")
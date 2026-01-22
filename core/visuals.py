import os
from typing import (
    Any,
    Iterable,
    Tuple,
    List
)
from PIL import (
    Image,
    ImageFile
)

import util.utils as utils
from common.typing import (
    Color,
    Pixel,
)
from util.utils import ICON_PATH


class MatrixImage:
    def __init__(
        self,
        filename: str
    ) -> None:
        super().__init__()
        self.path = utils.resolve_path(filename)
        self.pixel_matrix: List[List[Pixel]] = [[]]
        
        img = Image.open(self.path)
        self.pixel_matrix = self._img_to_px(img)
    
    def _img_to_px(
        self,
        img: ImageFile.ImageFile,
    ) -> List[List[Pixel]]:
        # img[x, y] = RGBA value
        pixels: List[List[Pixel]] = []
        rgba_values = img.convert("RGBA").getdata()
        
        width, height = img.size
        position = -width
        
        for y_pos in range(height):
            pixels.append(list())
            position += width
            
            for x_pos in range(width):
                pixel = rgba_values[position + x_pos]
                r, g, b, a = pixel
                c = Color(r, g, b)
                px = Pixel(True if a else False, color=c)
                pixels[y_pos].append(px)
        return pixels


CLR_RED                 =   Color(255,    0,      0)
CLR_GREEN               =   Color(0,      255,    0)
CLR_CYAN                =   Color(0,      255,    255)
CLR_DARK_BRIGHT_BLUE    =   Color(32,     121,    153)
CLR_BRIGHT_BLUE         =   Color(0,      187,    255)
CLR_BRIGHTER_BLUE       =   Color(168,    232,    255)
CLR_DARKEST_SUN         =   Color(255,    174,    0)
CLR_DARKER_SUN          =   Color(255,    208,    0)
CLR_SUN                 =   Color(255,    255,    0)
CLR_FOG                 =   Color(161,    161,    161)
CLR_WHITE               =   Color(255,    255,    255)
CLR_BLACK               =   Color(0,      0,      0)
CLR_YELLOW              =   Color(255,    255,    0)
CLR_CLOUD_0             =   Color(60,     60,     60)
CLR_CLOUD_1             =   Color(212,    212,    212)


# FOR WEATHER ICONS: 9x9 PIXELS!

#0, 1, 2, 3
IMG_SUN = MatrixImage(os.path.join(ICON_PATH, "IMG_SUN.png")).pixel_matrix
#45 ,48
IMG_FOG = MatrixImage(os.path.join(ICON_PATH, "IMG_FOG.png")).pixel_matrix
#51, 53, 55. 56, 57
IMG_DRIZZLE = MatrixImage(os.path.join(ICON_PATH, "IMG_DRIZZLE.png")).pixel_matrix
#61, 63, 65. 66. 67
IMG_RAINDROP = MatrixImage(os.path.join(ICON_PATH, "IMG_RAINDROP.png")).pixel_matrix
#71, 73, 75, 77
IMG_SNOWFLAKE = MatrixImage(os.path.join(ICON_PATH, "IMG_SNOWFLAKE.png")).pixel_matrix
#80, 81, 82
IMG_RAIN_SHOWER = MatrixImage(os.path.join(ICON_PATH, "IMG_RAIN_SHOWER.png")).pixel_matrix
#85, 86
IMG_SNOW_SHOWER = MatrixImage(os.path.join(ICON_PATH, "IMG_SNOW_SHOWER.png")).pixel_matrix
#95, 96, 99
IMG_THUNDER = MatrixImage(os.path.join(ICON_PATH, "IMG_THUNDER.png")).pixel_matrix



HVV_LOGO_BASE = MatrixImage(os.path.join(ICON_PATH, "HVVBASE.png")).pixel_matrix
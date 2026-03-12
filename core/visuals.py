import os
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


class MatrixImage(list):
    def __init__(
        self,
        filename: str
    ) -> None:
        super().__init__()
        self.path = utils.resolve_path(filename)
        
        img = Image.open(self.path)
        self._img_to_px(img)
    
    def _img_to_px(
        self,
        img: ImageFile.ImageFile,
    ) -> None:
        """Converts an image to RGBA tuples

        Uses PIL to convert an image to a large
        list of RGBA tuples which is then processed
        into a 2 dimensional array of RGBA tuples, basically
        storing the image as each individual pixel

        Args:
            img (ImageFile.ImageFile): PIL Image

        Returns:
            List[List[Pixel]]: 2D list of pixels
        """
        # img[x, y] = RGBA value
        rgba_values = img.convert("RGBA").getdata()
        
        width, height = img.size
        position = -width
        
        for y_pos in range(height):
            self.append(list())
            position += width
            
            for x_pos in range(width):
                pixel = rgba_values[position + x_pos]
                r, g, b, a = pixel
                c = Color(r, g, b)
                px = Pixel(True if a else False, color=c)
                self[y_pos].append(px)


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
IMG_SUN = MatrixImage(os.path.join(ICON_PATH, "IMG_SUN.png"))
#45 ,48
IMG_FOG = MatrixImage(os.path.join(ICON_PATH, "IMG_FOG.png"))
#51, 53, 55. 56, 57
IMG_DRIZZLE = MatrixImage(os.path.join(ICON_PATH, "IMG_DRIZZLE.png"))
#61, 63, 65. 66. 67
IMG_RAINDROP = MatrixImage(os.path.join(ICON_PATH, "IMG_RAINDROP.png"))
#71, 73, 75, 77
IMG_SNOWFLAKE = MatrixImage(os.path.join(ICON_PATH, "IMG_SNOWFLAKE.png"))
#80, 81, 82
IMG_RAIN_SHOWER = MatrixImage(os.path.join(ICON_PATH, "IMG_RAIN_SHOWER.png"))
#85, 86
IMG_SNOW_SHOWER = MatrixImage(os.path.join(ICON_PATH, "IMG_SNOW_SHOWER.png"))
#95, 96, 99
IMG_THUNDER = MatrixImage(os.path.join(ICON_PATH, "IMG_THUNDER.png"))



HVV_LOGO_BASE = MatrixImage(os.path.join(ICON_PATH, "HVVBASE.png"))
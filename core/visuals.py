from common.typing import (
    Color,
    Pixel,
    Image
)


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
# Ja, ich hätte das auch mit .pngs oder so machen können, 
# die ich dann parse, aber ich bin zu faul dafür gerade und 
# mir geht langsam die Zeit aus, also bitte verzeiht mir 
# diesen absolut gottlosen Code

#0, 1, 2, 3
IMG_SUN: Image = [
    [Pixel(False),              Pixel(True, CLR_DARKER_SUN),     Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(False)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN),         Pixel(True, CLR_SUN)],
    [Pixel(True, CLR_DARKEST_SUN),  Pixel(True, CLR_DARKEST_SUN),    Pixel(True, CLR_DARKEST_SUN), Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_DARKER_SUN),  Pixel(True, CLR_DARKER_SUN)],
    [Pixel(False),              Pixel(True, CLR_DARKER_SUN),     Pixel(True, CLR_DARKEST_SUN), Pixel(True, CLR_DARKEST_SUN), Pixel(True, CLR_DARKEST_SUN), Pixel(True, CLR_DARKEST_SUN), Pixel(True, CLR_DARKEST_SUN), Pixel(True, CLR_DARKEST_SUN), Pixel(False)]
]
#45 ,48
IMG_FOG: Image = [
    [Pixel(False),      Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False)],
    [Pixel(True, CLR_FOG),  Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(False),       Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(False),       Pixel(True, CLR_FOG)],
    [Pixel(False),      Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False)],
    [Pixel(True, CLR_FOG),  Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG)],
    [Pixel(False),      Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False)],
    [Pixel(True, CLR_FOG),  Pixel(True, CLR_FOG),   Pixel(False),       Pixel(False),       Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG)],
    [Pixel(False),      Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False)],
    [Pixel(True, CLR_FOG),  Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(False),       Pixel(False),       Pixel(True, CLR_FOG),   Pixel(True, CLR_FOG),   Pixel(False),       Pixel(True, CLR_FOG)],
    [Pixel(False),      Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False),       Pixel(False)],
]
#51, 53, 55. 56, 57
IMG_DRIZZLE: Image = [
    [Pixel(False), Pixel(False),                    Pixel(False), Pixel(False),                     Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False)],
    [Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),  Pixel(False), Pixel(False),                     Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False)],
    [Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),  Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),   Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False),                   Pixel(False)],
    [Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),  Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),   Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(False)],
    [Pixel(False), Pixel(False),                    Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),   Pixel(False),                   Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False)],
    [Pixel(False), Pixel(False),                    Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),   Pixel(False),                   Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False)],
    [Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),  Pixel(False), Pixel(False),                     Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(False)],
    [Pixel(False), Pixel(True, CLR_BRIGHT_BLUE),  Pixel(False), Pixel(False),                     Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False),                   Pixel(False)],
    [Pixel(False), Pixel(False),                    Pixel(False), Pixel(False),                     Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False),                   Pixel(False)],
]
#61, 63, 65. 66. 67
IMG_RAINDROP: Image = [
[Pixel(False),                      Pixel(False),                       Pixel(False),                       Pixel(True, CLR_BRIGHT_BLUE),     Pixel(False),                       Pixel(False),                       Pixel(False)],
[Pixel(False),                      Pixel(False),                       Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(False),                       Pixel(False)],
[Pixel(False),                      Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(False)],
[Pixel(True, CLR_BRIGHTER_BLUE),  Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE)],
[Pixel(True, CLR_BRIGHTER_BLUE),  Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE)],
[Pixel(True, CLR_BRIGHTER_BLUE),  Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_DARK_BRIGHT_BLUE)],
[Pixel(True, CLR_BRIGHTER_BLUE),  Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_DARK_BRIGHT_BLUE)],
[Pixel(True, CLR_BRIGHTER_BLUE),  Pixel(True, CLR_BRIGHTER_BLUE),   Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_DARK_BRIGHT_BLUE),Pixel(True, CLR_DARK_BRIGHT_BLUE)],
[Pixel(False),                      Pixel(True, CLR_BRIGHTER_BLUE),   Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_BRIGHT_BLUE),     Pixel(True, CLR_DARK_BRIGHT_BLUE),Pixel(True, CLR_DARK_BRIGHT_BLUE),Pixel(False)],
[Pixel(False),                      Pixel(False),                       Pixel(True, CLR_DARK_BRIGHT_BLUE),Pixel(True, CLR_DARK_BRIGHT_BLUE),Pixel(True, CLR_DARK_BRIGHT_BLUE),Pixel(False), Pixel(False)],
]
#71, 73, 75, 77
IMG_SNOWFLAKE: Image = [
    [Pixel(True),   Pixel(False),   Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False),   Pixel(False),   Pixel(True)],
    [Pixel(False),  Pixel(True),    Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False)],
    [Pixel(False),  Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False),   Pixel(False)],
    [Pixel(False),  Pixel(False),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False)],
    [Pixel(True),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(True),    Pixel(True),    Pixel(False),   Pixel(True),    Pixel(True)],
    [Pixel(False),  Pixel(False),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False)],
    [Pixel(False),  Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False),   Pixel(False)],
    [Pixel(False),  Pixel(True),    Pixel(False),   Pixel(False),   Pixel(False),   Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False)],
    [Pixel(True),   Pixel(False),   Pixel(False),   Pixel(False),   Pixel(True),    Pixel(False),   Pixel(False),   Pixel(False),   Pixel(True)]
]
#80, 81, 82
IMG_RAIN_SHOWER: Image = [
    [Pixel(True, CLR_CLOUD_0),    Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_0)],
    [Pixel(True, CLR_CLOUD_1),    Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_1)],
    [Pixel(False),                  Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(True, CLR_CLOUD_1)],
    [Pixel(False),                  Pixel(False),                   Pixel(False),                   Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(False),                   Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(False)],
    [Pixel(False),                  Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False)],
    [Pixel(False),                  Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),               Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False)],
    [Pixel(False),                  Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),               Pixel(True, CLR_BRIGHT_BLUE)],
    [Pixel(False),                  Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False),               Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(False),               Pixel(True, CLR_BRIGHT_BLUE)],
    [Pixel(False),                  Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),                   Pixel(True, CLR_BRIGHT_BLUE), Pixel(False),               Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False)]
]    
#85, 86
IMG_SNOW_SHOWER: Image = [
    [Pixel(True, CLR_CLOUD_0),    Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_0)],
    [Pixel(True, CLR_CLOUD_1),    Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_0),     Pixel(True, CLR_CLOUD_0), Pixel(True, CLR_CLOUD_1)],
    [Pixel(False),                  Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(True, CLR_CLOUD_1)],
    [Pixel(False),                  Pixel(False),                   Pixel(False),                   Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(False),                   Pixel(True, CLR_CLOUD_1),     Pixel(True, CLR_CLOUD_1), Pixel(False)],
    [Pixel(False),                  Pixel(True, CLR_WHITE),       Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False)],
    [Pixel(False),                  Pixel(True, CLR_WHITE),       Pixel(False),                   Pixel(True, CLR_WHITE), Pixel(False),                     Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False)],
    [Pixel(False),                  Pixel(False),                   Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False),                   Pixel(True, CLR_WHITE),       Pixel(False),               Pixel(True, CLR_WHITE)],
    [Pixel(False),                  Pixel(False),                   Pixel(True, CLR_WHITE),       Pixel(False),                   Pixel(False),               Pixel(True, CLR_WHITE),       Pixel(False),                   Pixel(False),               Pixel(True, CLR_WHITE)],
    [Pixel(False),                  Pixel(True, CLR_WHITE),       Pixel(False),                   Pixel(True, CLR_WHITE), Pixel(False),                     Pixel(False),                   Pixel(False),                   Pixel(False),               Pixel(False)]
]
#95, 96, 99
IMG_THUNDER: Image = [
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),           Pixel(False),           Pixel(False),           Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),           Pixel(False),           Pixel(False),           Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),           Pixel(False),           Pixel(False),           Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),           Pixel(False),           Pixel(False),           Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(False),           Pixel(False),           Pixel(False),           Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(False),           Pixel(False),           Pixel(False),           Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),       Pixel(False)],
    [Pixel(False),  Pixel(False),           Pixel(False),           Pixel(False),           Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(True, CLR_YELLOW),    Pixel(False),       Pixel(False)],
]

HVV_LOGO_BASE: Image = [
    [Pixel(False),  Pixel(False),   Pixel(False),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(False),   Pixel(False),   Pixel(False)],
    [Pixel(False),  Pixel(False),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(False),   Pixel(False)],
    [Pixel(False),  Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(False)],
    [Pixel(True, CLR_RED),  Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED)],
    [Pixel(False),  Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(False)],
    [Pixel(False),  Pixel(False),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(False),   Pixel(False)],
    [Pixel(False),  Pixel(False),   Pixel(False),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(True, CLR_RED),   Pixel(False),   Pixel(False),   Pixel(False)],
]
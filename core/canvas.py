import os
import sys
import argparse
from RGBMatrixEmulator import (
    RGBMatrix,
    RGBMatrixOptions,
    graphics
)
from typing import Optional
from util.utils import FONT_PATH
from common.typing import (
    Color,
    Image
)

# Copied a lot from Samplebase.py

class Matrix(object):
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser()

        self._parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 64", default=32, type=int)
        self._parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=64, type=int)
        self._parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.", default=1, type=int)
        self._parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self._parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self._parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self._parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'regular-pi1', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self._parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
        self._parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
        self._parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
        self._parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=1, type=int)
        self._parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        self._parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB", type=str)
        self._parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self._parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1=AB-addressed panels; 2=row direct; 3=ABC-addressed panels; 4 = ABC Shift + DE direct", default=0, type=int, choices=[0,1,2,3,4])
        self._parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven... (Default: 0)", default=0, type=int)
        self._parser.add_argument("--led-panel-type", action="store", help="Needed to initialize special panels. Supported: 'FM6126A'", default="", type=str)
        self._parser.add_argument("--led-no-drop-privs", dest="drop_privileges", help="Don't drop privileges from 'root' after initializing the hardware.", action='store_false')
        self._parser.set_defaults(drop_privileges=True)
    
    def draw_border(
        self, 
        color: Color
    ) -> None:
        """
        draw_border Draws a one-pixel wide border

        This function draws a one-pixel wide border with a specific
        color.

        Arguments:
            color -- Color of the border (check ./images.py Color dataclass)
        """
        r, g, b = color.r, color.g, color.b
        for x in range(0, self.matrix.width-1):
            self.canvas.SetPixel(x, 0, r, g, b)
            self.canvas.SetPixel(x, self.matrix.height-1, r, g, b)

        for y in range(0, self.matrix.height):
            self.canvas.SetPixel(0, y, r, g, b)
            self.canvas.SetPixel(self.matrix.width-1, y, r, g, b)

    def draw_horizontal(
            self,
            y: int,
            color: Color,
            start: Optional[int] = None,
            stop: Optional[int] = None
        ) -> None:
        """
        draw_horizontal Draws a horizontal line

        This one draws a horizontal line along the whole x-axis
        on a given y position.

        You can also set the color by passing red, green and blue values.

        Arguments:
            y -- Y-Position

        Keyword Arguments:
            r -- Amount of Red      (default: {255})
            g -- Amount of Green    (default: {255})
            b -- Amount of Blue     (default: {255})
        """
        r, g, b = color.r, color.g, color.b
        start = start if start else 0
        stop = stop if stop else self.matrix.width
        
        for x in range(start, stop):
            self.canvas.SetPixel(x, y, r, g, b)
    
    def draw_vertical(
        self,
        x: int,
        color: Color,
        start: Optional[int] = None,
        stop: Optional[int] = None
    ) -> None:
        r, g, b = color.r, color.g, color.b
        start = start if start else 0
        stop = stop if stop else self.matrix.height
        
        for y in range(start, stop):
            self.canvas.SetPixel(x, y, r, g, b)
    
    def draw_box(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: Color
    ) -> None:
        r, g, b = color.r, color.g, color.b
        set_pixel = self.canvas.SetPixel
        for y in range(y1, y2):
            for x in range(x1, x2):
                set_pixel(x, y, r, g, b)

    def draw_text(
            self, 
            x: int, 
            y: int, 
            color: Color,
            text: str,
            char_width: int = 6,
            char_height: int = 9
        ) -> None:
        """
        draw_text Draws text onto the LED-Panel

        Arguments:
            x -- X-Position
            y -- Y-Position
            r -- Amount of Red
            g -- Amount of Green
            b -- Amount of Blue
            text -- Text displayed

        Keyword Arguments:
            char_width -- Width of each individual character (default: {6})
            char_height -- Height of each individual character. (default: {9})
        """
        font = graphics.Font()
        font.LoadFont(self.interpret_font_size(
            char_width, 
            char_height
        ))
        font_color = graphics.Color(color.r, color.g, color.b)
        graphics.DrawText(self.canvas, font, x, y, font_color, text)

    def draw_image(
        self, 
        image: Image, 
        start_x: int, 
        start_y: int
    ) -> None:
        """
        draw_image Draws an image onto the LED-Panel

        Arguments:
            image -- The image drawn onto the Canvas (check typing.py Image dataclass)
            start_x -- Anchor X-Position of image
            start_y -- Anchor Y-Position of image
        """
        set_pixel = self.canvas.SetPixel
        for y_pos in range(len(image)):
            line = image[y_pos]
            pixel_y = start_y + y_pos
            
            for x_pos in range(len(line)):
                pixel = line[x_pos]
                if not pixel.on:
                    continue
                
                pixel_x = start_x + x_pos
                c = pixel.color
                if c:
                    set_pixel(pixel_x, pixel_y, c.r, c.g, c.b)
                else:
                    continue
    
    def interpret_font_size(
            self, 
            char_width: int,
            char_height: int
        ) -> str:
        """
        interpret_font_size Interprets the font the LED-Panel is going to use

        This works by checking the character width and height and then
        looking for a font with the same character width and height

        Arguments:
            char_width -- Width of each character
            char_height -- Height of each character

        Raises:
            ValueError: If the given size doesn't exist it will throw an error.

        Returns:
            The path to a possible font
        """
        path = os.path.join(FONT_PATH, f"{char_width}x{char_height}.bdf")
        if os.path.exists(os.path.abspath(path)):
            return path
        else:
            raise ValueError(f"Font size does not exist in available fonts.\nPath: {os.path.abspath(path)}")
    
    def run(self) -> None:
        print("Running")
    
    def process(self) -> bool:
        self.args = self._parser.parse_args()
        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        # options.pixel_mapper_config = self.args.led_pixel_mapper
        # options.panel_type = self.args.led_panel_type
        
        if self.args.led_show_refresh:
            options.show_refresh_rate = 1
        
        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True
        # if not self.args.drop_privileges:
        #   options.drop_privileges=False
        
        self.matrix = RGBMatrix(options = options)
        self.canvas = self.matrix.CreateFrameCanvas()
        
        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True
from RGBMatrixEmulator.emulation.canvas import Canvas
from RGBMatrixEmulator import graphics
from typing import Optional
from core.visuals import (
    CLR_BRIGHTER_BLUE,
    CLR_RED
)
from common.typing import Color

class RainBar:
    def __init__(
            self, 
            canvas: Optional[Canvas],
            x_pos: int,
            y_pos: int,
            width: int,
            height: int,
            color: Color
        ) -> None:
        """
        __init__ Initializes a rain bar to roughly visualize
        the amount of rain coming down in the current hour

        Arguments:
            canvas -- The LED-Panel's canvas the bar will be drawn onto
            x_pos -- Anchor X-Positon
            y_pos -- Anchor Y-Position
            width -- Width of the bar
            height -- Height of the bar
            color -- Color of the outline of the bar
        """
        self.canvas = canvas
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
    
    @property
    def top_y(self) -> int:
        """
        top_y Returns the y position of the ceiling of the rain bar

        Returns:
            y-position as int
        """
        return self.y_pos
    
    @property
    def bottom_y(self) -> int:
        """
        bottom_y Returns y position of the bottom of the rain bar

        Returns:
            y-position as int
        """
        return self.y_pos + self.height
    
    @property
    def left_x(self) -> int:
        """
        left_x Returns the x-position of the left wall of the bar

        Returns:
            x-position as int
        """
        return self.x_pos
    
    @property
    def right_x(self) -> int:
        """
        right_x Returns the x-position of the right wall of the bar

        Returns:
            x-position as int
        """
        return self.x_pos + self.width
    
    @property
    def fill_height(self) -> int:
        """
        fill_height Returns the height of the content in the rain bar

        Returns:
            height as int (rows)
        """
        return self.height - 1

    def draw_outline(
            self, 
            canvas: Canvas
        ) -> None:
        """
        draw_outline Draws the outline of the rain bar

        Arguments:
            canvas -- The LED-Panel's canvas to draw on.
        """
        y = self.top_y
        y2 = self.bottom_y
        
        for x in range(self.left_x, self.right_x+1):
            canvas.SetPixel(x, y, self.color.r, self.color.g, self.color.b)
            canvas.SetPixel(x, y2, self.color.r, self.color.g, self.color.b)
        
        x = self.left_x
        x2 = self.right_x

        for y in range(self.top_y, self.bottom_y+1):
            canvas.SetPixel(x, y, self.color.r, self.color.g, self.color.b) 
            canvas.SetPixel(x2, y, self.color.r, self.color.g, self.color.b) 

    def return_color_gradient(
            self, 
            rows: int, 
            start_color: Color, 
            end_color: Color
        ) -> list[Color]:
        """
        return_color_gradient Builds a list of colors

        Arguments:
            rows -- Amount of colors between start and end of gradient
            start_color -- The color the gradient starts with
            end_color -- The color the gradient ends with

        Returns:
            A list of colors of the full gradient.
        """
        colors = []
        for iteration in range(self.fill_height):
            ratio = iteration / (self.fill_height)
            color = Color(
                r=int(start_color.r + (end_color.r - start_color.r) * ratio),
                g=int(start_color.g + (end_color.g - start_color.g) * ratio),
                b=int(start_color.b + (end_color.b - start_color.b) * ratio),
            )
            colors.append(color)
        return colors[0:rows]
    
    def fill_bar(
        self, 
        canvas: Canvas,
        precipitation: float
    ) -> None:
        """
        fill_bar Fills the bar with a given amount of precipitation

        Arguments:
            canvas -- The LED Panels' canvas.
            precipitation -- The amount of water raining from the sky in this current hour (in mm)
        """
        max_mm = 7
        if precipitation > max_mm:
            precipitation = max_mm

        mm_per_row = max_mm / self.fill_height
        rows = round(precipitation / mm_per_row)

        colors = self.return_color_gradient(
            rows=self.fill_height,
            start_color=CLR_BRIGHTER_BLUE,
            end_color=CLR_RED
        )

        for iteration in range(rows):
            y = self.bottom_y - 1 - iteration
            for x in range(self.left_x+1, self.right_x):
                color = colors[iteration]
                canvas.SetPixel(x, y, color.r, color.g, color.b)
    
    def add_text(
        self, 
        canvas: Canvas, 
        precipitation: float,
        font_path: str
    ) -> None:
        """
        add_text Adds the text showing how much rain is coming down in mm

        Arguments:
            canvas -- The LED-Panels' canvas
            precipitation -- The amount of water raining from the sky in the present hour
            font_path -- The path to the font the text will use
        """
        text = str(round(precipitation, 1))
        font = graphics.Font()
        font.LoadFont(font_path)
        font_color = graphics.Color(255, 255, 255)

        graphics.DrawText(
            canvas=canvas, 
            font=font,
            x = self.right_x + 2,
            y = round((self.top_y + self.bottom_y) / 2) + 3,    # middle of bar and then 3 pixels down because font height
            color = font_color,
            text = text
        )

    def draw_bar(
        self, 
        canvas: Optional[Canvas], 
        precipitation: float,
        font_path: str
    ) -> None:
        """
        draw_bar Draws the entire bar.

        For more information on how this works check
        the functions this method calls.

        Arguments:
            canvas -- The LED-Panels' canvas
            precipitation -- The amount of water raining from the sky in the present hour
            font_path -- The path to the font we'll use for the text

        Raises:
            TypeError: If you've never initialized a Canvas an error will be raised.
        """
        if not self.canvas:
            if not canvas:
                raise TypeError("No Canvas initialized!")
            else:
                canvas = canvas
        else:
            canvas = self.canvas

        self.draw_outline(canvas)
        self.fill_bar(canvas, precipitation)
        self.add_text(
            canvas=canvas,
            precipitation=precipitation,
            font_path=font_path)
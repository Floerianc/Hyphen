from RGBMatrixEmulator.emulation.canvas import Canvas
from RGBMatrixEmulator import graphics
from typing import List
from os import PathLike
from common.typing import Color

class PrecipitationForecastWidget:
    def __init__(
        self,
        canvas: Canvas,
        x_pos: int,
        y_pos: int,
        font: str | PathLike,
        font_color: Color,
        gap: int,
        precipitation_forecast: List[float]
    ) -> None:
        self.canvas = canvas
        self.x = x_pos
        self.y = y_pos
        
        self.font = font
        self.color = font_color
        self.gap = gap
        self.pf = precipitation_forecast
    
    # @property
    # def forecast(self) -> List[float]:
    #     return self.weather.precipitation_forecast(3)
    
    def render(self) -> None:
        font = graphics.Font()
        font.LoadFont(self.font)
        
        y = self.y
        for idx, precipitation in enumerate(self.pf):
            graphics.DrawText(
                self.canvas,
                font,
                self.x,
                y,
                graphics.Color(self.color.r, self.color.g, self.color.b),
                f"+{idx+1} {round(precipitation, 1)}mm"
            )
            y += 5 + self.gap

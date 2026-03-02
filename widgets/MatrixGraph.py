import math
from typing import (
    Optional,
    List,
    Union
)
from core import visuals
from core.canvas import Matrix
from common.typing import Color
from common.logger import log_event


class MatrixGraph:
    def __init__(
        self,
        canvas: Matrix,
        x: int,
        y: int,
        width: int,
        height: int,
        max_value: Optional[int],
        graph_color: Color,
        data: List[Union[int, float]]
    ) -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.color = graph_color
        self.data = data
    
    def _get_absolute_x(
        self,
        x: int
    ) -> int:
        return self.x + x
    
    def _get_absolute_y(
        self,
        y: int
    ) -> int:
        return self.y + y
    
    def _draw_base(self) -> None:
        x_pos_ends = (self._get_absolute_x(0), self._get_absolute_x(self.width-1))
        y_pos_ends = (self._get_absolute_y(0), self._get_absolute_y(self.height-1))
        self.canvas.draw_horizontal(
            y=y_pos_ends[1],
            color=visuals.CLR_WHITE,
            start=x_pos_ends[0],
            stop=x_pos_ends[1]
        )
        self.canvas.draw_vertical(
            x=x_pos_ends[0],
            color=visuals.CLR_WHITE,
            start=y_pos_ends[0],
            stop=y_pos_ends[1]
        )
    
    def _get_max_limit(self) -> int:
        return math.ceil(max(self.data))
    
    def _get_min_limit(self) -> int:
        return math.floor(min(self.data))
    
    def _draw_limits(self) -> None:
        minimum = self._get_min_limit()
        maximum = self._get_max_limit()
        gap = 1
        char_width = 4
        
        min_x = self._get_absolute_x(0 - (gap + (char_width * len(str(minimum)))))
        max_x = self._get_absolute_x(0 - (gap + (char_width * len(str(maximum)))))
        min_y = self._get_absolute_y(self.height)
        max_y = self._get_absolute_y(0 + 5)
        
        self.canvas.draw_text(
            x=(min_x - 4) if minimum < 0 else min_x,  # if there's a "-", then you need more space. otherwise, it will clip into the base
            y=min_y,
            color=Color(255, 255, 255),
            text=str(minimum),
            char_width=4,
            char_height=6
        )
        self.canvas.draw_text(
            x=(max_x - 4) if maximum < 0 else max_x,
            y=max_y,
            color=Color(255, 255, 255),
            text=str(maximum),
            char_width=4,
            char_height=6
        )
    
    def _draw_values(self) -> None:
        start_x = self._get_absolute_x(2)
        start_y = self._get_absolute_y(self.height - 1)  # bottom
        end_x   = self._get_absolute_x(self.width)
        end_y   = self._get_absolute_y(0)                # top

        chart_width  = end_x - start_x
        chart_height = start_y - end_y

        gap = 1
        bar_width = max(
            1,
            math.floor((chart_width - (gap * len(self.data))) / len(self.data))
        )

        # --- VALUE SPACE ---
        min_val = self._get_min_limit()
        max_val = self._get_max_limit()

        # shift everything so min_val == 0
        offset = -min_val if min_val < 0 else 0
        adj_max = max_val + offset

        if adj_max == 0:
            adj_max = 1

        px_per_val = chart_height / adj_max
        
        for idx, value in enumerate(self.data):
            x1 = start_x + (bar_width + gap) * idx
            x2 = x1 + bar_width
            
            bar_height = int((value + offset) * px_per_val)
            
            y1 = start_y - bar_height
            y2 = start_y
            
            self.canvas.draw_box(
                x1=x1,
                x2=x2,
                y1=min(y1, y2),
                y2=max(y1, y2),
                color=self.color
            )
    
    def render(self) -> None:
        if self.data:
            self._draw_base()
            self._draw_limits()
            self._draw_values()
        else:
            log_event(
                "No data for the MatrixGraph."
                "Perhaps wrong list, no API response or something else lol"
            )
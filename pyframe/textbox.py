from textwrap import wrap
from time import sleep
from typing import Optional
from pyframe.border.border_types import Borders
from pyframe.frame import Frame, Title, Cell
from pyframe.grid import Grid
from pyframe.border.border_type import BorderType, Thickness
from pyframe.colors import Colors, Color
from pyframe.types_ import Alignment, TitleSide, VerticalAlignment

from pyframe.border.border_type import Thickness

from math import ceil
from pyframe.vector import VectorYX
from textwrap import wrap


class Textbox(Frame):
    def __init__(
        self,
        text: str,
        width: int,
        lines: Optional[int] = None,
        horizontal_padding: int = 1,
        text_alignment: Alignment = Alignment.LEFT,
        vertical_text_alignment: VerticalAlignment = VerticalAlignment.DOWN,
        border_type: BorderType = Borders.Thin.ROUND,
    ):
        """Wraps text to a frame"""
        padding = 2 + 2
        wrapped_lines = wrap(text, width - 2 - horizontal_padding * 2)

        amount_of_text_lines = len(wrapped_lines)
        total_lines = lines or amount_of_text_lines
        blank_lines = total_lines - amount_of_text_lines

        if vertical_text_alignment == VerticalAlignment.DOWN:
            top = [" "] * blank_lines
            bottom = []
        elif vertical_text_alignment == VerticalAlignment.UP:
            top = []
            bottom = [" "] * blank_lines
        else:
            top = [" "] * (blank_lines // 2)
            bottom = [" "] * ((blank_lines - 1) // 2 + 1)

        wrapped_lines = top + wrapped_lines + bottom

        aligned_lines = [
            text_alignment.align(line, width - padding // 2 - 1)
            for line in wrapped_lines
        ]

        formatted_text = Grid(
            [
                ([Cell(" ")] if row[0] != " " else []) + [Cell(cell) for cell in row]
                for row in aligned_lines
            ],
            text_alignment,
        )

        super().__init__(formatted_text, border_type)

        self.text = text

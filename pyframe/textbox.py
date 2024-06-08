from asyncio import sleep
from textwrap import wrap
from typing import Optional

from pyframe.screen.colors import Color, Colors
from pyframe.screen.frames.border.border_type import Borders, BorderType
from pyframe.screen.frames.frame import Frame, Title
from pyframe.screen.grid.matrix import Cell, Grid
from pyframe.screen.grid.point import Coord, Size
from pyframe.screen.web.event import _animation
from pyframe.screen.web.input import keys_pressed
from pyframe.types_ import Alignment


# TODO Different Words different colors
class TextBox(Frame):
    """A outlined box that can display text in the terminal"""

    def __init__(
        self,
        text: str,
        size: Size = Size(2, 70),
        author: Optional[str] = None,
        text_alignment: Alignment = Alignment.LEFT,
        skip_char: str = "⏷",
        border_type: BorderType = Borders.THIN,
        default_delay: float = 0.03,
        default_sped_up_delay: float = 0.01,
        delays: Optional[dict[str, float]] = None,
        sped_up_delays: Optional[dict[str, float]] = None,
        speed_key: str = " ",
        block_key: str = " ",
    ) -> None:
        super().__init__(Cell.from_size(size), border_type)

        if author:
            self.add_title(Title(author))

        self.text = text

        self.current_text = ""

        self.text_alignment = text_alignment
        self.author = author

        self.border_type = border_type

        self.wrap_width = self.size.inner.width - 6  # | x ⏷ |
        self.text_width = self.size.inner.width - 3  # | x |

        self.block_char = skip_char
        self.speed_key = speed_key
        self.block = False
        self.default_delay = default_delay
        self.default_sped_up_delay = default_sped_up_delay

        if delays is None:
            self.delays = {
                ".": 1.00,
                "?": 1.00,
                ";": 0.75,
                ",": 0.50,
                ":": 0.50,
            }
        else:
            self.delays = delays

        if sped_up_delays is None:
            self.sped_up_delays = {
                ".": 0.50,
                "?": 0.50,
                ";": 0.35,
                ",": 0.25,
                ":": 0.25,
            }
        else:
            self.sped_up_delays = sped_up_delays

        self.block_key = block_key
        self.completed = False

        def gen():
            lines = wrap(self.text, self.wrap_width)
            lines = tuple(line.split() for line in lines)

            for index, line in enumerate(lines):
                for index2, word in enumerate(line):
                    for index3, char in enumerate(word + " "):
                        if (
                            index2 == len(line) - 1
                            and index3 == len(word) - 1
                            and (
                                (index - 1) % self.size.inner.height == 0
                                or index == len(lines) - 1
                            )
                        ):
                            self.block = True

                        yield char

        self.characters = gen()

    @_animation(0.2)
    def speech(self):
        if self.block:
            while " " not in keys_pressed:
                return
            self.block = False

        char = next(self.characters)
        self.current_text += char

        lines = wrap(self.current_text, self.wrap_width)[-self.size.inner.height :]

        # TODO make as Cells so dont have to convert
        string = ""
        for i in range(self.size.inner.height):
            line = None
            if i <= len(lines) - 1:
                line = ""
                match self.text_alignment:
                    case Alignment.CENTER:
                        line = f" {lines[i]:^{self.text_width}} \n"
                    case Alignment.RIGHT:
                        line = f" {lines[i]:>{self.text_width}} \n"
                    case Alignment.LEFT:
                        line = f" {lines[i]:<{self.text_width}} \n"
                if self.block and i == len(lines) - 1:
                    line = line[:-3] + self.block_char + line[-2:]
            else:
                line = f' {" ":<{self.text_width}} \n'
            string += line

        # TODO faster alg
        new = Grid(string[:-1])
        import numpy as np

        def get_coordinates(start_point, end_point):
            return [
                Coord(y, x)
                for x in range(start_point.x, end_point.x + 1)
                for y in range(start_point.y, end_point.y + 1)
            ]

        for coord in get_coordinates(Coord(1, 1), new.size):
            self[coord].update(new[coord - Coord(1, 1)])

        self[(-2, -4)].emoji = True

        if " " in keys_pressed:
            speed = self.sped_up_delays.get(char, self.default_sped_up_delay)
        else:
            speed = self.delays.get(char, self.default_delay)
        return speed

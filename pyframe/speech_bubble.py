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
from pyframe.textbox import Textbox


class SpeechBubble(Textbox):
    def __init__(
        self,
        message: str,
        height: int,
        width: int,
        speaker: Optional[str] = None,
        text_alignment: Alignment = Alignment.LEFT,
        block_char: str = "⏷",
        border_type: BorderType = Borders.Thin.ROUND,
        # default_delay: float = 0.03,
        # default_sped_up_delay: float = 0.01,
        # delays: dict[str, float] = ...,
        # sped_up_delays: dict[str, float] = ...,
        # speed_key: str = " ",
        # block_key: str = " ",
        block: bool = True,
    ) -> None:
        
        # self.text = text
        # self.size = size

        # self.text_alignment = text_alignment
        # self.author = author
        # self.author_color = author_color
        # self.border_color = border_color
        # self.text_color = text_color
        # self.border_type = border_type

        # self.wrap_width = self.size.inner.width - 6  # | x ⏷ |
        # self.text_width = self.size.inner.width - 3  # | x |

        # self.block_char = block_char
        # self.speed_key = speed_key
        # self.block = False
        # self.default_delay = default_delay
        # self.default_sped_up_delay = default_sped_up_delay

        # self.delays = delays
        # if self.delays is ...:
        #     self.delays = {
        #         ".": 1.00,
        #         "?": 1.00,
        #         ";": 0.75,
        #         ",": 0.50,
        #         ":": 0.50,
        #     }

        # self.sped_up_delays = sped_up_delays
        # if self.sped_up_delays is ...:
        #     self.sped_up_delays = {
        #         ".": 0.50,
        #         "?": 0.50,
        #         ";": 0.35,
        #         ",": 0.25,
        #         ":": 0.25,
        #     }
        # self.block_key = block_key

        def speech():
            self.clear()
            lines = wrap(text, self.wrap_width)
            lines = [line.split() for line in lines]

            for index, line in enumerate(lines):
                for word in line:
                    if self.block:
                        self.refresh()

                        wait(block_key)
                        self.block = False

                    for char in word:
                        self.add(char)

                        self.refresh()

                        if is_pressed(self.speed_key):
                            sleep(
                                self.sped_up_delays.get(
                                    char, self.default_sped_up_delay
                                )
                            )
                        else:
                            sleep(self.delays.get(char, self.default_delay))

                    self.add(" ")

                #      If theres fully new display             OR    the last iteration   AND block is True then...
                if (
                    (index - 1) % self.size.inner.height == 0 or index == len(lines) - 1
                ) and block:
                    self.block = True

            return True

        self.event = speech

    def __str__(self) -> str:
        lines = wrap(self.text, self.wrap_width)[
            -self.size.inner.height :
        ]  # Last lines

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

        self.textbox = Frame.map(
            string,
            self.author,
            border_color=self.border_color,
            title_color=self.author_color,
            border_type=self.border_type,
            base_color=self.text_color,
        )

        return str(self.textbox)

    def add(self, text: str) -> None:
        """Adds text to the TextBox."""
        self.text += text

    def clear(self) -> None:
        """Clears the TextBox's text"""
        self.text = ""

    def refresh(self) -> None:
        Screen.write(str(self))

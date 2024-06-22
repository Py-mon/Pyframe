from copy import copy
from dataclasses import dataclass
from typing import Self

from pyframe.grid import Cell, Junction
from pyframe.types_ import Direction, JunctionDict, Thickness


@dataclass
class BorderType:
    top_right: JunctionDict | str
    top_left: JunctionDict | str
    bottom_right: JunctionDict | str
    bottom_left: JunctionDict | str

    top_horizontal: JunctionDict | str
    left_vertical: JunctionDict | str
    bottom_horizontal: JunctionDict | str
    right_vertical: JunctionDict | str

    # def __repr__(self) -> str:
    #     return repr(Border(self, 3, 5))

    @classmethod
    def thickness(
        cls, top: Thickness, bottom: Thickness, left: Thickness, right: Thickness
    ):
        return cls(
            top_right={Direction.DOWN: left, Direction.RIGHT: top},
            top_left={Direction.DOWN: right, Direction.LEFT: top},
            bottom_right={Direction.UP: left, Direction.RIGHT: bottom},
            bottom_left={Direction.UP: right, Direction.LEFT: bottom},
            top_horizontal={Direction.LEFT: top, Direction.RIGHT: top},
            left_vertical={Direction.UP: left, Direction.DOWN: left},
            bottom_horizontal={Direction.LEFT: bottom, Direction.RIGHT: bottom},
            right_vertical={Direction.UP: right, Direction.DOWN: right},
        )

    @classmethod
    def uniform_thickness(
        cls,
        thickness: Thickness,
    ):
        return cls(
            top_right={Direction.DOWN: thickness, Direction.RIGHT: thickness},
            top_left={Direction.DOWN: thickness, Direction.LEFT: thickness},
            bottom_right={Direction.UP: thickness, Direction.RIGHT: thickness},
            bottom_left={Direction.UP: thickness, Direction.LEFT: thickness},
            top_horizontal={Direction.LEFT: thickness, Direction.RIGHT: thickness},
            left_vertical={Direction.UP: thickness, Direction.DOWN: thickness},
            bottom_horizontal={Direction.LEFT: thickness, Direction.RIGHT: thickness},
            right_vertical={Direction.UP: thickness, Direction.DOWN: thickness},
        )


class Border:
    def __init__(self, border_type: BorderType, height: int, width: int):
        def create_instance(junction):
            if isinstance(junction, dict):
                return Junction(junction)
            if len(junction) > 1:
                return [Cell(x) for x in junction]
            return Cell(junction)

        self.top_right = create_instance(border_type.top_right)
        self.top_left = create_instance(border_type.top_left)
        self.bottom_right = create_instance(border_type.bottom_right)
        self.bottom_left = create_instance(border_type.bottom_left)

        self.top_horizontal = create_instance(border_type.top_horizontal)
        self.left_vertical = create_instance(border_type.left_vertical)
        self.bottom_horizontal = create_instance(border_type.bottom_horizontal)
        self.right_vertical = create_instance(border_type.right_vertical)

        def pattern(
            junction,
            width,
        ):
            if isinstance(junction, list):
                return [junction[i % len(junction)] for i in range(width)]
            return junction * width

        self.top_row = [
            self.top_right,
            *pattern(self.top_horizontal, width),
            self.top_left,
        ]
        self.left_column = self.left_vertical * height
        self.right_column = self.right_vertical * height

        self.bottom_row = [
            self.bottom_right,
            *pattern(self.bottom_horizontal, width),
            self.bottom_left,
        ]

    # def __repr__(self) -> str:
    #     return (
    #         f"{self.top_right}{''.join([str(cell) for cell in self.mult(self.top_horizontal, 4)])}{self.top_left}\n"
    #         f"{self.left_vertical}    {self.right_vertical}\n"
    #         f"{self.bottom_right}{str(self.bottom_horizontal) * 4}{self.bottom_left}\n"
    #     )


class BorderTypes:
    """
    ```
    Thin:
        ╭───╮
        │   │
        ╰───╯
    Thick:
        ┏━━━┓
        ┃   ┃
        ┗━━━┛
    Double:
        ╔═══╗
        ║   ║
        ╚═══╝
    """

    THIN = BorderType.uniform_thickness(Thickness.THIN)
    THICK = BorderType.uniform_thickness(Thickness.THICK)
    DOUBLE = BorderType.uniform_thickness(Thickness.DOUBLE)

    #

    CASTLE = copy(THIN)
    CASTLE.top_horizontal = "─⍽─"

    class Classic:
        PLUS = BorderType(
            top_right="+",
            top_left="+",
            bottom_right="+",
            bottom_left="+",
            top_horizontal="-",
            left_vertical="|",
            bottom_horizontal="-",
            right_vertical="|",
        )
        # EQUAL_SIGN = BorderType(
        #     top_right=PLUS.top_right,
        #     top_left=PLUS.top_left,
        #     bottom_right=PLUS.bottom_right,
        #     bottom_left=PLUS.bottom_left,
        #     top_horizontal="=",
        #     left_vertical=PLUS.left_vertical,
        #     bottom_horizontal="=",
        #     right_vertical=PLUS.right_vertical,
        # )
        UNDERSCORE = BorderType(
            top_right=" ",
            top_left=" ",
            bottom_right="|",
            bottom_left="|",
            top_horizontal="_",
            left_vertical=PLUS.left_vertical,
            bottom_horizontal="_",
            right_vertical=PLUS.right_vertical,
        )


# TODO vector2d, ascii art, more borders
# ― ⍽ ⎸ ⎹ ␣ ─ ━ │ ┃
# ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋╌ ╍ ╎ ╏


# DOUBLE and THICK aren't compatible
# print(
#     BorderType.thickness(
#         Thickness.DOUBLE, Thickness.DOUBLE, Thickness.DOUBLE, Thickness.THIN
#     )
# )

# print(BorderTypes.CLASSIC)

# print(
#     BorderType.thickness(
#         Thickness.THIN, Thickness.THIN, Thickness.DOUBLE, Thickness.THICK
#     )
# )

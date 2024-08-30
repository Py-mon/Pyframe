from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Optional, Self

from pyframe.border.border_type import BorderPattern, BorderType
from pyframe.border.junction import Junction
from pyframe.grid import Cell
from pyframe.types_ import Direction, JunctionDict, Thickness


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

    THICK = BorderType.thickness(thickness=Thickness.THICK)
    DOUBLE = BorderType.thickness(thickness=Thickness.DOUBLE)

    class Thin:
        ROUND = BorderType.thickness(thickness=Thickness.THIN, corner_style="round")
        SHARP = BorderType.thickness(thickness=Thickness.THIN, corner_style="sharp")

        Dashed: "type[_Dashed]"
        Castle: "type[_Castle]"

    class OverlapClassic:
        DASHED = BorderType(
            top_right="+",
            top_left="+",
            bottom_right="+",
            bottom_left="+",
            top_horizontal="-",
            left_vertical="|",
            bottom_horizontal="-",
            right_vertical="|",
            title_left="-",
            title_right="-",
        )
        DOUBLE = BorderType(
            top_right="+",
            top_left="+",
            bottom_right="+",
            bottom_left="+",
            top_horizontal="=",
            left_vertical="|",
            bottom_horizontal="=",
            right_vertical="|",
            title_left="=",
            title_right="=",
        )
        UNDERSCORE = BorderType(
            top_right=" ",
            top_left=" ",
            bottom_right="|",
            bottom_left="|",
            top_horizontal="_",
            left_vertical="|",
            bottom_horizontal="_",
            right_vertical="|",
            title_left="_",
            title_right="_",
        )
        OVERSCORE = BorderType(
            top_right="|",
            top_left="|",
            bottom_right=" ",
            bottom_left=" ",
            top_horizontal="‾",
            left_vertical="|",
            bottom_horizontal="‾",
            right_vertical="|",
            title_left="‾",
            title_right="‾",
        )

    ThickDashed: "type[_ThickDashed]"


def get_dashed_from(parent) -> tuple[BorderType, BorderType, BorderType]:
    triple = deepcopy(parent)
    triple.set_vertical_style("triple_dash")
    triple.set_horizontal_style("triple_dash")

    quad = deepcopy(parent)
    quad.set_vertical_style("quad_dash")
    quad.set_horizontal_style("quad_dash")

    duo = deepcopy(parent)
    duo.set_vertical_style("duo_dash")
    duo.set_horizontal_style("duo_dash")

    return triple, quad, duo


class _Castle:
    ROUND = copy(BorderTypes.Thin.ROUND)
    ROUND.top_horizontal = BorderPattern.from_string("─⍽")


BorderTypes.Thin.Castle = _Castle


class _Dashed:
    class Round:
        TRIPLE, QUAD, DUO = get_dashed_from(BorderTypes.Thin.ROUND)

    class Sharp:
        TRIPLE, QUAD, DUO = get_dashed_from(BorderTypes.Thin.SHARP)


BorderTypes.Thin.Dashed = _Dashed


class _ThickDashed:
    TRIPLE, QUAD, DUO = get_dashed_from(BorderTypes.THICK)


BorderTypes.Thin = BorderTypes.Thin
BorderTypes.ThickDashed = _ThickDashed

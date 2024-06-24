from copy import copy
from dataclasses import dataclass
from typing import Optional, Self

from pyframe.grid import Cell, Junction
from pyframe.types_ import Direction, JunctionDict, Thickness

StyledJunction = tuple[JunctionDict, str]


class Pattern:
    def __init__(self, *pattern: StyledJunction) -> None:
        self.pattern = pattern

    def __mul__(self, times):
        return [Junction(*self.pattern[i % len(self.pattern)]) for i in range(times)]


BorderJunction = StyledJunction | str | Pattern


@dataclass
class BorderType:
    top_right: BorderJunction
    top_left: BorderJunction
    bottom_right: BorderJunction
    bottom_left: BorderJunction

    top_horizontal: BorderJunction
    left_vertical: BorderJunction
    bottom_horizontal: BorderJunction
    right_vertical: BorderJunction

    @classmethod
    def thickness(
        cls,
        top: Optional[Thickness] = None,
        bottom: Optional[Thickness] = None,
        left: Optional[Thickness] = None,
        right: Optional[Thickness] = None,
        top_style: str = "default",
        left_style: str = "default",
        bottom_style: str = "default",
        right_style: str = "default",
        top_right_style: str = "default",
        top_left_style: str = "default",
        bottom_right_style: str = "default",
        bottom_left_style: str = "default",
        *,
        thickness: Optional[Thickness] = None,
        style: Optional[str] = None,
        corner_style: Optional[str] = None,
    ):
        if style:
            if top_style == "default":
                top_style = style
            if bottom_style == "default":
                bottom_style = style
            if left_style == "default":
                left_style = style
            if right_style == "default":
                right_style = style
        if corner_style:
            if top_right_style == "default":
                top_right_style = corner_style
            if bottom_left_style == "default":
                bottom_left_style = corner_style
            if top_left_style == "default":
                top_left_style = corner_style
            if bottom_right_style == "default":
                bottom_right_style = corner_style

        if thickness:
            top = thickness
            left = thickness
            right = thickness
            bottom = thickness
        elif top == None or left == None or right == None or bottom == None:
            raise

        return cls(
            top_right=(
                {Direction.DOWN: left, Direction.RIGHT: top},
                top_right_style,
            ),  # make junction here? <--
            top_left=({Direction.DOWN: right, Direction.LEFT: top}, top_left_style),
            bottom_right=(
                {Direction.UP: left, Direction.RIGHT: bottom},
                bottom_right_style,
            ),
            bottom_left=(
                {Direction.UP: right, Direction.LEFT: bottom},
                bottom_left_style,
            ),
            top_horizontal=(
                {Direction.LEFT: top, Direction.RIGHT: top},
                top_style,
            ),  # convert tuple to class
            left_vertical=({Direction.UP: left, Direction.DOWN: left}, left_style),
            bottom_horizontal=(
                {Direction.LEFT: bottom, Direction.RIGHT: bottom},
                bottom_style,
            ),
            right_vertical=({Direction.UP: right, Direction.DOWN: right}, right_style),
        )

    def set_vertical_style(self, vertical: str):
        if isinstance(self.left_vertical, tuple):
            self.left_vertical = (self.left_vertical[0], vertical)
        if isinstance(self.right_vertical, tuple):
            self.right_vertical = (self.right_vertical[0], vertical)

    def set_horizontal(self, horizontal: BorderJunction):
        self.left_horizontal = horizontal
        self.right_horizontal = horizontal

    def __repr__(self) -> str:
        return (
            f"{self.top_right}{str(self.top_horizontal)}{self.top_left}\n"
            f"{self.left_vertical}    {self.right_vertical}\n"
            f"{self.bottom_right}{str(self.bottom_horizontal)}{self.bottom_left}\n"
        )


class Border:
    def __init__(self, border_type: BorderType):
        def create_instance(junction):
            if isinstance(junction, tuple):
                junction, style = junction
                return Junction(junction, style)

            elif isinstance(junction, Pattern):
                return junction

            return Cell(junction)

        self.top_right = create_instance(border_type.top_right)
        self.top_left = create_instance(border_type.top_left)
        self.bottom_right = create_instance(border_type.bottom_right)
        self.bottom_left = create_instance(border_type.bottom_left)

        self.top_horizontal = create_instance(border_type.top_horizontal)
        self.left_vertical = create_instance(border_type.left_vertical)
        self.bottom_horizontal = create_instance(border_type.bottom_horizontal)
        self.right_vertical = create_instance(border_type.right_vertical)


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

    # TRIPLE_DASHED = copy(THIN)
    # TRIPLE_DASHED.set_horizontal("┄")
    # TRIPLE_DASHED.set_vertical("┆")

    # QUAD_DASHED = copy(THIN)
    # QUAD_DASHED.set_horizontal("┈")
    # QUAD_DASHED.set_vertical("┊")

    # DUO_DASHED = copy(THIN)
    # DUO_DASHED.set_horizontal("╌")
    # DUO_DASHED.set_vertical("╎")

    # THICK_TRIPLE_DASHED = copy(THICK)
    # THICK_TRIPLE_DASHED.set_horizontal("┅")
    # THICK_TRIPLE_DASHED.set_vertical("┇")

    # THICK_QUAD_DASHED = copy(THICK)
    # THICK_QUAD_DASHED.set_horizontal("┉")
    # THICK_QUAD_DASHED.set_vertical("┋")

    # THICK_DUO_DASHED = copy(THICK)
    # THICK_DUO_DASHED.set_horizontal("╍")
    # THICK_DUO_DASHED.set_vertical("╏")

    # CASTLE = copy(THIN)
    # CASTLE.top_horizontal = Pattern(
    #     ({Direction.LEFT: Thickness.THIN, Direction.RIGHT: Thickness.THIN}, "default"),
    #     ({Direction.LEFT: Thickness.THIN, Direction.RIGHT: Thickness.THIN}, "dip_down"),
    # )
    # CASTLE.top_horizontal = Pattern("─", "⍽")

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

    Thin: "type[_Thin]"
    Thick: "type[_Thick]"


class _Thin:
    ROUND = BorderType.thickness(thickness=Thickness.THIN, corner_style="round")
    SHARP = BorderType.thickness(thickness=Thickness.THIN, corner_style="sharp")

    Round: "type[_Round]"


class _Round:
    TRIPLE_DASHED = copy(_Thin.ROUND)
    # TRIPLE_DASHED.set_horizontal("┄")
    # TRIPLE_DASHED.set_vertical("┆")

    # QUAD_DASHED = copy(THIN)
    # QUAD_DASHED.set_horizontal("┈")
    # QUAD_DASHED.set_vertical("┊")

    # DUO_DASHED = copy(THIN)
    # DUO_DASHED.set_horizontal("╌")
    # DUO_DASHED.set_vertical("╎")


_Thin.Round = _Round


class _Thick:
    THICK = BorderType.thickness(thickness=Thickness.THICK)


BorderTypes.Thin = _Thin
BorderTypes.Thick = _Thick

print(BorderTypes.Thin.ROUND)

print(BorderTypes.Thin.Round.TRIPLE_DASHED)
# print(BorderTypes.THIN)
# ↕xx
# xxx

# TODO vector2d, ascii art, more borders
# ― ⍽ ⎸ ⎹ ␣ ─ ━ │ ┃
# ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋╌ ╍ ╎ ╏
# ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↚ ↛ ↜ ↝ ↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧ ↨ ↩ ↪ ↫ ↬ ↭ ↮ ↯ ↰ ↱ ↲ ↳ ↴ ↵ ↶ ↷ ↸ ↹ ↺ ↻ ⇄ ⇅ ⇆ ⇇ ⇈ ⇉ ⇊ ⇍ ⇎ ⇏ ⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ⇖ ⇗ ⇘ ⇙ ⇚ ⇛ ⇜ ⇝ ⇞ ⇟ ⇠ ⇡ ⇢ ⇣ ⇤ ⇥ ⇦ ⇧ ⇨ ⇩ ⇪
# ☐ ☑ ☒ ⫍ ⫎ ⮹ ⮽ ⺆ ⼌ ⼐ ⼕
# ↼ ↽ ↾ ↿ ⇀ ⇁ ⇂ ⇃ ⇋ ⇌
# ╱ ╲ ╳

# DOUBLE and THICK aren't compatible
# THIN only has rounded corners

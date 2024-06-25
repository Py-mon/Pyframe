from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Optional, Self

from pyframe.border.junction import Junction
from pyframe.grid import Cell
from pyframe.types_ import Direction, JunctionDict, Thickness

StyledJunction = tuple[JunctionDict, str]


class Pattern:
    def __init__(self, *pattern: Junction) -> None:
        self.pattern = pattern

    def __mul__(self, times):
        return [copy(self.pattern[i % len(self.pattern)]) for i in range(times)]

    @classmethod
    def from_string(cls, string: str):
        return cls(*[Junction.from_string(junction) for junction in string])


BorderJunction = Junction | str | Pattern


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
            top_right=Junction(
                {Direction.DOWN: left, Direction.RIGHT: top},
                top_right_style,
            ),
            top_left=Junction(
                {Direction.DOWN: right, Direction.LEFT: top}, top_left_style
            ),
            bottom_right=Junction(
                {Direction.UP: left, Direction.RIGHT: bottom},
                bottom_right_style,
            ),
            bottom_left=Junction(
                {Direction.UP: right, Direction.LEFT: bottom},
                bottom_left_style,
            ),
            top_horizontal=Junction(
                {Direction.LEFT: top, Direction.RIGHT: top},
                top_style,
            ),
            left_vertical=Junction(
                {Direction.UP: left, Direction.DOWN: left}, left_style
            ),
            bottom_horizontal=Junction(
                {Direction.LEFT: bottom, Direction.RIGHT: bottom},
                bottom_style,
            ),
            right_vertical=Junction(
                {Direction.UP: right, Direction.DOWN: right}, right_style
            ),
        )

    def set_vertical_style(self, vertical: str):
        if isinstance(self.left_vertical, Junction):
            self.left_vertical.style = vertical
        if isinstance(self.right_vertical, Junction):
            self.right_vertical.style = vertical

    def set_horizontal_style(self, horizontal: str):
        if isinstance(self.top_horizontal, Junction):
            self.top_horizontal.style = horizontal
        if isinstance(self.bottom_horizontal, Junction):
            self.bottom_horizontal.style = horizontal

    def __repr__(self) -> str:
        return (
            f"{self.top_right}{str(self.top_horizontal)}{self.top_left}\n"
            f"{self.left_vertical}    {self.right_vertical}\n"
            f"{self.bottom_right}{str(self.bottom_horizontal)}{self.bottom_left}\n"
        )


class Border:
    def __init__(self, border_type: BorderType):
        def create_instance(junction):
            if isinstance(junction, Pattern):
                return junction
            elif isinstance(junction, Junction):
                return copy(junction)

            return Cell(junction)

        self.top_right = create_instance(border_type.top_right)
        self.top_left = create_instance(border_type.top_left)
        self.bottom_right = create_instance(border_type.bottom_right)
        self.bottom_left = create_instance(border_type.bottom_left)

        self.top_horizontal = create_instance(border_type.top_horizontal)
        self.left_vertical = create_instance(border_type.left_vertical)
        self.bottom_horizontal = create_instance(border_type.bottom_horizontal)
        self.right_vertical = create_instance(border_type.right_vertical)


# TODO vector2d, ascii art, more borders
# ― ⍽ ⎸ ⎹ ␣ ─ ━ │ ┃
# ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋╌ ╍ ╎ ╏
# ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↚ ↛ ↜ ↝ ↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧ ↨ ↩ ↪ ↫ ↬ ↭ ↮ ↯ ↰ ↱ ↲ ↳ ↴ ↵ ↶ ↷ ↸ ↹ ↺ ↻ ⇄ ⇅ ⇆ ⇇ ⇈ ⇉ ⇊ ⇍ ⇎ ⇏ ⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ⇖ ⇗ ⇘ ⇙ ⇚ ⇛ ⇜ ⇝ ⇞ ⇟ ⇠ ⇡ ⇢ ⇣ ⇤ ⇥ ⇦ ⇧ ⇨ ⇩ ⇪
# ☐ ☑ ☒ ⫍ ⫎ ⮹ ⮽ ⺆ ⼌ ⼐ ⼕
# ↼ ↽ ↾ ↿ ⇀ ⇁ ⇂ ⇃ ⇋ ⇌
# ╱ ╲ ╳

# DOUBLE and THICK aren't compatible
# THIN only has rounded corners

from copy import copy
from dataclasses import dataclass, field
from typing import Optional

from pyframe.border.junction import Junction
from pyframe.grid import Cell
from pyframe.types_ import Direction, Thickness


class BorderPattern:
    """A pattern of Junctions for a side of a border.

    ```
    >>> BorderPattern.from_string('-+') * 5
    "-+-+-'
    ```
    """

    def __init__(self, *pattern: Junction | Cell) -> None:
        self.pattern = pattern

    def __mul__(self, times):
        return [copy(self.pattern[i % len(self.pattern)]) for i in range(times)]

    @classmethod
    def from_string(cls, string: str):
        return cls(*[Junction.from_string(junction) for junction in string])


BorderJunctions = Junction | str | BorderPattern


@dataclass
class BorderType:
    """Stores the styles and thicknesses of borders used in `Frames`.

    If an attribute is a string, it no longer becomes a Junction type and overrides other borders.

    Note: `DOUBLE` and `THICK` aren't compatible thicknesses due to box-drawing character limitations.
    """

    top_right: BorderJunctions
    top_left: BorderJunctions
    bottom_right: BorderJunctions
    bottom_left: BorderJunctions

    top_horizontal: BorderJunctions
    left_vertical: BorderJunctions
    bottom_horizontal: BorderJunctions
    right_vertical: BorderJunctions

    title_left: Optional[str]
    title_right: Optional[str]

    @classmethod
    def thickness(
        cls,
        top: Optional[Thickness] = None,
        bottom: Optional[Thickness] = None,
        left: Optional[Thickness] = None,
        right: Optional[Thickness] = None,
        *,
        top_style: str = "default",
        left_style: str = "default",
        bottom_style: str = "default",
        right_style: str = "default",
        top_right_style: str = "default",
        top_left_style: str = "default",
        bottom_right_style: str = "default",
        bottom_left_style: str = "default",
        thickness: Optional[Thickness] = None,
        style: Optional[str] = None,
        corner_style: Optional[str] = None,
        title_left: Optional[str] = None,
        title_right: Optional[str] = None,
    ):
        """
        #### Thickness (cannot be None if `thickness` argument is None)
        - `top` -> the thickness of the top of the border
        - `bottom` -> the thickness of the bottom of the border
        - `left` -> the thickness of the left side of the border
        - `right` -> the thickness of the right side of the border

        - `thickness` overrides all of the arguments above that are `None`.

        #### Style
        - `top_style` -> the style of the top of the border
        - `bottom_style` -> the style of the bottom of the border
        - `left_style` -> the style of the left side of the border
        - `right_style` -> the style of the right side of the border

        - `style` overrides all of the arguments above that are `None`.

        #### Corner Style
        - `top_right_style` -> the style of the top right corner
        - `top_left_style` -> the style of the top left corner
        - `bottom_right_style` -> the style of the bottom right corner
        - `bottom_left_style` -> the style of the bottom left corner

        - `corner_style` overrides all of the arguments above that are `None`.

        (corners thickness automatically assigned)
        """
        if style:
            if top_style == "default":
                top_style = style
            if bottom_style == "default":
                bottom_style = style
            if left_style == "default":
                left_style = style
            if right_style == "default":
                right_style = style
            if not corner_style:
                corner_style = style
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
            title_left=title_left,
            title_right=title_right,
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
            f"{self.top_right}{str(self.top_horizontal) * 3}{self.top_left}\n"
            f"{self.left_vertical}   {self.right_vertical}\n"
            f"{self.bottom_right}{str(self.bottom_horizontal) * 3}{self.bottom_left}\n"
        )


class Border:
    def __init__(self, border_type: BorderType):
        def create_instance(border_junctions: BorderJunctions):
            if isinstance(border_junctions, BorderPattern):
                return border_junctions
            elif isinstance(border_junctions, Junction):
                return copy(border_junctions)

            return Cell(border_junctions)

        self.top_right = create_instance(border_type.top_right)
        self.top_left = create_instance(border_type.top_left)
        self.bottom_right = create_instance(border_type.bottom_right)
        self.bottom_left = create_instance(border_type.bottom_left)

        self.top_horizontal = create_instance(border_type.top_horizontal)
        self.left_vertical = create_instance(border_type.left_vertical)
        self.bottom_horizontal = create_instance(border_type.bottom_horizontal)
        self.right_vertical = create_instance(border_type.right_vertical)

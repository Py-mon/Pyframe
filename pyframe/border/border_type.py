from dataclasses import dataclass

from pyframe.grid import Junction
from pyframe.types_ import Direction, JunctionDict, Thickness


@dataclass
class BorderType:
    top_right: JunctionDict
    top_left: JunctionDict
    bottom_right: JunctionDict
    bottom_left: JunctionDict

    top_horizontal: JunctionDict
    left_vertical: JunctionDict
    bottom_horizontal: JunctionDict
    right_vertical: JunctionDict

    def __repr__(self) -> str:
        return (
            f"{Junction(self.top_right)}{str(Junction(self.top_horizontal)) * 4}{Junction(self.top_left)}\n"
            f"{Junction(self.left_vertical)}    {Junction(self.right_vertical)}\n"
            f"{Junction(self.bottom_right)}{str(Junction(self.bottom_horizontal)) * 4}{Junction(self.bottom_left)}\n"
        )


def border_type(
    horizontal: Thickness, vertical
) -> tuple[
    JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict
]:
    return (
        {Direction.DOWN: vertical, Direction.RIGHT: horizontal},
        {Direction.DOWN: vertical, Direction.LEFT: horizontal},
        {Direction.UP: vertical, Direction.RIGHT: horizontal},
        {Direction.UP: vertical, Direction.LEFT: horizontal},
        {Direction.LEFT: horizontal, Direction.RIGHT: horizontal},
        {Direction.UP: vertical, Direction.DOWN: vertical},
    )


def _uniform(
    thickness: Thickness,
) -> tuple[
    JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict
]:
    return (
        {Direction.DOWN: thickness, Direction.RIGHT: thickness},
        {Direction.DOWN: thickness, Direction.LEFT: thickness},
        {Direction.UP: thickness, Direction.RIGHT: thickness},
        {Direction.UP: thickness, Direction.LEFT: thickness},
        {Direction.LEFT: thickness, Direction.RIGHT: thickness},
        {Direction.UP: thickness, Direction.DOWN: thickness},
        {Direction.LEFT: thickness, Direction.RIGHT: thickness},
        {Direction.UP: thickness, Direction.DOWN: thickness},
    )


class Borders:
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

    THIN = BorderType(*_uniform(Thickness.THIN))
    THICK = BorderType(*_uniform(Thickness.THICK))
    DOUBLE = BorderType(*_uniform(Thickness.DOUBLE))


print(Borders.THIN)
'2024-05-23 06:23 PM  May, 23, Thursday'
'2023-07-17 08:10 PM  July, 17, Monday'
'Entries: 50/50 (Modified A Lot)'

from collections.abc import Iterable
from math import sqrt
from random import randint
from typing import Iterable, Self, overload

from window.text.grid.point import Coord

from pybattle.log.errors import InvalidConvertType
from pybattle.types_ import is_nested, nested_len
from pybattle.window.text.grid.range import rect_range


class Size(Coord):
    """Immutable (height, width) representing the ending coordinate of a object"""

    @property
    def center(self) -> Self:
        """The center of the Size"""
        return type(self)(self.height // 2, self.width // 2)

    @classmethod
    def from_str(cls, string: str) -> Self:
        """Get the Size of a str"""
        return Size(
            string.removeprefix("\n").count("\n"), nested_len(string.splitlines())
        )

    @classmethod
    def from_list(cls, lst: list[list]) -> Self:
        """Get the Size of a nested list"""
        height = len(lst)
        width = nested_len(lst)

        return Size(height, width)

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

    @property
    def height(self) -> int:
        return self.y

    @property
    def width(self) -> int:
        return self.x

    @property
    def inner(self) -> Self:
        """The inner part from along the edge excluding the corners

        ```
          vvv
        ╭ ─── ╮
          ^^^
         ```
        """

        return self - Coord(2, 2)

    @property
    def i(self) -> Self:
        """The true size (0 inclusive)

        ```
        0 1 2 3 4
        ╭ ─ ─ ─ ╮
         ```
        """
        return self - Coord(1, 1)

    def __repr__(self) -> str:
        """Size(height, width)"""
        return f"Size(height={self.height}, width={self.width})"

    def random(self):
        """Get a random coordinate within the size."""
        return Coord(randint(0, self.height), randint(0, self.width))

    def __contains__(self, item: Coord):
        return self.height <= item.y and self.width <= item.y
        # return item in rect_range(self)

    @property
    def dis(self) -> float:
        """The distance (the amount of points) between the origin"""
        return sqrt(self.x**2 + self.y**2)

    @property
    def size(self):
        """Compare the size of a Size (without accurate spaces `Size(y=4, x=3)` is not double the size of `Size(y=2, x=3)`)"""
        return self.x**2 + self.y**2

    def __lt__(self, __other) -> bool:
        y, x = type(self)._convert(__other)
        return self.y**2 + self.x**2 < y**2 + x**2

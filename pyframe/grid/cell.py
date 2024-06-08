from collections.abc import Iterable
from typing import Any, Literal, Self

from pyframe.colors import Color, Colors

# from pyframe.screen.grid.emoji import is_emoji


class Cell:
    """A Cell in a matrix."""

    def __init__(
        self,
        value: str,
        color: Color = Colors.DEFAULT,
    ) -> None:
        self.value = value

        self.empty = self.value == " "

        self.color = color

        # self.emoji = False
        # is_emoji(value)

    def update(self, cell: Self):
        self.value = cell.value
        self.color = cell.color

    def __repr__(self) -> str:
        return str(self.value)

    def __len__(self) -> Literal[0]:
        return 0

    @classmethod
    def from_iter(cls, itr: Iterable) -> tuple[Self, ...]:
        """Create a list of cells from an iterable."""
        return tuple(cls(cell) for cell in itr)

    @classmethod
    def from_str(
        cls, string: str
    ) -> tuple[tuple[Self, ...], ...]:  # make work with \n at end
        return tuple(cls.from_iter(row) for row in string.split("\n"))

    @classmethod
    def from_size(cls, size, fill_with: str = " "):
        return tuple(
            tuple(cls(fill_with) for _ in range(size.width)) for _ in range(size.height)
        )

    def __mul__(self, times: int) -> tuple[Self, ...]:
        return tuple(type(self)(self.value, self.color) for _ in range(times))

    @classmethod
    def padding(cls, width: int, value=" ") -> tuple[Self, ...]:
        return tuple(cls(value) for _ in range(width))

    def __eq__(self, to):
        return self.value == to._value and self.color == to.color

    def __hash__(self) -> int:
        return hash((self.value, self.color))

    def __copy__(self):
        return Cell(self.value, self.color)

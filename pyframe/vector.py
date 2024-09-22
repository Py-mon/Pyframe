from __future__ import annotations

from collections.abc import Iterable
from typing import Iterable, NamedTuple, Optional, Self, overload


class VectorYX(NamedTuple("Vector", [("y", int), ("x", int)])):
    """A 2d Vector"""

    @overload
    def __new__(cls, lst: list[int], /) -> Self: ...

    @overload
    def __new__(cls, tup: tuple[int, int], /) -> Self: ...

    @overload
    def __new__(cls, y: int, x: int, /) -> Self: ...

    @overload
    def __new__(cls, yx: int, /) -> Self: ...

    @overload
    def __new__(cls, vector: Self, /) -> Self: ...

    def __new__(
        cls,
        y: VectorLike,
        x: Optional[int] = None,
    ) -> Self:
        if isinstance(y, cls):
            return y
        elif isinstance(y, int):
            if x is None:
                vector = y, y
            else:
                vector = (y, x)
        else:
            vector = y

        return super().__new__(cls, *vector)

    def __add__(self, other: VectorLike) -> Self:
        cls = type(self)
        vector = cls(other)
        return cls(self.y + vector.y, self.x + vector.x)

    def __sub__(self, other: VectorLike) -> Self:
        cls = type(self)
        vector = cls(other)
        return cls(self.y - vector.y, self.x - vector.x)

    def __mul__(self, other: VectorLike) -> Self:
        cls = type(self)
        vector = cls(other)
        return cls(self.y * vector.y, self.x * vector.x)

    def __pow__(self, other: VectorLike) -> Self:
        cls = type(self)
        vector = cls(other)
        return cls(self.y**vector.y, self.x**vector.x)

    def __floordiv__(self, other: VectorLike) -> Self:
        cls = type(self)
        vector = cls(other)
        return cls(self.y // vector.y, self.x // vector.x)

    @property
    def positive(self) -> Self:
        return type(self)(max(self.y, 0), max(self.x, 0))

    def distance(self, vector) -> float:
        return ((vector.x - self.x) ** 2 + (vector.y - self.y) ** 2) ** (1 / 2)

    def __str__(self):
        return f"Vector(y={self.y},x={self.x}))"

    def box_range(self, start_from: Optional[Self] = None) -> list[Self]:
        """Get a list of coordinates starting at `start` and ending at the Size in a rectangle."""
        start_from = start_from or type(self)(0, 0)
        return [
            type(self)(y, x)
            for y in range(start_from.y, self.y + 1)
            for x in range(start_from.x, self.x + 1)
        ]

    def box_range_nested(self, start_from: Optional[Self] = None) -> list[list[Self]]:
        """Get a `nested` list of coordinates starting at `start` and ending at the Size in a rectangle."""
        start_from = start_from or type(self)(0, 0)
        return [
            [type(self)(y, x) for x in range(start_from.x, self.x + 1)]
            for y in range(start_from.y, self.y + 1)
        ]


VectorLike = VectorYX | int | list[int] | tuple[int, int]


'2024-05-23 06:23 PM  May, 23, Thursday'
'2023-07-17 08:27 PM  July, 17, Monday'
'Entries: 50/50 (Modified A Lot)'

from collections.abc import Iterable
from typing import Iterable, NamedTuple, Self


class Point(NamedTuple):
    """Immutable 2D point in the format of (y, x) or (row, col)"""

    y: int
    x: int
    
    @property
    def row(self):
        return self.y
    
    @property
    def col(self):
        return self.x

    @classmethod
    def _convert(cls, obj: Iterable[int] | Self | int) -> Iterable[int] | Self:
        if not isinstance(obj, int):
            return obj
        return obj, obj

    def __add__(self, __other):
        y, x = type(self)._convert(__other)
        return type(self)(self.y + y, self.x + x)

    def __sub__(self, __other):
        y, x = type(self)._convert(__other)
        return type(self)(self.y - y, self.x - x)

    def __mul__(self, __other):
        y, x = type(self)._convert(__other)
        return type(self)(self.y * y, self.x * x)

    def __pow__(self, __other):
        y, x = type(self)._convert(__other)
        return type(self)(self.y**y, self.x**x)

    def __div__(self, __other):
        y, x = type(self)._convert(__other)
        return type(self)(self.y // y, self.x // x)


class Coord(Point):
    """Immutable 2D coordinate with positive values only, in the format of (y, x) or (row, col)"""
    def __init__(self, y, x):
        print('here')
        if y < 0 or x < 0:
            raise Exception

    @property
    def coords(self) -> tuple[int, int]:
        """Returns the current (y, x) coordinates as a tuple"""
        return tuple(self)
        
    def __lt__(self, other) -> bool:
        """Lexicographical Sorting"""
        return self.coords < tuple(type(self)._convert(other))



from typing import Iterable, Self, overload

from pybattle.log.errors import InvalidConvertType
from pybattle.types_ import is_nested, nested_len
from pybattle.window.text.grid.coord import Coord
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

    def __init__(self, width: int, height: int):
        super().__init__(width, height)

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
        return self.x**2 + self.y**2

    def __lt__(self, __other) -> bool:
        y, x = type(self)._convert(__other)
        return self.y**2 + self.x**2 < y**2 + x**2

# class Coord:
#     """Represents a 2D coordinate with positive values only, in the format of (y, x) or (row, col)"""

#     def __mul__(self, other) -> Self:
#         other = type(self)._convert(other)
#         return type(self)(self.y * other.y, self.x * other.x)

#     def __init__(self, y: int, x: int) -> None:
#         self.y = y
#         self.x = x

#     @property
#     def coords(self) -> tuple[int, int]:
#         """Returns the current (y, x) coordinates as a tuple"""
#         return self.y, self.x

#     @property
#     def x(self):
#         return self.__x

#     @x.setter
#     def x(self, to: int):
#         self.__x = max(0, to)

#     @property
#     def y(self):
#         return self.__y

#     @y.setter
#     def y(self, to: int):
#         self.__y = max(0, to)

#     @classmethod
#     def _convert(cls, obj: Self | int) -> Self:
#         """Tries to convert the object to a Coord object

#         Raises InvalidConvertType error on invalid object type"""
#         if isinstance(obj, Coord):
#             return obj
#         elif isinstance(obj, int):
#             return cls(obj, obj)
#         raise InvalidConvertType(type(obj), cls)

#     def __iter__(self):
#         return iter(self.coords)

#     def __add__(self, other) -> Self:
#         other = type(self)._convert(other)
#         return type(self)(self.y + other.y, self.x + other.x)

#     def __sub__(self, other) -> Self:
#         other = type(self)._convert(other)
#         return type(self)(self.y - other.y, self.x - other.x)

#     def __eq__(self, other) -> bool:
#         if isinstance(other, (Coord, int)):
#             other = type(self)._convert(other)
#             return self.coords == other.coords
#         return False

#     def __lt__(self, other) -> bool:
#         # Lexicographical Sorting
#         other = type(self)._convert(other)
#         return self.coords < other.coords

#     def __repr__(self) -> str:
#         return f"Coord(y={self.y}, x={self.x})"

#     def __hash__(self) -> int:
#         return hash(self.coords)

#     def distance(self, other: Self) -> float:
#         """Get the distance between one coord and another"""
#         return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


# from math import sqrt

# print(Coord(4, 4).distance(Coord(0, 0)))

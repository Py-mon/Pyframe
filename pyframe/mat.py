from collections.abc import Iterable
from copy import copy, deepcopy
from functools import cache
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Literal,
    Optional,
    Self,
    Type,
    Union,
    overload,
)

from pyframe.border.junction_table import get_junction
from pyframe.colors import Color, Colors
from pyframe.types_ import Alignment, Direction, JunctionDict


class Cell:
    """A Cell in a matrix."""

    def __init__(
        self,
        value: str,
        color: Color = Colors.DEFAULT,
    ) -> None:
        if len(value) > 1:
            raise ValueError("value more than 1 character")

        self.value = value

        self.empty = self.value == " "

        self.color = color

    def update(self, cell: Self):
        self.value = cell.value
        self.color = cell.color

    def __repr__(self) -> str:
        return str(self.value)

    def __len__(self) -> Literal[0]:
        return 0

    # @classmethod
    # def from_iter(cls, itr: Iterable) -> tuple[Self, ...]:
    #     """Create a list of cells from an iterable."""
    #     return tuple(cls(cell) for cell in itr)

    # @classmethod
    # def from_str(
    #     cls, string: str
    # ) -> tuple[tuple[Self, ...], ...]:  # make work with \n at end
    #     return tuple(cls.from_iter(row) for row in string.split("\n"))

    # @classmethod
    # def from_size(cls, size, fill_with: str = " "):
    #     return tuple(
    #         tuple(cls(fill_with) for _ in range(size.width)) for _ in range(size.height)
    #     )

    # def __mul__(self, times: int) -> tuple[Self, ...]:
    #     return tuple(type(self)(self.value, self.color) for _ in range(times))

    # @classmethod
    # def padding(cls, width: int, value=" ") -> tuple[Self, ...]:
    #     return tuple(cls(value) for _ in range(width))

    # def __eq__(self, to):
    #     return self.value == to._value and self.color == to.color

    # def __hash__(self) -> int:
    #     return hash((self.value, self.color))

    # def __copy__(self):
    #     return Cell(self.value, self.color)


class Junction(Cell):
    """A Cell that is the borders of frames."""

    def __init__(
        self,
        dct: JunctionDict,
        color: Color = Colors.DEFAULT,
    ) -> None:
        self._dct = dct

        self.empty = self.value == " "

        self.color = color

    @property
    def value(self):
        return get_junction(self._dct)

    def __repr__(self):
        return self.value

    @property
    def dct(self):
        return self._dct

    def __add__(self, junction: Self) -> Self:
        return type(self)(self.dct | junction.dct, junction.color)

    # def __mul__(self, times: int) -> tuple[Self, ...]:
    #     return tuple(Junction(self.dct, self.color) for _ in range(times))


def add_positions(*tups: tuple[int, int]):
    y, x = tups[0]
    for tup in tups[1:]:
        y += tup[0]
        x += tup[1]
    return y, x


def sub_positions(*tups: tuple[int, int]):
    y, x = tups[0]
    for tup in tups[1:]:
        y -= tup[0]
        x -= tup[1]
    return y, x


def add_int_positions(int_, *ints: int):
    y, x = int_
    for int_ in ints:
        y += int_
        x += int_
    return y, x


def add_y_from(tup, y):
    return tup[0] + y, tup[1]


def add_x_from(tup, x):
    return tup[0], tup[1] + x


class Grid:
    def __init__(
        self,
        cells: str | list[list[Cell]],
        alignment: Alignment = Alignment.LEFT,
    ):
        if isinstance(cells, str):
            rows = cells.split("\n")
            self._cells = [[Cell(cell) for cell in row] for row in rows]
        else:
            self._cells = cells

        self.height = len(self._cells)

        def create_padding(width: int, value=" ") -> list[Cell]:
            return [Cell(value) for _ in range(width)]

        def level_out(rows: list[list[Cell]], alignment: Alignment = Alignment.LEFT):
            """Level out the rows of the matrix making them all the same width."""
            max_length = max(len(row) for row in rows)

            for i, row in enumerate(rows):
                row_length = len(row)

                if row_length >= max_length:
                    continue

                if alignment == Alignment.LEFT:
                    row.extend(create_padding(max_length - row_length))
                elif alignment == Alignment.RIGHT:
                    rows[i] = create_padding(max_length - row_length) + row
                elif alignment == Alignment.CENTER:
                    left_padding = (max_length - row_length) // 2
                    right_padding = max_length - row_length - left_padding
                    rows[i] = (
                        create_padding(left_padding)
                        + row
                        + create_padding(right_padding)
                    )
            return max_length

        if self._cells:
            self.width = level_out(self._cells, alignment)
        else:
            self.width = 0

    @property
    def size(self) -> tuple[int, int]:
        """`(height, width)`"""
        return self.height, self.width

    def color(self, color: Color, coords: list[tuple[int, int]]) -> None:
        """Color cells in the matrix."""
        for coord in coords:
            self[coord].color = color

    def color_all(self, color: Color) -> None:
        """Color the whole matrix a certain color."""
        for cell in self:
            cell.color = color

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate through every cell."""
        for row in self._cells:
            for cell in row:
                yield cell

    @overload
    def __getitem__(self, row: int, /) -> Self: ...

    @overload
    def __getitem__(self, slice_: slice, /) -> Self: ...

    @overload
    def __getitem__(self, coord: tuple[int, int], /) -> Cell: ...

    def __getitem__(self, item, /):
        if isinstance(item, tuple):
            return self._cells[item[0]][item[1]]

        elif isinstance(item, slice):
            start_y, start_x = item.start or (0, 0)

            if item.stop is None:
                stop_y, stop_x = (self.height - start_y, self.width - start_x)
            else:
                stop_y, stop_x = item.stop

            stop_y += 1
            stop_x += 1

            return Grid([row[start_x:stop_x] for row in self._cells[start_y:stop_y]])

        elif isinstance(item, int):
            return self._cells[item]

    @overload
    def __setitem__(self, slice_: slice, matrix: Self, /) -> None: ...

    @overload
    def __setitem__(self, index: int, row: list[Cell], /) -> None: ...

    @overload
    def __setitem__(self, tup: tuple[int, int], value: Cell, /) -> None: ...

    def __setitem__(self, item, new_cells, /) -> None:
        if isinstance(item, tuple):
            self._cells[item[0]][item[1]] = new_cells  # update?

        elif isinstance(item, int):
            self._cells[item] = new_cells

        elif isinstance(item, slice):
            start_y, start_x = item.start or (
                (item.stop[0] - new_cells.height + 1),
                (item.stop[1] - new_cells.width + 1),
            )
            stop_y, stop_x = item.stop or (
                (item.start[0] + new_cells.height - 1),
                (item.start[1] + new_cells.width - 1),
            )

            for i in range(start_y, stop_y + 1):
                print(new_cells[i - start_y], self._cells[i][start_x : stop_x + 1])
                # self._cells[start_y : stop_y + 1][i][start_x : stop_x + 1] = new_cells[
                #     i - start_y
                self._cells[i][start_x : stop_x + 1] = new_cells[
                    i - start_y
                ]

            # for i, row in enumerate(self._cells[start_y : stop_y + 1]):
            #     print(new_cells[i], row, row[start_x : stop_x + 1])
            #     row[start_x : stop_x + 1] = new_cells[i]

    def overlay_from_top_left(self, m: Self, pos: tuple[int, int]) -> None:
        print(add_int_positions(add_positions(pos, m.size), -1))
        self[pos : add_int_positions(add_positions(pos, m.size), -1)] = m

    def overlay_from_bottom_right(self, m: Self, pos: tuple[int, int]) -> None:
        self[add_int_positions(sub_positions(pos, m.size), 1) : pos] = m

    def overlay_from_bottom_left(self, m: Self, pos: tuple[int, int]) -> None:
        self[add_y_from(pos, -(m.height - 1)) : add_x_from(pos, m.width + 1)] = m

    def overlay_from_top_right(self, m: Self, pos: tuple[int, int]) -> None:
        print(add_x_from(pos, -(m.width - 1)), pos, -(m.width - 1))
        self[add_x_from(pos, -(m.width - 1)) : add_y_from(pos, m.height + 1)] = m

    # def overlay_from_top_left(self, m: "Grid", pos: Coord) -> None:
    #     self[pos : pos + m.size - 1] = m

    # def overlay_from_bottom_right(self, m: "Grid", pos: Coord) -> None:
    #     self[pos - m.size + 1 : pos] = m

    # def overlay_from_bottom_left(self, m: "Grid", pos: Coord) -> None:
    #     self[pos.sub_y(m.size.height - 1) : pos.add_x(m.size.width + 1)] = m

    # def overlay_from_top_right(self, m: "Grid", pos: Coord) -> None:
    #     self[pos.sub_x(m.size.width - 1) : pos.add_y(m.size.height + 1)] = m

    @property
    def rows(self):
        """The same as `self.cells` (for readability in for loops: `for row in matrix"""
        return self._cells

    def __str__(self) -> str:
        """The values of each cell joined together."""
        x = []
        for row in self.rows:
            for cell in row + [Cell("\n")]:
                x.append(str(cell.value))

        return "".join(x)[:-1]

    def colored_str(self) -> str:
        """The colors and values of each cell joined together."""
        x = []
        pre_cell = None
        for row in self.rows:
            for cell in row + [Cell("\n")]:
                # print(cell.color, pre_cell.color if pre_cell else "")
                color = ""
                if pre_cell is None:
                    color = f'\033[38;2;{";".join([str(x) for x in cell.color.rgb])}m'
                elif pre_cell.color != cell.color:
                    color = f'\033[38;2;{";".join([str(x) for x in cell.color.rgb])}m'

                pre_cell = cell

                x.append(color + str(cell.value))

        return "".join(x)[:-1] + f"\033[0m"

    # def remove_whitespace_sides(self):
    #     matrix = list(self.cells)
    #     while all(row[1].value == " " for row in matrix):
    #         for i in range(len(matrix)):
    #             matrix[i] = matrix[i][2:]
    #     # Remove leading space rows
    #     while matrix[0] and all(
    #         matrix[0][i].value == " " for i in range(len(matrix[0]))
    #     ):
    #         matrix.pop(0)
    #     # Remove trailing space rows
    #     while matrix[-1] and all(
    #         matrix[-1][i].value == " " for i in range(len(matrix[-1]))
    #     ):
    #         matrix.pop()
    #     self.cells = tuple(matrix)

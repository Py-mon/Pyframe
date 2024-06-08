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

import numpy as np
from numpy.typing import NDArray

from pyframe.grid.cell import Cell
from pyframe.grid.point import Vector2D

# from pyframe.log.errors import OutOfBounds, TooSmallError
# from pyframe.screen.colors import Color, Colors
# from pyframe.screen.frames.border.junction_table import get_junction
# from pyframe.screen.grid.cell import Cell
# from pyframe.screen.grid.nested import (
#     flatten,
#     format,
#     is_nested,
#     level_out,
#     max_len,
#     nest,
# )
# from pyframe.screen.grid.point import Coord, Point, Size
# from pyframe.types_ import Alignment, Direction, JunctionDict


class Junction(Cell):
    """A Cell that is the borders of frames."""

    def __init__(self, dct: JunctionDict, color: Color = Colors.DEFAULT):
        super().__init__(dct, color, True)

    @property
    def value(self):
        return get_junction(self._value)

    def __repr__(self):
        return self.value

    @property
    def dct(self):
        return self._value

    def __add__(self, junction: Self) -> Self:
        return Junction(self.dct | junction.dct, junction.color)

    def __mul__(self, times: int) -> tuple[Self, ...]:
        return tuple(Junction(self.dct, self.color) for _ in range(times))


class Grid:
    def __init__(
        self,
        cells: str | list[list[Cell]] | NDArray,
        alignment: Optional[Alignment] = Alignment.LEFT,
    ):
        if isinstance(cells, np.ndarray):
            self.array = cells
            return

        if isinstance(cells, str):
            cells = Cell.from_str(cells)

        if alignment:
            level_out(cells, alignment)

        self.array = np.array(cells, dtype=Cell)

    def copy(self):
        return Grid(deepcopy(self.array))

    def copy2(self):
        return Grid(self.array.copy())

    @property
    def size(self) -> Size:
        """The amount of elements vertical and horizontal."""
        return Size(self.array.shape[0], self.array.shape[1])

    @property
    def coords(self):
        """All of the valid coordinates in the Grid."""
        return self.size.i.rect_range()

    @property
    def coord_mapping(self) -> dict[Coord, Cell]:
        """A mapping of each coordinate to its Cell."""
        dct: dict[Coord, Cell] = {}
        for i, row in enumerate(self.array):
            for j, cell in enumerate(row):
                dct[Coord(i, j)] = cell
        return dct

    @property
    def coord_mapping_rows(self) -> list[dict[Coord, Cell]]:
        """A list of rows mapping each coordinate to its Cell."""
        lst: list[dict[Coord, Cell]] = []
        for i, row in enumerate(self.array):
            dct: dict[Coord, Cell] = {}
            for j, cell in enumerate(row):
                dct[Coord(i, j)] = cell
            lst.append(dct)
        return lst

    def color(self, color: Color, coords: list[Coord]) -> None:
        """Color cells in the matrix."""
        for coord in coords:
            if coord not in self.size:
                raise OutOfBounds(
                    f"The color '{color.name}' at {coord} is out of bounds of {self.size.i} by {(coord - self.size.i).non_negative}"
                )
            self[coord].color = color

    def color_all(self, color: Color) -> None:
        """Color the whole matrix a certain color."""
        self.color(color, self.coords)

    def __contains__(self, item: Coord | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        if isinstance(item, Coord):
            return item in self.coords
        return Cell(item) in self.array

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate through every cell"""
        for row in self.array:
            for cell in row:
                yield cell

    @overload
    def __getitem__(self, row: int, /) -> Self: ...

    @overload
    def __getitem__(self, slice_: slice, /) -> Self: ...

    @overload
    def __getitem__(self, coord: Coord, /) -> Cell: ...

    @overload
    def __getitem__(self, coord: tuple[int, int], /) -> Cell: ...

    @overload
    def __getitem__(
        self, coord: tuple[slice, slice] | tuple[int, slice] | tuple[slice, int], /
    ) -> NDArray: ...

    def __getitem__(self, item, /):
        # out of bounds
        if isinstance(item, tuple):
            return self.array[item[0], item[1]]

        if isinstance(item, Coord):
            return self.array[item.y, item.x]

        elif isinstance(item, slice):
            start: Coord = item.start or Coord(0, 0)

            if item.stop is None:
                stop = Size(self.size.width, self.size.height) - start
            else:
                stop = Size(*item.stop)

            stop += 1

            return Grid(self.array[start.y : stop.y, start.x : stop.x])

        elif isinstance(item, int):
            return Grid([self.array[item]])

    @overload
    def __setitem__(self, coord: Coord, cell: Cell | str, /) -> None: ...

    @overload
    def __setitem__(self, slice_: slice, matrix: Self | str | Any, /) -> None: ...

    @overload
    def __setitem__(self, index: int, row: list[Cell], /) -> None: ...

    @overload
    def __setitem__(self, tup: tuple[int, int], value: Cell, /) -> None: ...

    def __setitem__(self, item, new_cells, /) -> None:
        if isinstance(item, tuple):
            self.array[item[0], item[1]] = new_cells

        elif isinstance(item, Coord):
            if isinstance(new_cells, str):
                new_cells = Cell(new_cells)
            self.array[item.y, item.x].update(new_cells)

        elif isinstance(item, int):
            self.array[item] = new_cells

        elif isinstance(item, slice):
            if isinstance(new_cells, str):
                new_cells = Grid(new_cells)

            start: Coord = item.start or (item.stop - new_cells.size + 1)
            stop: Coord = item.stop or (item.start + new_cells.size - 1)

            stop += 1

            self.array[start.y : stop.y, start.x : stop.x] = new_cells.array

            # ?Better way to fix?
            # for coord, cell in new_cells.coord_mapping.items():
            #     if cell.double:
            #         self[coord.y + start.y] = [
            #             *self[coord.y + start.y, :-2],
            #             self[coord.y + start.y, -1],
            #             self[coord.y + start.y, -2],
            #         ]

    def overlay_from_top_left(self, m: "Grid", pos: Coord) -> None:
        self[pos : pos + m.size - 1] = m

    def overlay_from_bottom_right(self, m: "Grid", pos: Coord) -> None:
        self[pos - m.size + 1 : pos] = m

    def overlay_from_bottom_left(self, m: "Grid", pos: Coord) -> None:
        self[pos.sub_y(m.size.height - 1) : pos.add_x(m.size.width + 1)] = m

    def overlay_from_top_right(self, m: "Grid", pos: Coord) -> None:
        self[pos.sub_x(m.size.width - 1) : pos.add_y(m.size.height + 1)] = m

    def extend_row(self, row: Optional[list] = None, n: int = 1):
        """Extend `n` row(s) of spaces (if negative extends the opposite way)"""
        if row is None:
            row = Cell.padding(self.size.width)

        if n < 0:
            self.array = np.vstack((*(row for _ in range(-n)), self.array))
        else:
            self.array = np.vstack((self.array, *(row for _ in range(n))))

    def extend_column(self, row: Optional[list] = None, n: int = 1):
        """Extend `n` row(s) of spaces (if negative extends the opposite way)"""
        if row is None:
            row = Cell.padding(self.size.height)

        if n < 0:
            self.array = np.hstack(
                (*[np.transpose([row]) for _ in range(-n)], self.array)
            )
        else:
            self.array = np.hstack(
                (self.array, *[np.transpose([row]) for _ in range(n)])
            )

    @property
    def rows(self) -> np.ndarray:
        """The same as `self.cells` (for readability in for loops: `for row in matrix"""
        return self.array

    @property
    def cols(self) -> list[list[Cell]]:
        """Transposed rows."""
        return [list(col) for col in list(zip(*self.rows))]

    def __repr__(self) -> str:
        """A formatted representation of the matrix."""
        return format(self.array.tolist())

    def __str__(self) -> str:
        """The colors and values of each cell joined together."""
        skip = False
        x = []
        for row in self.array.tolist():
            for cell in row + [Cell("\n")]:
                if skip:
                    skip = False
                    continue

                x.append(str(cell.value))

        return "".join(x)[:-1]

    def colored_str(self) -> str:
        """The colors and values of each cell joined together."""

        useable = []
        for row in self.array:
            new_row = list(row)

            for i, cell in enumerate(new_row):
                if not cell.emoji:
                    continue

                for j in range(i, len(row)):
                    print(j, new_row[j], new_row[j + 1])
                    if new_row[j].value == "│":
                        del new_row[j + 1]
                        break

                # for j in range(1, len(row)):
                #     print(-j, new_row[-j], "".join([cell.value for cell in new_row]))
                #     if new_row[-j].value == " ":
                #         print('cut')
                #         del new_row[-j]
                #         break

            useable.append(new_row)

        x = []
        pre_cell = None
        for row in useable:
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

    def move_space(self, coord, to_coord):
        # convert to list and then convert back
        # if double then in str remove space at end

        # print(np.delete(self.array, coord.y, axis=coord.x))
        pass

    # def print_x(self):
    #     for cell in self:
    #         if cell.double:


# import numpy

# m = Grid("123\n456")

# from time import time

# print(time())
# x = time()
# for _ in range(100000):
#     n = ""
#     for row in m.rows:
#         row_html = "".join(
#             [
#                 f'<code class="c" style="color: rgb{cell.color.rgb};">{cell.value}</code>'
#                 for cell in row
#             ]
#         )
#         n += f"{row_html}<br>"

#     # .7
#     # n = ''
#     # for row in m.rows:
#     #     for cell in row:
#     #         n += f'<code class="c" style="color: rgb{cell.color.rgb};">{cell.value}</code>'
#     #     n += f"<br>"

#     n = ""
#     for row in m.rows:

#         n +=str(map(
#             lambda cell: f'<code class="c" style="color: rgb{cell.color.rgb};">{cell.value}</code>', row
#         ))+"<br>"

#     # n = numpy.array2string(
#     #     m.rows,
#     #     separator="",
#     #     max_line_width=99999,
#     #     formatter={
#     #         "all": lambda cell: f'<code class="c" style="color: rgb{cell.color.rgb};">{cell.value}</code>'
#     #     },
#     # )
# print(time() - x)
# print(time())

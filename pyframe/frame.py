from copy import copy, deepcopy
from dataclasses import dataclass
from math import ceil
from typing import Any, Callable, Optional, Self

from pyframe.border.border_type import Border, BorderType, BorderTypes
from pyframe.border.junction_table import get_junction
from pyframe.colors import Color, Colors
from pyframe.grid import Cell, Grid, Junction, add_int_positions, add_positions
from pyframe.types_ import Alignment, Direction, JunctionDict, Level


@dataclass
class Title:
    title: str
    x: int | Alignment = Alignment.LEFT
    color: Color = Colors.DEFAULT
    margin: int = 2
    level: Level = Level.TOP


def get_center_position(position):
    return position[0] // 2, position[1] // 2


def convert_align_to_pos(
    alignment: Alignment | int,
    of: tuple[int, int],
    right_adjustment: int = 0,
    margins: int = 3,
):
    print(alignment)
    if not isinstance(alignment, Alignment):
        return alignment

    if alignment == type(alignment).CENTER or alignment == type(alignment).MIDDLE:
        return get_center_position(of)[1] - 1
    elif alignment == type(alignment).LEFT:
        right_offset_margin = of[1] - margins - right_adjustment
        if margins >= right_offset_margin:
            return right_offset_margin

        return margins
    elif alignment == type(alignment).RIGHT:
        return of[1] - right_adjustment - margins


def rect_range(stop, start=None) -> list[tuple[int, int]]:
    start = start or (0, 0)
    return [
        (y, x)
        for y in range(start[0], stop[0] + 1)
        for x in range(start[1], stop[1] + 1)
    ]


class Frame(Grid):
    @classmethod
    def centered(
        cls,
        text: str,
        height: int,
        width: int,
        border_type: BorderType = BorderTypes.THIN,
        alignment: Alignment = Alignment.CENTER,
    ) -> Self:
        """
        ```
        >>> Frame.centered("abcdef\\nghij")
        ╭──────────╮
        │          │
        │  abcdef  │
        │   ghij   │
        │          │
        ╰──────────╯
        """
        frame = cls(
            [[Cell(" ") for _ in range(width)] for _ in range(height)], border_type
        )

        aligned_text = Grid(
            [[Cell(cell) for cell in row] for row in text.split("\n")], alignment
        )
        slice_ = get_box(frame.size, add_int_positions(aligned_text.size, -1))

        frame[slice_] = aligned_text

        return frame

    @classmethod
    def box(
        cls,
        height: int,
        width: int,
        border_type: BorderType = BorderTypes.THIN,
    ) -> Self:
        frame = cls(
            [[Cell(" ") for _ in range(width - 2)] for _ in range(height - 2)],
            border_type,
        )
        if height == 2:
            frame.width = width - 2
            frame.border()
        return frame

    def __init__(
        self,
        cells: list[list[Cell]],
        border_type: BorderType = BorderTypes.THIN,
    ) -> None:
        super().__init__(cells)

        self.titles: list[Title] = []

        self.border_type = border_type
        self.border_color = None
        self.left_title_color = None
        self.right_title_color = None
        self.base_color = None

        if self.width != 0:
            self.border()

    def color_inner(self, color: Color):
        self.base_color = color
        self.color(
            self.base_color, rect_range(add_int_positions(self.size, -2), (1, 1))
        )

    def color_border(self, color: Color):
        self.border_color = color
        self.color(self.border_color, self.border_coords)

        self.recolor_titles()

    def recolor_titles(self):
        for title in self.titles:
            pos = convert_align_to_pos(
                title.x, self.size, len(title.title), title.margin + 1
            )

            self.color(
                title.color,
                rect_range(
                    (title.level.value, pos + len(title.title) - 1),
                    (title.level.value, pos),
                ),
            )

    def unborder(self):
        """Remove the border."""
        self._cells = self[(1, 1) : add_int_positions(self.size, -2)]._cells

    def add_title(self, title: Title) -> None:
        matrix = Grid(
            [
                [Cell(cell) for cell in row]
                for row in ("╴" + title.title + "╶").split("\n")
            ]
        )

        # matrix.color(title.color, matrix.size.i.sub_x(1).rect_range(Coord(0, 1)))

        pos = convert_align_to_pos(
            title.x, self.size, len(title.title), title.margin + 1
        )

        self[
            (title.level.value, pos - 1) : (title.level.value, pos + len(title.title))
        ] = matrix  # type: ignore

        self.titles.append(title)

    def border(self):
        """Add a border around the Matrix."""
        border = Border(self.border_type)

        def pattern(
            junction,
            width,
        ):
            if isinstance(junction, list):
                return [junction[i % len(junction)] for i in range(width)]
            return junction * width

        top_row = [
            border.top_right,
            *pattern(border.top_horizontal, self.width),
            border.top_left,
        ]

        left_column = border.left_vertical * self.height
        right_column = border.right_vertical * self.height

        bottom_row = [
            border.bottom_right,
            *pattern(border.bottom_horizontal, self.width),
            border.bottom_left,
        ]

        for i, row in enumerate(self._cells):
            row.insert(0, left_column[i])
            row.append(right_column[i])

        self._cells.append(bottom_row)
        self._cells.insert(0, top_row)

        self.height += 2
        self.width += 2

        self.border_coords = (
            [(0, i) for i in range(self.width)]
            + [(self.height - 1, i) for i in range(self.width)]
            + [(i, 0) for i in range(1, self.height - 1)]
            + [(i, self.width - 1) for i in range(self.height - 1)]
        )

        for title in self.titles.copy():
            self.add_title(title)

    def add_frame(
        self,
        frame: Self,
        pos: tuple[int, int] = (0, 0),
        change_border_color: bool = False,
    ) -> None:
        # deepcopy frame if not wanted to share changes
        # frame.objs.append(self)

        junctions: list[tuple[Junction, tuple[int, int]]] = []

        for coord in frame.border_coords:
            coord_pos = add_positions(coord, pos)

            self_junction = self[coord_pos]
            frame_junction = frame[coord]

            if isinstance(self_junction, Junction) and isinstance(
                frame_junction, Junction
            ):
                junctions.append((self_junction + frame_junction, coord_pos))

        self.overlay_from_top_left(frame, pos)

        for junction, coord in junctions:
            print(junction, coord)
            for direction in junction.dct.copy():
                ahead = (0, 0)
                match direction:
                    case Direction.UP:
                        ahead = (coord[0] - 1, coord[1])
                    case Direction.DOWN:
                        ahead = (coord[0] + 1, coord[1])
                    case Direction.LEFT:
                        ahead = (coord[0], coord[1] - 1)
                    case Direction.RIGHT:
                        ahead = (coord[0], coord[1] + 1)
                try:
                    if not isinstance(self[ahead], Junction):
                        junction.dct.pop(direction)
                except IndexError:  # out of bounds
                    pass

            self[coord]._dct = junction.dct

        if not change_border_color and self.border_color is not None:
            self.color_border(self.border_color)

    # if self.title is not None:
    #     for i, char in enumerate(" " + self.title + " "):
    #         self[Coord(0, i + 2)] = Cell(char, self.title_color, True)


def get_box(center_of: tuple[int, int], size: tuple[int, int]) -> slice:
    """Get a slice that is the size of inner_size in the center of the outer_size."""
    return slice(
        (
            ceil((center_of[0] - size[0]) / 2 - 1),
            ceil((center_of[1] - size[1]) / 2 - 1),
        ),
        (
            ceil((center_of[0] + size[0]) / 2 - 1),
            ceil((center_of[1] + size[1]) / 2 - 1),
        ),
    )


from pyframe.border.border_type import Thickness

f = Frame.centered(
    "abcdef\nghij",
    4,
    10,
    BorderTypes.THIN
)
print(f.width)
print(f._cells)
print(f)
# f = Frame.box(6, 10)
# f.add_title(Title("SO", Alignment.CENTER, Colors.BLUE))
# f.add_frame(Frame.box(4, 5), (1, 0))
# # f.color_border(Colors.RED)
# print(f)
# print(f.colored_str())

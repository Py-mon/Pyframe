from dataclasses import dataclass
from math import ceil
from typing import Self

from pyframe.border.border_type import Border, BorderPattern, BorderType
from pyframe.border.border_types import Borders
from pyframe.border.junction import Junction
from pyframe.colors import Color, Colors
from pyframe.grid import Cell, Grid
from pyframe.types_ import Alignment, Direction, TitleSide
from pyframe.vector import VectorYX

from typing import overload

# TODO game package -> sprites, ui package -> scroll wheel mouse inputs buttons etc


@dataclass
class Title:
    title: str
    alignment: int | Alignment = Alignment.LEFT
    color: Color = Colors.DEFAULT
    margin: int = 2
    title_side: TitleSide = TitleSide.TOP  # side titles


def get_center_position(position):
    return position[0] // 2, position[1] // 2


def convert_align_to_pos(
    alignment: Alignment | int,
    of: int,
    length_adjustment: int = 0,
    margin: int = 3,
):
    if not isinstance(alignment, Alignment):
        return alignment

    max_margin = of - length_adjustment - 4  # two corners, two title sides
    margin = min(max_margin, margin)

    if alignment == type(alignment).CENTER or alignment == type(alignment).MIDDLE:
        return of // 2 - ceil(length_adjustment / 2) + 1
    elif alignment == type(alignment).LEFT:
        right_offset_margin = of - margin - length_adjustment
        if margin >= right_offset_margin:
            return right_offset_margin

        return margin
    elif alignment == type(alignment).RIGHT:
        return of - length_adjustment - margin


def rect_range(stop, start=None) -> list[tuple[int, int]]:
    start = start or (0, 0)
    return [
        (y, x)
        for y in range(start[0], stop[0] + 1)
        for x in range(start[1], stop[1] + 1)
    ]


class Frame(Grid):
    @classmethod
    def empty_box(
        cls,
        height: int,
        width: int,
        border_type: BorderType = Borders.Thin.ROUND,
    ) -> "Frame":
        """Includes border"""
        frame = Frame(
            [[Cell(" ") for _ in range(width - 2)] for _ in range(height - 2)],
            border_type,
        )
        if height == 2:
            frame.width = width - 2
            frame.border()

        return frame

    @classmethod
    def map_text(
        cls,
        text: str,
        border_type: BorderType = Borders.Thin.ROUND,
    ) -> Self:
        return cls(
            [[Cell(char) for char in row] for row in text.splitlines()], border_type
        )

    @overload
    def __init__(self, grid: Grid, border_type: BorderType = Borders.Thin.ROUND, /): ...

    @overload
    def __init__(
        self,
        cells: list[list[Cell]],
        border_type: BorderType = Borders.Thin.ROUND,
        /,
    ): ...

    def __init__(
        self,
        cells: list[list[Cell]] | Grid,
        border_type: BorderType = Borders.Thin.ROUND,
    ) -> None:
        if isinstance(cells, Grid):
            cells = cells._cells

        super().__init__(cells)

        self.titles: list[Title] = []

        self.border_type = border_type
        self.border_color = None
        self.left_title_color = None
        self.right_title_color = None
        self.base_color = None

        if self.width != 0:
            self.border()

        self.children = []
        self.parents = []

    def color_inner(self, color: Color):
        self.base_color = color
        self.color(self.base_color, rect_range(VectorYX(self.size) - 2, (1, 1)))

    def color_border(self, color: Color):
        self.border_color = color
        self.color(self.border_color, self.border_coords)

        self._add_titles()

    def _add_titles(self):
        for title in self.titles:
            title_right = (
                self.border_type.title_right_top
                if title.title_side == TitleSide.TOP
                else self.border_type.title_right_bottom
            )
            title_left = (
                self.border_type.title_left_top
                if title.title_side == TitleSide.TOP
                else self.border_type.title_left_bottom
            )
            title_right = (
                title_right if isinstance(title_right, str) else title_right.value
            )
            title_left = title_left if isinstance(title_left, str) else title_left.value

            matrix = Grid(
                [
                    [Cell(title_left, color=self.border_color)]
                    + [Cell(cell, color=title.color) for cell in title.title]
                    + [Cell(title_right, color=self.border_color)]
                ]
            )

            pos = convert_align_to_pos(
                title.alignment,
                (
                    self.size[0]
                    if title.title_side in [TitleSide.LEFT, TitleSide.RIGHT]
                    else self.size[1]
                ),
                len(title.title),
                title.margin + 1,
            )

            start_pos = pos - 1

            if title.title_side == TitleSide.LEFT:
                self[(start_pos, 0):] = Grid(list(map(list, zip(*matrix._cells))))
            elif title.title_side == TitleSide.RIGHT:
                self[(start_pos, self.width - 1) :] = Grid(
                    list(map(list, zip(*matrix._cells)))
                )
            elif title.title_side == TitleSide.TOP:
                self[(0, start_pos):] = matrix
            elif title.title_side == TitleSide.BOTTOM:
                self[(self.height - 1, start_pos) :] = matrix

    def unborder(self):
        """Remove the border."""
        self._cells = self[(1, 1) : VectorYX(self.size) - 2]._cells

    def add_title(self, title: Title) -> None:  # make titles better
        self.titles.append(title)

        self._add_titles()  # maybe separate construct function?

    def border(self):
        """Add a border around the Matrix."""
        border = Border(self.border_type)

        top_row = [
            border.top_right,
            *(border.top_horizontal * self.width),
            border.top_left,
        ]

        left_column = border.left_vertical * self.height
        right_column = border.right_vertical * self.height

        bottom_row = [
            border.bottom_right,
            *(border.bottom_horizontal * self.width),
            border.bottom_left,
        ]

        for i, row in enumerate(self._cells):
            row.insert(0, left_column[i])
            row.append(right_column[i])

        self._cells.append(bottom_row)
        self._cells.insert(0, top_row)

        self.height += 2
        self.width += 2

        self.top_coords = [(0, i) for i in range(1, self.width - 1)]
        self.bottom_coords = [(self.height - 1, i) for i in range(1, self.width - 1)]
        self.left_coords = [(i, 0) for i in range(1, self.height - 1)]
        self.right_coords = [(i, self.width - 1) for i in range(1, self.height - 1)]

        self.corner_coords = [
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
        ]

        self.border_coords = [
            *self.top_coords,
            *self.bottom_coords,
            *self.left_coords,
            *self.right_coords,
            *self.corner_coords,
        ]

        self._add_titles()

    def add_frame(
        self,
        frame: Self,
        pos: tuple[int, int] = (0, 0),
        change_border_color: bool = False,
    ) -> None:
        frame.parents.append(self)
        self.children.append(frame)

        junctions: list[tuple[Junction, tuple[int, int]]] = []

        def combine_junctions(coords, remove_direction=None):
            for coord in coords:
                coord_pos = VectorYX(coord) + VectorYX(pos)

                self_junction = self[coord_pos]
                frame_junction = frame[coord]

                if not isinstance(self_junction, Junction) or not isinstance(
                    frame_junction, Junction
                ):
                    continue

                junction = self_junction + frame_junction
                if remove_direction and remove_direction in junction._directions:
                    junction._directions.pop(remove_direction)
                junction._update_value()
                junctions.append((junction, coord_pos))

        combine_junctions(frame.top_coords, Direction.DOWN)
        combine_junctions(frame.bottom_coords, Direction.UP)
        combine_junctions(frame.left_coords, Direction.RIGHT)
        combine_junctions(frame.right_coords, Direction.LEFT)
        combine_junctions(frame.right_coords, Direction.LEFT)
        combine_junctions(frame.corner_coords)

        # self.overlay_from_top_left(frame, pos)
        self.overlay_from_top_right(frame, pos)

        for junction, coord in junctions:
            self[coord] = junction

        if not change_border_color and self.border_color is not None:
            self.color_border(self.border_color)

        self._add_titles()


def get_centered_box(center_of: tuple[int, int], size: tuple[int, int]) -> slice:
    """Get a slice that is the shape of `size` in the center of the `center_of`."""
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

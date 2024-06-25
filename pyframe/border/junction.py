import json
from typing import Self

from pyframe.colors import Color, Colors
from pyframe.grid import Cell
from pyframe.types_ import Direction, JunctionDict, Thickness

# TABLE[UP][DOWN][LEFT][RIGHT] -> Junction string
TABLE = json.load(open(r"pyframe\border\junctions.json", encoding="utf-8"))
DIRECTION_ORDER = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


class Junction(Cell):
    """A `Cell` that is a part of a border of a `Frame`."""

    def __init__(
        self,
        dct: JunctionDict,
        style: str,
        color: Color = Colors.DEFAULT,
    ) -> None:
        self._directions = dct
        self.style = style
        self.color = color

        self._update_value()

    def _update_value(self):
        def get_directional_thickness(direction):
            result = self._directions.get(direction)
            if result:
                return result.value
            else:
                return "none"

        junction: str | dict[str, str] = TABLE[
            get_directional_thickness(DIRECTION_ORDER[0])
        ][get_directional_thickness(DIRECTION_ORDER[1])][
            get_directional_thickness(DIRECTION_ORDER[2])
        ][
            get_directional_thickness(DIRECTION_ORDER[3])
        ]

        # Style
        if isinstance(junction, dict):
            junction = junction[self.style or "default"]

        self.value = junction

    def __repr__(self):
        return self.value

    def __add__(self, junction: Self) -> Self:
        return type(self)(
            self._directions | junction._directions,
            "default",
            junction.color,  # 'default'?
        )

    def __mul__(self, times: int) -> list[Self]:
        return [
            type(self)(self._directions, self.style, self.color) for _ in range(times)
        ]

    def __copy__(self):
        return type(self)(self._directions, self.style, self.color)

    @classmethod
    def from_string(cls, string: str):
        def get_path(nested_dict, value, pre=()) -> tuple[str, str, str, str, str]:
            for k, v in nested_dict.items():
                path = pre + (k,)
                if v == value:
                    return path
                elif hasattr(v, "items"):
                    p = get_path(v, value, path)
                    if p is not None:
                        return p

        *path, style = get_path(TABLE, string)

        dct = {}
        for i, thickness in enumerate(path):
            if thickness != "none":
                dct[DIRECTION_ORDER[i]] = Thickness.__getitem__(thickness.upper())

        return Junction(dct, style)

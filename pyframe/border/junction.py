import json
from typing import Self

from pyframe.colors import Color, Colors
from pyframe.grid import Cell
from pyframe.types_ import Direction, JunctionDict, Thickness

# table[UP][DOWN][LEFT][RIGHT]
table = json.load(open(r"pyframe\border\junctions.json", encoding="utf-8"))
direction_order = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


class Junction(Cell):
    """A Cell that is the borders of frames."""

    def __init__(
        self,
        dct: JunctionDict,
        style: str,
        color: Color = Colors.DEFAULT,
    ) -> None:
        self._directions = dct
        self.style = style
        self.color = color

    @property
    def value(self):
        def convert(direction):
            none = "none"
            result = self._directions.get(direction)
            if result:
                return result.value
            else:
                return none

        junction = table[convert(direction_order[0])][convert(direction_order[1])][
            convert(direction_order[2])
        ][convert(direction_order[3])]

        if isinstance(junction, dict):
            return junction[self.style or "default"]

        return junction

    def __repr__(self):
        return self.value

    def __add__(self, junction: Self) -> Self:
        return type(self)(
            self._directions | junction._directions, "default", junction.color
        )

    def __mul__(self, times: int) -> list[Self]:
        return [
            type(self)(self._directions, self.style, self.color) for _ in range(times)
        ]

    def __copy__(self):
        return type(self)(self._directions, self.style, self.color)

    @classmethod
    def from_string(cls, string: str):
        def get_path(nested_dict, value, pre=()):
            for k, v in nested_dict.items():
                path = pre + (k,)
                if v == value:  # found value
                    return path
                elif hasattr(v, "items"):  # v is a dict
                    p = get_path(v, value, path)  # recursive call
                    if p is not None:
                        return p

        path = get_path(table, string)

        dct = {}
        for i, thickness in enumerate(path):
            if i == 4:
                style = thickness
                return Junction(dct, style)
            if thickness != "none":
                dct[direction_order[i]] = Thickness.__getitem__(thickness.upper())
        return Junction(dct, "default")

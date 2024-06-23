import json

from pyframe.types_ import Direction, JunctionDict, Thickness

# table[UP][DOWN][LEFT][RIGHT]
table = json.load(open(r"pyframe\border\junctions.json", encoding="utf-8"))


# TODO separate style and dict
def get_junction(dct: JunctionDict, style: str) -> str:
    """Get a str junction from a dict of Directions and Thicknesses."""

    def convert(direction):
        none = "none"
        result = dct.get(direction)
        if result:
            return result.value
        else:
            return none

    junction = table[convert(Direction.UP)][convert(Direction.DOWN)][
        convert(Direction.LEFT)
    ][convert(Direction.RIGHT)]

    if isinstance(junction, dict):
        return junction[style or "default"]

    return junction

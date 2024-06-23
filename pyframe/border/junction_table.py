import json

from pyframe.types_ import Direction, JunctionDict, Thickness

# table[UP][DOWN][LEFT][RIGHT]
table = json.load(open(r"pyframe\border\junctions.json", encoding="utf-8"))


def get_junction(dct: JunctionDict) -> str:
    """Get a str junction from a dict of Directions and Thicknesses."""
    style = None
    if isinstance(dct, tuple):
        style = dct[1]
        dct = dct[0]

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
        return junction[style or 'default']

    return junction

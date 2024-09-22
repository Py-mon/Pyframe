from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __lt__(self, other):
        return self.value < other.value


class Alignment(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    MIDDLE = 2

    def align(self, string: str, width: int) -> str:
        if self == type(self).LEFT:
            return string.ljust(width)
        elif self == type(self).RIGHT:
            return string.rjust(width)
        elif self == type(self).CENTER or self == type(self).MIDDLE:
            return string.center(width)
        return ""


class TitleSide(Enum):
    TOP = 0
    BOTTOM = -1
    LEFT = 1
    RIGHT = 2


class Side(Enum):
    LEFT = 0
    RIGHT = -1


class Thickness(Enum):
    THIN = "thin"
    THICK = "thick"
    DOUBLE = "double"


JunctionDict = dict[Direction, Thickness]

from typing import Self


class Color:
    @classmethod
    def from_hex(cls, name: str, hex_code: str) -> Self:
        index = hex_code.lstrip("#")
        rgb = tuple(int(index[i : i + 2], 16) for i in (0, 2, 4))
        return cls(name, hex_code, rgb)

    @classmethod
    def from_rgb(cls, name: str, r: int, g: int, b: int) -> Self:
        rgb = r, g, b
        hex_ = "#" + hex(r)[2:] + hex(g)[2:] + hex(b)[2:]
        return cls(name, hex_, rgb)

    def __init__(self, name: str, hex: str, rgb: tuple[int, ...]):
        self._hex = hex
        self._rgb = rgb
        self.name = name

    @property
    def hex(self):
        return self._hex

    @property
    def rgb(self):
        return self._rgb

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]


class Colors:
    BLACK = Color.from_hex("BLACK", "#090300")
    DEFAULT = Color.from_hex("DEFAULT", "#d0d0d0")
    BLUE = Color.from_hex("BLUE", "#01A0E4")
    GRAY = Color.from_hex("GRAY", "#5C5855")
    CYAN = Color.from_hex("CYAN", "#B5E4F4")
    GREEN = Color.from_hex("GREEN", "#01A252")
    MAGENTA = Color.from_hex("MAGENTA", "#A16A94")
    RED = Color.from_hex("RED", "#DB2D20")
    WHITE = Color.from_hex("WHITE", "#F7F7F7")
    YELLOW = Color.from_hex("YELLOW", "#FDED02")

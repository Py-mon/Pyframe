'2024-05-23 05:16 PM  May, 23, Thursday'
'2023-04-23 07:22 PM  April, 23, Sunday'
'Entries: 42/50 (Modified Often)'

from enum import Enum


class CursorCode(Enum):
    """Codes for moving the cursor"""

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    MOVE = 4


class AnsiEscSeq:
    """ANSI escape sequence"""

    ESC = "\033"
    CSI = ESC + "["

    def __init__(self, code: str, *args: str | int) -> None:
        self.code = code
        self.args = ";".join([str(arg) for arg in args])
        self.seq = self.CSI + self.args + self.code

    def exec(self) -> None:
        """Execute the ANSI escape sequence"""
        print(self.seq, end="")

    def __repr__(self) -> str:
        return repr(self.seq)

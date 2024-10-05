# Dynamic Boxes

from pyframe.border.border_types import Borders
from pyframe.frame import Frame, Title

from pyframe.border.border_type import BorderType, Thickness
from pyframe.colors import Colors
from pyframe.types_ import Alignment, TitleSide

from pyframe.border.border_type import Thickness

print("\nCentered Top Title")
# TODO vertical padding and horizontal
frame = Frame.centered(
    "Lorem ipsum dolor sit amet,\n consectetur adipiscising elit. ",
    4,
    70,
    Borders.Thin.ROUND,
)
frame.add_title(
    Title(
        "Title",
        alignment=Alignment.LEFT,
        title_side=TitleSide.TOP,
    )
)
print(frame)

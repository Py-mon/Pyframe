# Dynamic Boxes

from pyframe.border.border_types import Borders
from pyframe.frame import Frame, Title

from pyframe.border.border_type import BorderType, Thickness
from pyframe.colors import Colors
from pyframe.types_ import Alignment, TitleSide

from pyframe.border.border_type import Thickness

print("\nCentered Top Title")
frame = Frame.empty_box(5, 13, Borders.Thin.ROUND)
frame.add_title(
    Title(
        "Title",
        alignment=Alignment.CENTER,
        title_side=TitleSide.TOP,
    )
)
print(frame)

print("\nCentered Bottom Title")
frame = Frame.empty_box(5, 13, Borders.Thin.ROUND)
frame.add_title(
    Title(
        "Title",
        alignment=Alignment.CENTER,
        title_side=TitleSide.BOTTOM,
    )
)
print(frame)

print("\nRight Top Title")
frame = Frame.empty_box(5, 13, Borders.Thin.ROUND)
frame.add_title(
    Title(
        "Title",
        color=Colors.BLUE,
        alignment=Alignment.RIGHT,
        title_side=TitleSide.TOP,
        margin=1,
    )
)
print(frame)

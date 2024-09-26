# Dynamic Boxes

from pyframe.border.border_types import BorderTypes
from pyframe.frame import Frame, Title

from pyframe.border.border_type import BorderType, Thickness
from pyframe.colors import Colors
from pyframe.types_ import Alignment, TitleSide

from pyframe.border.border_type import Thickness


f1 = Frame.box(5, 13, BorderTypes.OverlapClassic.DASHED)
f1.add_title(
    Title(
        "Title",
        color=Colors.BLUE,
        alignment=Alignment.CENTER,
        title_side=TitleSide.TOP,
    )
)
print(f1)
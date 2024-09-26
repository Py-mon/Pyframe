# Dynamic Boxes

from pyframe.border.border_types import BorderTypes
from pyframe.frame import Frame, Title

from pyframe.border.border_type import BorderType, Thickness
from pyframe.colors import Colors
from pyframe.types_ import Alignment, TitleSide

from pyframe.border.border_type import Thickness


# f1 = Frame.box(12, 12, BorderTypes.OverlapClassic.DOUBLE)
# f1.add_title(
#     Title(
#         "hello",
#         color=Colors.BLUE,
#         alignment=Alignment.RIGHT,
#         title_side=TitleSide.BOTTOM,
#     )
# )
# f1.color_border(Colors.RED)
# print(f1)

# f2 = Frame.box(4, 9, BorderTypes.Thin.SHARP)
# print(f2)

# f3 = Frame.box(
#     4,
#     9,
#     BorderType.thickness(
#         top=Thickness.THIN,
#         bottom=Thickness.THIN,
#         left=Thickness.DOUBLE,
#         right=Thickness.THICK,
#     ),
# )
# print(f3)
# f4 = Frame.box(4, 9, BorderTypes.DOUBLE)
# print(f4)

# f5 = Frame.centered("abcdef\nghij", 6, 12, BorderTypes.THICK)
# f5.color_border(Colors.RED)
# print(f5)

# f = Frame.box(15, 30, BorderTypes.Thin.ROUND)
# f.add_frame(f1, (2, 12))
# # f.add_frame(f2, (0, 12))
# # f.add_frame(f4, (2, 14))
# # f.add_frame(f3, (6, 12))
# # f.add_frame(f5, (9, 15))
# print(f.colored_str())
# print(f[(2, 2)].color.name)
# # f = Frame.box(6, 10)
# # f.add_title(Title("SO", Alignment.CENTER, Colors.BLUE))
# # f.add_frame(Frame.box(4, 5), (1, 0))
# # # f.color_border(Colors.RED)
# # print(f)
# # print(f.colored_str())

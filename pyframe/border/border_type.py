from copy import copy
from dataclasses import dataclass
from typing import Optional, Self

from pyframe.grid import Cell, Junction
from pyframe.types_ import Direction, JunctionDict, Thickness


@dataclass
class BorderType:
    top_right: JunctionDict | str
    top_left: JunctionDict | str
    bottom_right: JunctionDict | str
    bottom_left: JunctionDict | str

    top_horizontal: JunctionDict | str
    left_vertical: JunctionDict | str
    bottom_horizontal: JunctionDict | str
    right_vertical: JunctionDict | str

    @classmethod
    def thickness(
        cls,
        top: Optional[Thickness] = None,
        bottom: Optional[Thickness] = None,
        left: Optional[Thickness] = None,
        right: Optional[Thickness] = None,
        top_style: str = "default",
        left_style: str = "default",
        bottom_style: str = "default",
        right_style: str = "default",
        top_right_style: str = "default",
        top_left_style: str = "default",
        bottom_right_style: str = "default",
        bottom_left_style: str = "default",
        *,
        thickness: Optional[Thickness] = None,
        style: Optional[str] = None,
        corner_style: Optional[str] = None,
    ):
        if style:
            if top_style == "default":
                top_style = style
            if bottom_style == "default":
                bottom_style = style
            if left_style == "default":
                left_style = style
            if right_style == "default":
                right_style = style
        if corner_style:
            if top_right_style == "default":
                top_right_style = corner_style
            if bottom_left_style == "default":
                bottom_left_style = corner_style
            if top_left_style == "default":
                top_left_style = corner_style
            if bottom_right_style == "default":
                bottom_right_style = corner_style

        if thickness:
            top = thickness
            left = thickness
            right = thickness
            bottom = thickness
        elif top == None or left == None or right == None or bottom == None:
            raise
        
        # Patterns?
        return cls(
            top_right=({Direction.DOWN: left, Direction.RIGHT: top}, top_right_style),
            top_left=({Direction.DOWN: right, Direction.LEFT: top}, top_left_style),
            bottom_right=(
                {Direction.UP: left, Direction.RIGHT: bottom},
                bottom_right_style,
            ),
            bottom_left=(
                {Direction.UP: right, Direction.LEFT: bottom},
                bottom_left_style,
            ),
            top_horizontal=({Direction.LEFT: top, Direction.RIGHT: top}, top_style),
            left_vertical=({Direction.UP: left, Direction.DOWN: left}, left_style),
            bottom_horizontal=(
                {Direction.LEFT: bottom, Direction.RIGHT: bottom},
                bottom_style,
            ),
            right_vertical=({Direction.UP: right, Direction.DOWN: right}, right_style),
        )

    # @classmethod
    # def uniform_thickness(
    #     cls,
    #     thickness: Thickness,
    #     top_style: str = "default",
    #     left_style: str = "default",
    #     bottom_style: str = "default",
    #     right_style: str = "default",
    #     *,
    #     style: Optional[str] = None,
    #     corner_style: Optional[str] = None,
    # ):
    #     return cls(
    #         top_right={Direction.DOWN: thickness, Direction.RIGHT: thickness},
    #         top_left={Direction.DOWN: thickness, Direction.LEFT: thickness},
    #         bottom_right={Direction.UP: thickness, Direction.RIGHT: thickness},
    #         bottom_left={Direction.UP: thickness, Direction.LEFT: thickness},
    #         top_horizontal=(
    #             {Direction.LEFT: thickness, Direction.RIGHT: thickness},
    #             style,
    #         ),
    #         left_vertical=({Direction.UP: thickness, Direction.DOWN: thickness}, style),
    #         bottom_horizontal=(
    #             {Direction.LEFT: thickness, Direction.RIGHT: thickness},
    #             style,
    #         ),
    #         right_vertical=(
    #             {Direction.UP: thickness, Direction.DOWN: thickness},
    #             style,
    #         ),
    #     )

    # @classmethod
    # def y(
    #     cls,
    #     thickness: Thickness,
    #     # TODO put dashes in junctions.json and classic etc
    # ):
    #     #  x.top_right |= {"smoothness": smoothness}  # type: ignore
    #     # x.top_left |= {"smoothness": smoothness}  # type: ignore
    #     # x.bottom_right |= {"smoothness": smoothness}  # type: ignore
    #     # x.bottom_left |= {"smoothness": smoothness}  # type: ignore
    #     return cls(
    #         top_right={Direction.DOWN: thickness, Direction.RIGHT: thickness},
    #         top_left={Direction.DOWN: thickness, Direction.LEFT: thickness},
    #         bottom_right={Direction.UP: thickness, Direction.RIGHT: thickness},
    #         bottom_left={Direction.UP: thickness, Direction.LEFT: thickness},
    #         top_horizontal={Direction.LEFT: thickness, Direction.RIGHT: thickness},
    #         left_vertical={Direction.UP: thickness, Direction.DOWN: thickness},
    #         bottom_horizontal={Direction.LEFT: thickness, Direction.RIGHT: thickness},
    #         right_vertical={Direction.UP: thickness, Direction.DOWN: thickness},
    #     )

    def set_vertical(self, vertical: JunctionDict | str):
        self.left_vertical = vertical
        self.right_vertical = vertical

    def set_horizontal(self, horizontal: JunctionDict | str):
        self.left_horizontal = horizontal
        self.right_horizontal = horizontal

    def __repr__(self) -> str:
        return (
            f"{self.top_right}{str(self.top_horizontal)}{self.top_left}\n"
            f"{self.left_vertical}    {self.right_vertical}\n"
            f"{self.bottom_right}{str(self.bottom_horizontal)}{self.bottom_left}\n"
        )


class Border:
    def __init__(self, border_type: BorderType):
        def create_instance(junction):
            
            if isinstance(junction, tuple):
                return Junction(junction)
            # if len(junction[0]) > 1:
            #     return [Cell(x) for x in junction]
            return Cell(junction)

        self.top_right = create_instance(border_type.top_right)
        self.top_left = create_instance(border_type.top_left)
        self.bottom_right = create_instance(border_type.bottom_right)
        self.bottom_left = create_instance(border_type.bottom_left)

        self.top_horizontal = create_instance(border_type.top_horizontal)
        self.left_vertical = create_instance(border_type.left_vertical)
        self.bottom_horizontal = create_instance(border_type.bottom_horizontal)
        self.right_vertical = create_instance(border_type.right_vertical)


class BorderTypes:
    """
    ```
    Thin:
        ╭───╮ # TODO sharp edges
        │   │
        ╰───╯
    Thick:
        ┏━━━┓
        ┃   ┃
        ┗━━━┛
    Double:
        ╔═══╗
        ║   ║
        ╚═══╝
    """
    THIN = BorderType.thickness(thickness=Thickness.THIN, corner_style='round')
    THICK = BorderType.thickness(thickness=Thickness.THICK)
    DOUBLE = BorderType.thickness(thickness=Thickness.DOUBLE)
    # THIN = BorderType.uniform_thickness(Thickness.THIN)
    # THICK = BorderType.uniform_thickness(Thickness.THICK)
    # DOUBLE = BorderType.uniform_thickness(Thickness.DOUBLE)

    TRIPLE_DASHED = copy(THIN)
    TRIPLE_DASHED.set_horizontal("┄")
    TRIPLE_DASHED.set_vertical("┆")

    QUAD_DASHED = copy(THIN)
    QUAD_DASHED.set_horizontal("┈")
    QUAD_DASHED.set_vertical("┊")

    DUO_DASHED = copy(THIN)
    DUO_DASHED.set_horizontal("╌")
    DUO_DASHED.set_vertical("╎")

    THICK_TRIPLE_DASHED = copy(THICK)
    THICK_TRIPLE_DASHED.set_horizontal("┅")
    THICK_TRIPLE_DASHED.set_vertical("┇")

    THICK_QUAD_DASHED = copy(THICK)
    THICK_QUAD_DASHED.set_horizontal("┉")
    THICK_QUAD_DASHED.set_vertical("┋")

    THICK_DUO_DASHED = copy(THICK)
    THICK_DUO_DASHED.set_horizontal("╍")
    THICK_DUO_DASHED.set_vertical("╏")

    CASTLE = copy(THIN)
    CASTLE.top_horizontal = "─⍽"

    class Classic:
        PLUS = BorderType(
            top_right="+",
            top_left="+",
            bottom_right="+",
            bottom_left="+",
            top_horizontal="-",
            left_vertical="|",
            bottom_horizontal="-",
            right_vertical="|",
        )
        UNDERSCORE = BorderType(
            top_right=" ",
            top_left=" ",
            bottom_right="|",
            bottom_left="|",
            top_horizontal="_",
            left_vertical=PLUS.left_vertical,
            bottom_horizontal="_",
            right_vertical=PLUS.right_vertical,
        )

# print(BorderTypes.THIN)
# ↕xx
# xxx

# TODO vector2d, ascii art, more borders
# ― ⍽ ⎸ ⎹ ␣ ─ ━ │ ┃
# ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋╌ ╍ ╎ ╏
# ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↚ ↛ ↜ ↝ ↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧ ↨ ↩ ↪ ↫ ↬ ↭ ↮ ↯ ↰ ↱ ↲ ↳ ↴ ↵ ↶ ↷ ↸ ↹ ↺ ↻ ⇄ ⇅ ⇆ ⇇ ⇈ ⇉ ⇊ ⇍ ⇎ ⇏ ⇐ ⇑ ⇒ ⇓ ⇔ ⇕ ⇖ ⇗ ⇘ ⇙ ⇚ ⇛ ⇜ ⇝ ⇞ ⇟ ⇠ ⇡ ⇢ ⇣ ⇤ ⇥ ⇦ ⇧ ⇨ ⇩ ⇪
# ☐ ☑ ☒ ⫍ ⫎ ⮹ ⮽ ⺆ ⼌ ⼐ ⼕
# ↼ ↽ ↾ ↿ ⇀ ⇁ ⇂ ⇃ ⇋ ⇌
# ╱ ╲ ╳

# DOUBLE and THICK aren't compatible
# THIN only has rounded corners

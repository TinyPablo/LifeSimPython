from enum import Enum


class SelectionCondition(Enum):
    CENTER_ZONE = "center_zone"
    BOTTOM_RIGHT_SQUARE = "bottom_right_square"
    CORNERS = "corners"
    RIGHT_EDGE = "right_edge"
    LEFT_EDGE = "left_edge"
    UPPER_LEFT_SQUARE = "upper_left_square"
    ALMOST_P = "almost_p"
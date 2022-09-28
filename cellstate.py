from enum import Enum, auto


class CellState(Enum):
    CLOSED = auto()
    FLAGGED = auto()
    OPEN = auto()
    LOST_GAME = auto()

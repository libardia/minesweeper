from enum import Enum, auto


class CellState(Enum):
    CLOSED = auto()
    FLAGGED = auto()
    PRESSED = auto()
    OPEN = auto()
    LOST_GAME = auto()

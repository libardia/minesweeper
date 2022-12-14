import pygame as pg
from go import GameObject
from cellstate import CellState
import static


class goCell(GameObject):
    def __init__(self, grid) -> None:
        super().__init__()
        self.goGrid = grid
        self.state = CellState.CLOSED
        self.changeState(CellState.CLOSED)
        self.near = 0
        self.nearCells: list[goCell] = []
        self.mine = False
        self.pressed = False
        self.gx = 0
        self.gy = 0

    def reveal(self):
        if self.state == CellState.CLOSED:
            if self.mine:
                self.changeState(CellState.LOST_GAME)
                static.game.playing = False
                static.game.wonGame = False
                static.game.finalize = True
            elif self.state != CellState.OPEN:
                self.changeState(CellState.OPEN)
                self.goGrid.hidden -= 1
                if self.near == 0:
                    for c in self.nearCells:
                        c.reveal()

    def press(self):
        if self.state == CellState.CLOSED:
            self.pressed = True
            self.img = static.image.pressed

    def unpress(self):
        self.pressed = False
        if self.state == CellState.CLOSED:
            self.img = static.image.closed

    def pressAround(self):
        for cell in self.nearCells:
            cell.press()

    def surroundingFlagged(self):
        result = 0
        for cell in self.nearCells:
            if cell.state == CellState.FLAGGED:
                result += 1
        return result

    def surroundingNonOpen(self):
        result = 0
        for cell in self.nearCells:
            if cell.state != CellState.OPEN:
                result += 1
        return result

    def changeState(self, state):
        prev = self.state
        self.state = state
        match state:
            case CellState.CLOSED:
                self.img = static.image.closed
            case CellState.FLAGGED:
                self.img = static.image.flagged
            case CellState.OPEN:
                if self.mine:
                    # If this cell had a bomb, show it
                    # (this would happen at the end of the game, win or lose)
                    self.img = static.image.open_mine
                else:
                    if prev == CellState.FLAGGED:
                        # If this cell didn't have a bomb but it was flagged, show
                        # the image meaning there wasn't actually a bomb here
                        # (this would happen at the end of the game on a loss)
                        self.img = static.image.open_mine_crossed
                    else:
                        # If this cell didn't have a bomb and wasn't flagged, show
                        # the number of surrounding mines (normal open)
                        self.img = static.image.open[self.near]
            case CellState.LOST_GAME:
                self.img = static.image.open_mine_red

    def handleEvents(self, event, gridPosition: tuple[int, int], dt) -> None:
        if gridPosition == (self.gx, self.gy):
            if event.type == pg.MOUSEBUTTONUP:
                match event.button:
                    case pg.BUTTON_LEFT:
                        match self.state:
                            case CellState.CLOSED:
                                self.reveal()
                            case CellState.OPEN:
                                if self.surroundingFlagged() == self.near:
                                    for cell in self.nearCells:
                                        cell.reveal()
            elif (event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT) or (event.type == pg.MOUSEMOTION and event.buttons[0] == 1):
                match self.state:
                    case CellState.OPEN:
                        self.pressAround()
                    case CellState.CLOSED:
                        self.press()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_RIGHT:
                    match self.state:
                        case CellState.CLOSED:
                            self.changeState(CellState.FLAGGED)
                            self.goGrid.flagged += 1
                        case CellState.FLAGGED:
                            self.changeState(CellState.CLOSED)
                            self.goGrid.flagged -= 1
                        case CellState.OPEN:
                            if self.surroundingNonOpen() == self.near:
                                for cell in self.nearCells:
                                    if cell.state == CellState.CLOSED:
                                        cell.changeState(
                                            CellState.FLAGGED)
                                        self.goGrid.flagged += 1

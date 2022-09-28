import pygame as pg
from go import GameObject
from cellstate import CellState
import static
import const


class goCell(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.state = CellState.CLOSED
        self.changeState(CellState.CLOSED)
        self.neighbors = 0
        self.bomb = False
        static.game.registerEvent(self, pg.MOUSEBUTTONDOWN)

    def reveal(self):
        if self.bomb:
            self.changeState(CellState.LOST_GAME)
        else:
            self.changeState(CellState.OPEN)

    def changeState(self, state):
        prev = self.state
        self.state = state
        match state:
            case CellState.CLOSED:
                self.img = static.image.closed
            case CellState.FLAGGED:
                self.img = static.image.flagged
            case CellState.PRESSED:
                self.img = static.image.pressed
            case CellState.OPEN:
                if self.bomb:
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
                        self.img = static.image.open[self.neighbors]
            case CellState.LOST_GAME:
                self.img = static.image.open_mine_red

    def handleEvents(self, event, dt) -> None:
        if pg.Rect(self.x, self.y, const.CELL_PX_WIDTH, const.CELL_PX_HEIGHT).collidepoint(event.pos):
            if event.button == pg.BUTTON_LEFT:
                if self.state == CellState.CLOSED:
                    self.changeState(CellState.OPEN)
                elif self.state == CellState.OPEN:
                    self.changeState(CellState.CLOSED)
            elif event.button == pg.BUTTON_RIGHT:
                if self.state == CellState.CLOSED:
                    self.changeState(CellState.FLAGGED)
                elif self.state == CellState.FLAGGED:
                    self.changeState(CellState.CLOSED)

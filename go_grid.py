import pygame as pg
import random
from cellstate import CellState
from go import GameObject
from go_cell import goCell
import const
import static


class goGrid(GameObject):
    def __init__(self, width, height, mines) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.mines = mines
        self.flagged = 0
        self.hidden = width * height
        self.firstClick = True
        self.grid: list[list[goCell]] = []

    def onAdd(self):
        static.game.registerEvent(self, pg.MOUSEBUTTONDOWN)
        static.game.registerEvent(self, pg.MOUSEBUTTONUP)
        static.game.registerEvent(self, pg.MOUSEMOTION)
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                c = goCell(self)
                c.gx = x
                c.gy = y
                c.onAdd()
                self.grid[y].append(c)

    def positionInGrid(self, pos: tuple[int, int]):
        return pos[0] >= 0 and pos[0] < self.width and pos[1] >= 0 and pos[1] < self.height

    def placeMines(self, clickPos: tuple[int, int]):
        # Positions that can't have mines
        safe = [(clickPos[0]+dx, clickPos[1]+dy)
                for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        # Place mines
        for _ in range(self.mines):
            # Keep trying if we try to put a mine where there already is one
            retry = True
            while retry:
                mx = random.randint(0, self.width-1)
                my = random.randint(0, self.height-1)
                if not self.grid[my][mx].mine and (mx, my) not in safe:
                    self.grid[my][mx].mine = True
                    # We placed a mine, so we're done trying
                    retry = False
        # Count mines around cells, and also give each cell a list of their
        # neighbors
        for y in range(self.height):
            for x in range(self.width):
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if (dx, dy) != (0, 0):
                            if self.positionInGrid((x+dx, y+dy)):
                                self.grid[y][x].nearCells.append(
                                    self.grid[y+dy][x+dx])
                                if self.grid[y+dy][x+dx].mine:
                                    self.grid[y][x].near += 1

    def draw(self, dt):
        for row in self.grid:
            for go in row:
                go.draw(dt)

    def update(self, dt):
        # Win if hidden = mines (but only do this once)
        if static.game.playing and self.hidden == self.mines:
            # If not all the hidden cells are flagged,
            # flag them all
            if self.flagged != self.mines:
                for x in range(self.width):
                    for y in range(self.height):
                        cell = self.grid[y][x]
                        if cell.state == CellState.CLOSED:
                            cell.changeState(CellState.FLAGGED)
                            self.flagged += 1
            static.game.playing = False
            static.game.wonGame = True
            static.game.finalize = True
            static.game.unregisterEvent(self.id)
            static.game.unregisterEvent(self.id)
            static.game.unregisterEvent(self.id)
        for x in range(self.width):
            for y in range(self.height):
                c = self.grid[y][x]
                c.x = self.x + (x * const.CELL_PX_WIDTH)
                c.y = self.y + (y * const.CELL_PX_HEIGHT)

        if not static.game.playing and not static.game.wonGame and static.game.finalize:
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.grid[y][x]
                    if cell.state != CellState.LOST_GAME:
                        cell.changeState(CellState.OPEN)

    def handleEvents(self, event, dt):
        if (event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT) or (event.type == pg.MOUSEMOTION and event.buttons[0] == 1):
            for y in range(self.height):
                for x in range(self.width):
                    self.grid[y][x].unpress()
        gx = int((event.pos[0] - self.x) // const.CELL_PX_WIDTH)
        gy = int((event.pos[1] - self.y) // const.CELL_PX_HEIGHT)
        if event.type == pg.MOUSEBUTTONUP and self.firstClick:
            self.placeMines((gx, gy))
            self.firstClick = False
        for row in self.grid:
            for go in row:
                go.handleEvents(event, (gx, gy), dt)

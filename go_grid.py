import pygame as pg
import random
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
        self.firstClick = True
        self.grid: list[list[goCell]] = []
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                c = goCell()
                c.gx = x
                c.x = self.x + (x * const.CELL_PX_WIDTH)
                c.gy = y
                c.y = self.y + (y * const.CELL_PX_HEIGHT)
                self.grid[y].append(c)
        static.game.registerEvent(self, pg.MOUSEBUTTONDOWN)
        static.game.registerEvent(self, pg.MOUSEBUTTONUP)

    def positionInGrid(self, pos: tuple[int, int]):
        return pos[0] >= 0 and pos[0] < self.width and pos[1] >= 0 and pos[1] < self.height

    def placeMines(self, clickPos: tuple[int, int]):
        # Place mines
        for _ in range(self.mines):
            # Keep trying if we try to put a mine where there already is one
            retry = True
            while retry:
                mx = random.randint(0, self.width-1)
                my = random.randint(0, self.height-1)
                if not self.grid[my][mx].mine and (mx, my) != clickPos:
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

    def handleEvents(self, event, dt):
        gx = (event.pos[0] - self.x) // const.CELL_PX_WIDTH
        gy = (event.pos[1] - self.y) // const.CELL_PX_HEIGHT
        if self.firstClick:
            self.placeMines((gx, gy))
            self.firstClick = False
        for row in self.grid:
            for go in row:
                go.handleEvents(event, (gx, gy), dt)

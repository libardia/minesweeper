from go import GameObject
from go_cell import goCell
import const


class goGrid(GameObject):
    def __init__(self, width, height) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.grid = []
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                c = goCell()
                c.x = x * const.CELL_PX_WIDTH
                c.y = y * const.CELL_PX_HEIGHT
                self.grid[y].append(c)

    def draw(self, dt):
        for row in self.grid:
            for go in row:
                go.draw(dt)

    def handleEvents(self, event, dt):
        for row in self.grid:
            for go in row:
                go.handleEvents(event, dt)

from collections import defaultdict
import pygame as pg
import static
import const
import img
from go import GameObject
from go_grid import goGrid
from go_ui import goUI


class Game:
    def __init__(self) -> None:
        pg.init()
        w = const.GRID_WIDTH * const.CELL_PX_WIDTH + 2 * const.WINDOW_PADDING
        h = const.GRID_HEIGHT * const.CELL_PX_HEIGHT + \
            2 * const.WINDOW_PADDING + const.UI_SPACE
        self.setupScreen(w, h)
        pg.display.set_caption('Minesweeper')
        pg.display.set_icon(pg.image.load(const.IMAGE_PATH + 'cf.png'))
        self.quit = False
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(const.FPS)
        # [depth, [id, go]]
        self.gameObjects: dict[int, dict[int, GameObject]] = {0: {}}
        self.depthBounds = [0, 0]
        # [event type, [id, go]]
        self.eventQueues: dict[pg.event._EventTypes,
                               dict[int, GameObject]] = {}
        static.image = img.Images()

    def initialize(self):
        static.image.loadMS()
        self.lost = False
        grid = goGrid(const.GRID_WIDTH, const.GRID_HEIGHT, const.GRID_MINES)
        grid.x = const.WINDOW_PADDING
        grid.y = const.WINDOW_PADDING + const.UI_SPACE
        self.add(grid)
        self.add(goUI())

    def setupScreen(self, width, height):
        self.screen = pg.display.set_mode(
            (width, height), flags=pg.DOUBLEBUF, vsync=1)

    def add(self, go: GameObject, depth: int = 0):
        if depth < self.depthBounds[0]:
            self.depthBounds[0] = depth
        if depth > self.depthBounds[1]:
            self.depthBounds[1] = depth
        if depth not in self.depthBounds:
            self.depthBounds[depth] = {}
        self.gameObjects[depth][go.id] = go
        go.onAdd()

    def findGameObject(self, id):
        for depth, gos in self.gameObjects.items():
            if id in gos:
                return gos[id]

    def findGameObjectByType(self, type):
        for depth, gos in self.gameObjects.items():
            for id, go in gos.items():
                if isinstance(go, type):
                    return go

    def remove(self, id: int):
        for depth, gos in self.gameObjects.items():
            if id in gos:
                gos[id].onRemove()
                gos.pop(id)
                break
        for evtype, gos in self.eventQueues.items():
            if id in gos:
                gos.pop(id)
                break
        # Remove empty indexes
        self.gameObjects = {depth: gos for depth,
                            gos in self.gameObjects.items() if len(gos) > 0}
        self.eventQueues = {evtype: gos for evtype,
                            gos in self.eventQueues.items() if len(gos) > 0}

    def remove(self, go: GameObject):
        self.remove(go.id)

    def registerEvent(self, go: GameObject, type):
        if type not in self.eventQueues:
            self.eventQueues[type] = {}
        self.eventQueues[type][go.id] = go

    def validateDepth(self):
        keys = tuple(self.gameObjects.keys())
        self.depthBounds = [min(keys, default=0), max(keys, default=0)]

    def draw(self) -> None:
        self.screen.fill(const.BG_COLOR)

        # Draw from lowest to highest depth
        for depth in range(self.depthBounds[0], self.depthBounds[1] + 1):
            if depth in self.gameObjects:
                for id, go in self.gameObjects[depth].items():
                    go.draw(self.dt)

        pg.display.flip()

    def handleEvents(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type in self.eventQueues:
                for id, go in self.eventQueues[event.type].items():
                    go.handleEvents(event, self.dt)

    def update(self) -> None:
        for depth, gos in self.gameObjects.items():
            for id, go in gos.items():
                go.update(self.dt)

    def main(self) -> None:
        while not self.quit:
            self.dt = self.clock.tick(const.FPS)
            self.update()
            self.draw()
            self.handleEvents()


if __name__ == "__main__":
    static.game = Game()
    static.game.initialize()
    static.game.main()
    pg.display.quit()
    pg.quit()
    print('Quit gracefully.')

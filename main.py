import pygame as pg
import static
import const
import img
import fnt
import cfg
from go import GameObject
from go_grid import goGrid
from go_mineui import goMineUI
from go_resultui import goResultUI
from go_resethandler import goResetHandler


class Game:
    def __init__(self) -> None:
        pg.init()

        pg.display.set_caption('Minesweeper')
        pg.display.set_icon(pg.image.load(const.IMAGE_PATH + 'cf.png'))
        self.quit = False
        self.clock = pg.time.Clock()
        static.image = img.Images()
        static.font = fnt.Fonts()
        static.config = cfg.ConfigHolder()
        self.dt = self.clock.tick(const.FPS)

    def initialize(self):
        # [depth, [id, go]]
        self.gameObjects: dict[int, dict[int, GameObject]] = {0: {}}
        self.depthBounds = [0, 0]
        # [event type, [id, go]]
        self.eventQueues: dict[pg.event._EventTypes,
                               dict[int, GameObject]] = {}
        # Whether the game is currently going
        self.playing = True
        # Outcome of the game; true is win, false is loss
        self.wonGame = True
        # We should finalize things at the end of the game (used on loss to open all the remaining cells)
        self.finalize = False
        gridWidth = static.config.getGridWidth()
        gridHeight = static.config.getGridHeight()
        numMines = static.config.getNumMines()
        grid = goGrid(gridWidth, gridHeight, numMines)
        screenWidth = gridWidth * const.CELL_PX_WIDTH + 2 * const.WINDOW_PADDING
        screenHeight = gridHeight * const.CELL_PX_HEIGHT + \
            2 * const.WINDOW_PADDING + const.UI_SPACE
        self.setupScreen(screenWidth, screenHeight)
        grid.x = const.WINDOW_PADDING
        grid.y = const.WINDOW_PADDING + const.UI_SPACE
        self.add(grid)
        self.add(goMineUI())
        self.add(goResultUI())
        self.add(goResetHandler())

    def deinitialize(self):
        static.config.save()

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

    def registerEvent(self, go: GameObject, type):
        if type not in self.eventQueues:
            self.eventQueues[type] = {}
        self.eventQueues[type][go.id] = go

    def unregisterEvent(self, id: int):
        for etype, gos in self.eventQueues.items():
            if id in gos:
                gos.pop(id)
                break

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
        # Turn finalize off after updating everything else; this is so this flag is only active for one frame
        if self.finalize:
            self.finalize = False

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
    static.game.deinitialize()
    pg.display.quit()
    pg.quit()
    print('Quit gracefully.')

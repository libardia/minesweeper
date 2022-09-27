from collections import defaultdict
import pygame as pg
import static
import const
import util
from go import GameObject


class Game:
    def __init__(self) -> None:
        pg.init()
        self.quit = False
        self.screen = pg.display.set_mode(
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        # [depth, [id, go]]
        self.gameObjects: dict[int, dict[int, GameObject]] = {0: {}}
        self.depthBounds = [0, 0]
        # [event type, [id, go]]
        self.eventQueues: dict[pg.event._EventTypes,
                               dict[int, GameObject]] = {}

    def add(self, go: GameObject, depth: int):
        if depth < self.depthBounds[0]:
            self.depthBounds[0] = depth
        if depth > self.depthBounds[1]:
            self.depthBounds[1] = depth
        if depth not in self.depthBounds:
            self.depthBounds[depth] = {}
        self.gameObjects[depth][go.id] = go

    def remove(self, go: GameObject):
        for k, v in self.gameObjects.items():
            v.pop(go.id, None)
        self.gameObjects = {k: v for k, v in self.gameObjects if len(v) > 0}
        for k, v in self.eventQueues.items():
            v.pop(go.id, None)
        self.eventQueues = {k: v for k, v in self.eventQueues if len(v) > 0}

    def registerEvent(self, go: GameObject, type: pg.event._EventTypes):
        if type not in self.eventQueues:
            self.eventQueues[type] = {}
        self.eventQueues[type][go.id] = go

    def validateDepth(self):
        keys = tuple(self.gameObjects.keys())
        self.depthBounds = [min(keys, default=0), max(keys, default=0)]

    def draw(self) -> None:
        self.screen.fill(const.BG_COLOR)

        # Draw from lowest to highest depth
        for i in range(self.depthBounds[0], self.depthBounds[1] + 1):
            if i in self.gameObjects:
                for k, v in self.gameObjects[i].items():
                    v.draw()

        pg.display.flip()

    def handleEvents(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

    def update(self) -> None:
        pass

    def main(self) -> None:
        while not self.quit:
            self.update()
            self.draw()
            self.handleEvents()


if __name__ == "__main__":
    static.game = Game()
    static.game.main()
    print('Quit gracefully.')

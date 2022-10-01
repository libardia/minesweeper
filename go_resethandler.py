import pygame as pg
from go import GameObject
import static
from go_grid import goGrid


class goResetHandler(GameObject):
    def __init__(self) -> None:
        super().__init__()

    def onAdd(self):
        static.game.registerEvent(self, pg.KEYDOWN)
        self.goGrid = static.game.findGameObjectByType(goGrid)

    def handleEvents(self, event, dt):
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            static.game.initialize()

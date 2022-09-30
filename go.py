import pygame as pg
import static
import util


class GameObject:
    def __init__(self) -> None:
        self.id = util.getuuid()
        self.img = None
        self.x = 0.0
        self.y = 0.0

    # Placeholder to be overridden
    def onAdd(self):
        pass

    # Placeholder to be overridden
    def onRemove(self):
        pass

    # Can be overridden
    def draw(self, dt) -> None:
        if self.img is not None:
            static.game.screen.blit(self.img, (self.x, self.y))

    # Placeholder to be overridden
    def update(self, dt) -> None:
        pass

    # Placeholder to be overridden
    def handleEvents(self, event, dt) -> None:
        pass

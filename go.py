import pygame as pg
import static
import util


class GameObject:
    def __init__(self) -> None:
        self.id = util.getuuid()
        self.x = 0.0
        self.y = 0.0

    # Placeholder for fake polymorphism
    def draw(self, dt) -> None:
        pass

    # Placeholder for fake polymorphism
    def update(self, dt) -> None:
        pass

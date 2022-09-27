import pygame as pg
import static
import util


class GameObject:
    def __init__(self) -> None:
        self.id = util.getuuid()

    # Placeholder for fake polymorphism
    def draw(self) -> None:
        pass

    # Placeholder for fake polymorphism
    def update(self) -> None:
        pass

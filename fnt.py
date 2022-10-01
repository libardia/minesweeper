import pygame as pg
import const


class Fonts():
    def __init__(self) -> None:
        self.consolab32 = self.loadFont('consolab.ttf', 32)

    def loadFont(self, filename, size):
        return pg.font.Font(const.FONT_PATH + filename, size)

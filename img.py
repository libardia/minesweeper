import pygame as pg
import const


class Images():
    def __init__(self) -> None:
        self.closed = self.loadImage('c.png')
        self.flagged = self.loadImage('cf.png')
        self.pressed = self.loadImage('ch.png')
        self.open = [self.loadImage(f'o{i}.png') for i in range(9)]
        self.open_mine = self.loadImage('om.png')
        self.open_mine_crossed = self.loadImage('omc.png')
        self.open_mine_red = self.loadImage('omr.png')

    def loadImage(self, filename):
        return pg.image.load(const.IMAGE_PATH + filename)

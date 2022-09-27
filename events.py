import pygame as pg
import static

class EventHandler():
    def handleEvent(self, event: pg.event):
        match event.type:
            case pg.QUIT:
                static.game.quit = True

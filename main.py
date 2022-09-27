import pygame as pg
import static, const
from events import EventHandler
from go import GameObject

class Game:
    def __init__(self) -> None:
        pg.init()
        self.quit = False
        self.screen = pg.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.events = EventHandler()
        self.eventQueues: dict[pg.event._EventTypes, list[GameObject]] = {}
    
    def draw(self) -> None:
        self.screen.fill(const.BG_COLOR)
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

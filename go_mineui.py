import pygame as pg
from go import GameObject
from go_grid import goGrid
import static
import const


class goMineUI(GameObject):
    def __init__(self) -> None:
        super().__init__()

    def onAdd(self):
        self.goGrid: goGrid = static.game.findGameObjectByType(goGrid)
        self.font = pg.font.Font(const.FONT_PATH + 'consolab.ttf', 32)
        # Run update here to get the values of width and height from the render
        self.update(0)
        self.x = const.WINDOW_PADDING
        self.y = (const.WINDOW_PADDING + const.UI_SPACE) / 2 - self.height / 2

    def update(self, dt):
        self.remaining = self.goGrid.mines - self.goGrid.flagged
        if static.game.playing:
            self.img = self.font.render(
                f'Remaining mines: {self.remaining:02}', True, const.UI_COLOR)
        elif static.game.finalize:
            self.img = self.font.render('Press R to restart.', True, const.UI_COLOR)
        r = self.img.get_rect()
        self.width = r.width
        self.height = r.height

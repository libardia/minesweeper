from go import GameObject
import static
import const


class goResultUI(GameObject):
    def __init__(self) -> None:
        super().__init__()

    def onAdd(self):
        self.font = static.font.consolab32
        self.update(0)

    def update(self, dt):
        if static.game.playing:
            self.img = self.font.render('Careful...', True, const.UI_COLOR)
        elif static.game.finalize:
            if static.game.wonGame:
                self.img = self.font.render('You won!', True, (0, 255, 0))
            else:
                self.img = self.font.render('You lost.', True, (255, 0, 0))
        r = self.img.get_rect()
        self.width = r.width
        self.height = r.height
        self.x = static.game.screen.get_width() - const.WINDOW_PADDING - self.width
        self.y = (const.WINDOW_PADDING + const.UI_SPACE) / 2 - self.height / 2

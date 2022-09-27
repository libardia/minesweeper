from xmlrpc.server import DocXMLRPCRequestHandler
from go import GameObject
import static, const


class goSmile(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.img = static.image.smile
        speed = 0.5
        self.dx = speed
        self.dy = speed

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        if self.x + self.img.get_width() > const.SCREEN_WIDTH or self.x < 0:
            self.dx = -self.dx
        if self.y + self.img.get_height() > const.SCREEN_HEIGHT or self.y < 0:
            self.dy = -self.dy

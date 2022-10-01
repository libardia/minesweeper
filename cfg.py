import configparser
import const


class ConfigHolder():
    def __init__(self) -> None:
        self.cfg = configparser.ConfigParser(defaults={
            'width': const.DEF_GRID_WIDTH,
            'height': const.DEF_GRID_HEIGHT,
            'mines': const.DEF_GRID_MINES
        })
        self.cfg.read(const.CONFIG_FILE)

    def save(self):
        print('Saving config')
        with open(const.CONFIG_FILE, 'w') as file:
            self.cfg.write(file)

    def getGridWidth(self):
        return self.cfg.getint('DEFAULT', 'width')

    def getGridHeight(self):
        return self.cfg.getint('DEFAULT', 'height')

    def getNumMines(self):
        return self.cfg.getint('DEFAULT', 'mines')

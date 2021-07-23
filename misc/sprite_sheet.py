import pygame as pg


class SpriteSheet:
    def __init__(self, sprite_path: str, sprite_size=(0, 0)):
        self.img = pg.image.load(sprite_path).convert_alpha()
        self.img.set_colorkey((0, 0, 0))
        self.x, self.y = sprite_size

    @property
    def all_frames(self) -> list[pg.image]:
        def creator():
            if self.x and self.y:
                for i in range(self.img.get_width() // self.x):
                    yield self.img.subsurface((self.x * i, 0, self.x, self.y))
            else:
                yield self.img
        return list(creator())

import pygame as pg


class SpriteSheet:
    def __init__(self, sprite_path: str, sprite_size=(0, 0)):
        self.__img = pg.image.load(sprite_path)
        self.__img.set_colorkey((0, 0, 0))
        self.__x, self.__y = sprite_size
        self.__all_frames = list(self.__get_all_frames)

    @property
    def __get_all_frames(self):
        if self.__x and self.__y:
            for i in range(self.__img.get_width() // self.__x):
                yield self.__img.subsurface((self.__x * i, 0, self.__x, self.__y))
        else:
            yield self.__img

    def __getitem__(self, item):
        return self.__all_frames[item]

    def __setitem__(self, key, value):
        self.__all_frames[key] = value

    def __len__(self):
        return len(self.__all_frames)

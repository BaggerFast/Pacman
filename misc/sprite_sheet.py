import pygame as pg


class SpriteSheet:
    def __init__(self, sprite_path: str, sprite_size: tuple =(0, 0)):
        self.__img = pg.image.load(sprite_path)
        self.__x, self.__y = sprite_size
        self.__all_frames = self.__get_all_frames()

    def __get_all_frames(self):
        if not (self.__x and self.__y):
            return tuple(tuple([self.__img]))
        local_x = self.__img.get_width() // self.__x
        local_y = self.__img.get_height() // self.__y
        frames = []
        for y in range(local_y):
            local = []
            for x in range(local_x):
                local.append(self.__img.subsurface((x * self.__x, y * self.__y, self.__x, self.__y)))
            frames.append(tuple(local))
        return tuple(frames)

    def __getitem__(self, item):
        return self.__all_frames[item]

    def __len__(self):
        return len(self.__all_frames)

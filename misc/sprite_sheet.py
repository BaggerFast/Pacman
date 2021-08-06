import pygame as pg


class SpriteSheet:
    def __init__(self, sprite_path: str, sprite_size=(0, 0)):
        self.__img = pg.image.load(sprite_path)
        self.__img.set_colorkey((0, 0, 0))
        self.__x, self.__y = sprite_size
        self.sprite_size = sprite_size
        self.__all_frames = self.__get_all_frames

    @property
    def __get_all_frames(self):
        if self.sprite_size[0] > 0 and self.sprite_size[1] > 0:
            local_x, local_y = self.__img.get_width() // self.sprite_size[0], self.__img.get_height() // self.sprite_size[1]
            frames = []
            for y in range(local_y):
                local = []
                for x in range(local_x):
                    local.append(self.__img.subsurface((x * self.__x, y * self.__y, self.__x, self.__y)))
                frames.append(local)
            return tuple(tuple(i) for i in frames)
        else:
            return [[self.__img]]

    def __getitem__(self, item):
        return self.__all_frames[item]

    def __len__(self):
        return len(self.__all_frames)

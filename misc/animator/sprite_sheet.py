import pygame as pg

from misc import load_image


class SpriteSheet:

    def __init__(self, sprite_path: str, sprite_size: tuple):
        self.__all_frames = self.__get_all_frames(load_image(sprite_path), sprite_size[0], sprite_size[1])

    def __getitem__(self, item: int) -> pg.image:
        return self.__all_frames[item]

    def __len__(self):
        return len(self.__all_frames)

    @staticmethod
    def __get_all_frames(img: pg.image, x, y) -> tuple:
        if not (x and y):
            raise Exception('sprite_size не может быть равен 0')
        frames = [
            [img.subsurface((_x * x, y * _y, x, y)) for _x in range(img.get_width() // x)]
            for _y in range(img.get_height() // y)
        ]
        return tuple(frames)

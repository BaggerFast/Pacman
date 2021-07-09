import pygame as pg

from misc import Color, BaseFromFileLoader
from objects import DrawableObject, ImageObject


class Map(DrawableObject):
    size = (224, 248)
    tile_names = [
        "space",
        "fat_up_wall", "fat_left_corner",
        "fat_y_corner", "up_wall",
        "left_corner", "ghost_left_corner",
        "ghost_door", "ghost_door_wall_left"
    ]
    tiles = []

    def __init__(self, game, map_data: BaseFromFileLoader, x=0, y=20):
        super().__init__(game)
        self.rect.topleft = x, y
        self.rect.size = self.size
        self.map_data: BaseFromFileLoader = map_data
        self.surface = self.map_data.surface
        self.color = self.game.map_color
        self.paint()

    @property
    def surface(self) -> pg.Surface:
        return self.map_data.surface

    @surface.setter
    def surface(self, var: pg.Surface):
        self.map_data.surface = var

    def paint(self) -> None:
        temp_surface = pg.Surface(self.surface.get_size())
        temp_surface.fill(self.color)
        self.surface.set_colorkey(Color.MAIN_MAP)
        temp_surface.blit(self.surface, (0, 0))
        self.surface = temp_surface  # Set the color of the pixel.
        self.surface.set_colorkey(None)

    def prerender_map_image_scaled(self) -> ImageObject:
        image = ImageObject(self.game, self.surface.copy())
        image.smoothscale(100, 100)

        # Threshold
        for x in range(image.image.get_width()):
            for y in range(image.image.get_height()):
                if image.image.get_at((x, y))[2] != 0:
                    image.image.set_at((x, y), (0, 0, 255))  # Set the color of the pixel.
        return image

    def process_draw(self): self.game.screen.blit(self.surface, self.rect)


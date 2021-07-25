from typing import Union
import pygame as pg

from misc import get_path, Color
from misc.sprite_sheet import SpriteSheet
from objects import DrawableObject, ImageObject


class Tile(pg.sprite.Sprite):
    def __init__(self, image: Union[str, pg.Surface], cords: ()):
        super().__init__()
        if isinstance(image, str):
            self.image = pg.image.load(image)
        elif isinstance(image, pg.Surface):
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords

    def process_draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Map(DrawableObject):
    def __init__(self, game, map_data) -> None:
        super().__init__(game)
        self.game = game
        self.color = self.game.map_color
        self.map_data = map_data
        self.tile_size = 8
        self.sprite_sheet = SpriteSheet(sprite_path=get_path('images/map.png'), sprite_size=(self.tile_size,
                                                                                             self.tile_size))
        self.start_x, self.start_y = 0, 0
        self.tiles = list(self.load_tiles())
        self.surface = pg.Surface(self.resolution)
        self.draw_map()

    def draw_map(self):
        for tile in self.tiles:
            tile.process_draw(self.surface)

        for x in range(self.surface.get_width()):
            for y in range(self.surface.get_height()):
                if self.surface.get_at((x, y)) == Color.MAIN_MAP:
                    self.surface.set_at((x, y), self.color)

    def load_tiles(self):
        x, y = 0, 0
        for row in self.map_data:
            x = 0
            for tile in row:
                yield Tile(self.sprite_sheet[tile - 1], cords=(x * self.tile_size, y * self.tile_size))
                x += 1
            y += 1
        self.resolution = x * self.tile_size, y * self.tile_size

    def prerender_map_surface(self) -> pg.Surface:
        for x in range(self.surface.get_width()):
            for y in range(self.surface.get_height()):
                if self.surface.get_at((x, y)) == Color.MAIN_MAP:
                    self.surface.set_at((x, y), self.color)
        return self.surface

    def prerender_map_image_scaled(self) -> ImageObject:
        image = ImageObject(self.game, self.surface, (110, 96))
        image.smoothscale(100, 100)
        return image

    def process_draw(self):
        self.game.screen.blit(self.surface, (0, 20))

    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass

import pygame as pg

from misc import CELL_SIZE, get_image_path
from objects import DrawableObject


class Map(DrawableObject):
    tile_names = [
        "space.png",
        "fat_up_wall.png", "fat_left_corner.png",
        "fat_y_corner.png", "out_corner.png",
        "up_wall.png", "left_corner.png",
        "ghost_up_wall.png", "ghost_left_corner.png",
        "ghost_door.png", "ghost_door_wall_left.png"
    ]
    tiles = []

    def __init__(self, game, map_data, x=0, y=20) -> None:
        super().__init__(game)
        self.x = x
        self.y = y
        self.map = map_data
        self.surface = pg.Surface((224, 248))
        self.__load_tiles()
        self.__render_map_surface()

    def __load_tiles(self) -> None:
        self.tiles = []
        for i in self.tile_names:
            tile_path = get_image_path(i, "map")
            tile = pg.image.load(tile_path)
            self.tiles.append(tile)

    def __corner_preprocess(self, x, y, temp_surface: pg.surface.Surface) -> pg.surface.Surface:
        flip_x = self.map[y][x][1] // (CELL_SIZE//2)
        flip_y = False
        temp_surface = pg.transform.flip(temp_surface, flip_x, flip_y)
        rotate_angle = self.map[y][x][1] % (CELL_SIZE//2) * -90
        temp_surface = pg.transform.rotate(temp_surface, rotate_angle)
        return temp_surface

    def __draw_cell(self, x, y) -> None:
        temp_surface = self.tiles[self.map[y][x][0]]
        if len(self.map[y][x]) == 2:
            temp_surface = self.__corner_preprocess(x, y, temp_surface)
        self.surface.blit(temp_surface, (x * CELL_SIZE, y * CELL_SIZE))

    def __render_map_surface(self) -> None:
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.__draw_cell(x, y)

    def process_draw(self) -> None:
        self.game.screen.blit(self.surface, (self.x, self.y))

    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass


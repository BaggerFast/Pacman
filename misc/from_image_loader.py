from PIL import Image, ImageChops, ImageDraw
from typing import List, Tuple
from .base_from_file_loader import BaseFromFileLoader
from .constants import CELL_SIZE
from .vec import Vec
from .rotation import Rotation
import pygame
import os


class FromImageLoader(BaseFromFileLoader):
    pacman_image: Image.Image = Image.open("images/pacman/default/walk/0.png").convert('RGB')
    energizer_image: Image.Image = Image.open("images/map/energizer.png").convert('RGB')
    seed_image: Image.Image = Image.open("images/map/seed.png").convert('RGB')
    fruit_image: Image.Image = Image.open("images/fruit/0.png").convert('RGB')

    def __init__(self, filename: str):
        self.image: Image.Image
        self.draw: ImageDraw.ImageDraw
        self.pacman_image: Image.Image
        self.energizer_image: Image.Image
        self.seed_image: Image.Image
        self.fruit_image: Image.Image
        super(FromImageLoader, self).__init__(filename)
    
    def load(self):
        self.__load_images()
    
        self.find_pacman()
        self.find_ghosts()
        self.find_fruit()
        self.find_energizers()
        self.find_seeds()
        self.find_movements_data()
        self.compile_movements_data()
        self.create_surface()
    
    def __load_images(self):
        self.image = Image.open(os.path.join('maps', self.filename)).convert('RGB')
        self.draw = ImageDraw.ImageDraw(self.image)

    def find_pacman(self):
        for x, y in self.__iterator():
            diff = ImageChops.difference(self.image.crop((x + 1, y + 6, x + 13 + 1, y + 13 + 6)), self.pacman_image)
            if len(diff.getcolors()) == 1:
                self.player_pos = Vec(x / CELL_SIZE + 0.5, y // CELL_SIZE + 1)
                self.draw.rectangle((x + 1, y + 6, x + 13 + 1 - 1, y + 13 + 6 - 1), (0, 0, 0))
                return
        raise Exception("Пакмен не найден")

    def find_energizers(self):
        for x, y in self.__iterator():
            diff = ImageChops.difference(
                self.image.crop((x, y, x + CELL_SIZE, y + CELL_SIZE)),
                self.energizer_image
            )
            if len(diff.getcolors()) == 1:
                self.energizers_pos.append(Vec(x // CELL_SIZE, y // CELL_SIZE))
                self.draw.rectangle((x, y, x + CELL_SIZE-1, y + CELL_SIZE-1), (0, 0, 0))

    def find_seeds(self):
        for x, y in self.__iterator():
            diff = ImageChops.difference(
                self.image.crop((x, y, x + CELL_SIZE, y + CELL_SIZE)),
                self.seed_image
            )
            if len(diff.getcolors()) == 1:
                self.seed_data[y//CELL_SIZE][x//CELL_SIZE] = True
                self.draw.rectangle((x, y, x + CELL_SIZE-1, y + CELL_SIZE-1), (0, 0, 0))

    def find_movements_data(self):
        for x, y in self.__iterator():
            colors = self.image.crop((x, y, x + CELL_SIZE, y + CELL_SIZE)).getcolors()
            if len(colors) == 1 and hash(colors[0]) == hash((64, (0, 0, 0))):
                self.movements_data[y//CELL_SIZE][x//CELL_SIZE] = True
                # self.draw.rectangle((x, y, x + CELL_SIZE-1, y + CELL_SIZE-1), (0, 255, 0))

    def compile_movements_data(self):
        for pos in Vec(0, 0).iterator_to(self.size):
            tile = 0
            if self.movements_data[pos.y][pos.x]:
                for rot in reversed(Rotation):
                    pos2: Vec = pos.offset(rot)
                    tile *= 2
                    tile += bool(self.movements_data[pos2.y % self.size[1]][pos2.x % self.size[0]])
            self.movements_data[pos.y][pos.x] = tile

    def find_ghosts(self):
        self.ghosts_pos.append(self.find_ghost(Image.open("images/ghost/inky/top/0.png").convert('RGB')))
        self.ghosts_pos.append(self.find_ghost(Image.open("images/ghost/pinky/top/0.png").convert('RGB')))
        self.ghosts_pos.append(self.find_ghost(Image.open("images/ghost/clyde/top/0.png").convert('RGB')))
        self.ghosts_pos.append(self.find_ghost(Image.open("images/ghost/blinky/top/0.png").convert('RGB')))

    def find_ghost(self, image) -> Vec:
        for x, y in self.__iterator():
            diff = ImageChops.difference(self.image.crop((x + 1, y + 6, x + 14 + 1, y + 14 + 6)), image)
            if len(diff.getcolors()) == 1:
                self.draw.rectangle((x + 1, y + 6, x + 14 + 1 - 1, y + 14 + 6 - 1), (0, 0, 0))
                return Vec(x // CELL_SIZE + 0.5, y // CELL_SIZE + 1)
        raise Exception("Призрак не найден")

    def clear_memory(self):
        del self.draw, self.image

    def __iterator(self) -> tuple:  # не придумал имя
        for y in range(0, self.size[1]*CELL_SIZE, CELL_SIZE):
            for x in range(0, self.size[0]*CELL_SIZE, CELL_SIZE):
                yield x, y

    def create_surface(self):
        self.surface = pygame.image.frombuffer(self.image.tobytes(), self.image.size, self.image.mode)

    def find_fruit(self):
        for x, y in self.__iterator():
            diff = ImageChops.difference(self.image.crop((x + 2, y + 6, x + 12 + 2, y + 12 + 6)), self.fruit_image)
            if len(diff.getcolors()) == 1:
                self.fruit_pos = Vec(x / CELL_SIZE + 0.5, y // CELL_SIZE + 1)
                self.draw.rectangle((x + 2, y + 6, x + 12 + 2 - 1, y + 12 + 6 - 1), (0, 0, 0))
                return
        raise Exception("Фрукт не найден")

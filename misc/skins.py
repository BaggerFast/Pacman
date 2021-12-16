import pygame as pg
from copy import copy
from typing import Union, Dict
from objects import ImageObject
from misc.sprite_sheet import SpriteSheet
from misc import Animator, get_path, Sounds
from misc.animator import SpriteSheetAnimator
from misc.constants.skin_names import SkinsNames
from misc.sound_controller import SoundController


class Skin:

    def __init__(self, game, path: str, cost: dict, skin_name: str = SkinsNames.default):
        self.name: str = skin_name
        self.skin_cost: dict = cost
        self.game = game
        self.__walk = SpriteSheetAnimator(SpriteSheet(get_path(f'images/pacman/{path}/walk.png'), (13, 13)))
        self.__dead = Animator(SpriteSheet(get_path(f'images/pacman/{path}/dead.png'), (15, 15))[0],
                               time_out=125, repeat=False)
        self.__image = self.prerender_surface()

    @property
    def is_unlocked(self):
        return self.name in self.game.unlocked_skins

    @property
    def walk(self):
        return copy(self.__walk)

    @property
    def dead(self):
        return copy(self.__dead)

    @property
    def image(self):
        return self.__image

    def prerender_surface(self) -> ImageObject:
        image = ImageObject(self.game, self.__walk.sheet[0][3], (145, 125))
        image.scale(70, 70)
        return image

    def sound_preset(self):
        pass


class HalfLife(Skin):

    def sound_preset(self):
        self.game.sounds.siren = SoundController(self.game, Sounds.Ch.siren, Sounds.VALVE_SOUNDS[0])
        self.game.sounds.intro = SoundController(self.game, Sounds.Ch.intro, Sounds.VALVE_SOUNDS[1])
        self.game.sounds.seed = SoundController(self.game, Sounds.Ch.seed, Sounds.VALVE_SOUNDS[2])
        self.game.sounds.ghost = SoundController(self.game, Sounds.Ch.ghost, Sounds.VALVE_SOUNDS[3])
        self.game.sounds.pellet = SoundController(self.game, Sounds.Ch.pellet, Sounds.VALVE_SOUNDS[4])
        self.game.sounds.fruit = SoundController(self.game, Sounds.Ch.fruit, Sounds.VALVE_SOUNDS[5])
        self.game.sounds.pacman = SoundController(self.game, Sounds.Ch.pacman, Sounds.VALVE_SOUNDS[6])


class Windows(Skin):

    def sound_preset(self):
        self.game.sounds.intro = SoundController(self.game, Sounds.Ch.intro, Sounds.WINDOWS_SOUNDS[0])
        self.game.sounds.pacman = SoundController(self.game, Sounds.Ch.pacman, Sounds.WINDOWS_SOUNDS[1])
        self.game.sounds.seed = SoundController(self.game, Sounds.Ch.seed, Sounds.WINDOWS_SOUNDS[2])
        self.game.sounds.gameover = SoundController(self.game, Sounds.Ch.game_over, Sounds.WINDOWS_SOUNDS[3])
        self.game.sounds.ghost = SoundController(self.game, Sounds.Ch.ghost, Sounds.WINDOWS_SOUNDS[4])
        self.game.sounds.fruit = SoundController(self.game, Sounds.Ch.fruit, Sounds.WINDOWS_SOUNDS[5])


class PokeBall(Skin):

    def sound_preset(self):
        self.game.sounds.intro = SoundController(self.game, Sounds.Ch.intro, Sounds.POC_INTRO)


class Skins:

    def __init__(self, game):
        self.game = game

        self.default = Skin(self.game, f'default', {0: 0, 1: 0}, SkinsNames.default)
        self.half_life = HalfLife(self.game, f'half_life', {1: 14, 2: 10}, SkinsNames.half_life)
        self.pokeball = PokeBall(self.game, f'pokeball', {2: 12, 3: 8}, SkinsNames.pokeball)
        self.edge = Skin(self.game, f'edge', {3: 10, 4: 7}, SkinsNames.edge)
        self.chrome = Skin(self.game, f'chrome', {4: 7, 5: 6}, SkinsNames.chrome)
        self.windows = Windows(self.game, f'windows', {6: 5, 5: 4}, SkinsNames.windows)

        self.__current = self.default

    def prerender_surfaces(self) -> Dict[str, pg.Surface]:
        return {key: self.__dict__[key].image for key in self.all_skins}

    @property
    def all_skins(self) -> list:
        return [key for key in self.__dict__.keys() if isinstance(self.__dict__[key], Skin)]

    @property
    def current(self) -> Skin:
        return self.__current

    @current.setter
    def current(self, value: Union[str, Skin]):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, Skin):
            self.__current = value

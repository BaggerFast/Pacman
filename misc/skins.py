from copy import copy
from typing import Union
from misc import Animator, PathManager
from misc.animator import SpriteSheetAnimator
from misc.constants.classes import Sounds
from misc.constants.skin_names import SkinsNames
from misc.sound_controller import SoundController
from misc.sprite_sheet import SpriteSheet
from objects import ImageObject
from serializers import SkinSerializer


class Skin:

    def __init__(self, game, path: str, cost: dict, skin_name=SkinsNames.DEFAULT):
        # todo delete game
        self.name: str = skin_name.name
        self.skin_cost: dict = cost
        self.game = game
        self.__walk = SpriteSheetAnimator(SpriteSheet(PathManager.get_image_path(f'pacman/{path}/walk.png'), (13, 13)))
        self.__dead = Animator(SpriteSheet(PathManager.get_image_path(f'pacman/{path}/dead.png'), (15, 15))[0],
                               time_out=125, repeat=False)
        self.__image = self.prerender_surface()
    # region Public

    @property
    def is_unlocked(self):
        return self.name in SkinSerializer().unlocked

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
        image = ImageObject(self.__walk.sheet[0][3], (145, 125))
        image.scale(70, 70)
        return image

    def sound_preset(self):
        pass

    # endregion


class HalfLife(Skin):

    def sound_preset(self):
        self.game.sounds.siren = SoundController(Sounds.Ch.siren, Sounds.VALVE_SOUNDS[0])
        self.game.sounds.intro = SoundController(Sounds.Ch.intro, Sounds.VALVE_SOUNDS[1])
        self.game.sounds.seed = SoundController(Sounds.Ch.eatable, Sounds.VALVE_SOUNDS[2])
        self.game.sounds.ghost = SoundController(Sounds.Ch.eatable, Sounds.VALVE_SOUNDS[3])
        self.game.sounds.pellet = SoundController(Sounds.Ch.pellet, Sounds.VALVE_SOUNDS[4])
        self.game.sounds.fruit = SoundController(Sounds.Ch.eatable, Sounds.VALVE_SOUNDS[5])
        self.game.sounds.pacman = SoundController(Sounds.Ch.pacman, Sounds.VALVE_SOUNDS[6])


class Windows(Skin):

    def sound_preset(self):
        self.game.sounds.intro = SoundController(Sounds.Ch.intro, Sounds.WINDOWS_SOUNDS[0])
        self.game.sounds.pacman = SoundController(Sounds.Ch.pacman, Sounds.WINDOWS_SOUNDS[1])
        self.game.sounds.seed = SoundController(Sounds.Ch.eatable, Sounds.WINDOWS_SOUNDS[2])
        self.game.sounds.gameover = SoundController(Sounds.Ch.game_over, Sounds.WINDOWS_SOUNDS[3])
        self.game.sounds.ghost = SoundController(Sounds.Ch.eatable, Sounds.WINDOWS_SOUNDS[4])
        self.game.sounds.fruit = SoundController(Sounds.Ch.eatable, Sounds.WINDOWS_SOUNDS[5])


class PokeBall(Skin):

    def sound_preset(self):
        self.game.sounds.intro = SoundController(Sounds.Ch.intro, Sounds.POC_INTRO)


class Skins:

    def __init__(self, game):
        # todo delete game
        self.default = Skin(game, 'default', {0: 0, 1: 0}, SkinsNames.DEFAULT)
        self.edge = Skin(game, 'edge', {3: 10, 4: 7}, SkinsNames.EDGE)
        self.chrome = Skin(game, 'chrome', {4: 7, 5: 6}, SkinsNames.CHROME)

        self.half_life = HalfLife(game, 'half_life', {1: 14, 2: 10}, SkinsNames.HALF_LIFE)
        self.pokeball = PokeBall(game, 'pokeball', {2: 12, 3: 8}, SkinsNames.POKEMON)
        self.windows = Windows(game, 'windows', {6: 5, 5: 4}, SkinsNames.WINDOWS)

        self.__current = self.default

    # region Public

    @property
    def current(self) -> Skin:
        return self.__current

    @current.setter
    def current(self, value: Union[str, Skin]):
        if isinstance(value, Skin):
            self.__current = value
        elif hasattr(self, value):
            self.__current = getattr(self, value)

    # endregion

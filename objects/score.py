from misc.constants.skin_names import SkinsNames
from . import DrawableObject, Text
from misc import EvenType, Font, Points
import pygame as pg


class Score(DrawableObject):
    base_pos = (5, 270)
    shift = 20

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.__value = 0
        self.fear_mode = False
        self.fear_count = 0
        self.data = {
            EvenType.EatSeed: lambda: self + Points.POINT_PER_SEED * self.game.difficulty,
            EvenType.EatEnergizer: self.__eat_energizer,
            EvenType.EatGhost: self.__eat_ghost,
            EvenType.StopFearMode: self.__deactivate_fear_mode,
        }
        self.text = Text(self.game, f'{self.__value}', Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 8, 20, 20))

    def process_draw(self) -> None:
        self.text.text = f'{self.__value} {"Mb" if self.game.skins.current.name == SkinsNames.chrome else ""}'
        self.text.process_draw()

    def process_event(self, event: pg.event.Event) -> None:
        if event.type in self.data:
            self.data[event.type]()

    def __str__(self):
        return str(self.__value)

    def __int__(self):
        return self.__value

    @property
    def score(self):
        return self.__value

    def __add__(self, value):
        self.__value += value
        return self

    def __iadd__(self, value):
        return self + value

    def eat_fruit(self, bonus) -> None:
        self + bonus * self.game.difficulty

    def __eat_energizer(self):
        self.__activate_fear_mode()
        for ghost in self.game.current_scene.ghosts:
            ghost.toggle_mode_to_frightened()

    def __activate_fear_mode(self) -> None:
        self.fear_mode = True

    def __deactivate_fear_mode(self) -> None:
        self.fear_mode = False
        self.fear_count = 0

    def __eat_ghost(self) -> None:
        self + ((200 * self.game.difficulty ** 2) * 2 ** self.fear_count)
        self.fear_count += 1



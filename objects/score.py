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

    def process_draw(self) -> None:
        Text(self.game, f'{self.__value} {"Mb" if self.game.skins.current.name == SkinsNames.chrome else ""}',
             Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 8, 20, 20)).process_draw()

    def process_event(self, event: pg.event.Event) -> None:
        data = {
            EvenType.EatSeed: lambda: self + Points.POINT_PER_SEED * self.game.difficulty,
            EvenType.EatEnergizer: self.eat_energizer(),
            EvenType.EatGhost: self.eat_ghost(),
        }
        if event.type in data:
            print(event.type)
            data[event.type]()

    def process_logic(self) -> None:
        pass

    def __str__(self):
        return str(self.__value)

    def __int__(self):
        return self.__value

    @property
    def score(self):
        return self.__value

    def reset(self) -> None:
        self.__value = 0

    def __add__(self, value):
        self.__value += value
        return self

    def __iadd__(self, value):
        return self + value

    def eat_fruit(self, bonus) -> None:
        self + bonus * self.game.difficulty

    def eat_energizer(self):
        self.activate_fear_mode()
        # for ghost in self.game.ghosts:
        #     ghost.toggle_mode_to_frightened()

    def activate_fear_mode(self) -> None:
        self.fear_mode = True
        self.fear_count = 0

    def deactivate_fear_mode(self) -> None:
        self.fear_mode = False
        self.fear_count = 0

    def eat_ghost(self) -> None:
        self + ((200 * self.game.difficulty ** 2) * 2 ** self.fear_count)
        self.fear_count += 1



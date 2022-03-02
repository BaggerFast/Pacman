import pygame as pg

from misc import Animator
from misc.animator import SpriteSheetAnimator
from misc.constants import EvenType
from misc.interfaces.igeneric_object import IEventful
from misc.keyboards import PacmanKeyboard
from objects import HealthController
from objects.characters.character_base import Character


class Pacman(Character, IEventful):

    dir_action = {
        EvenType.GoUp: (0, -1, 3),
        EvenType.GoDown: (0, 1, 1),
        EvenType.GoLeft: (-1, 0, 2),
        EvenType.GoRight: (1, 0, 0)
    }

    def __init__(self, game, start_pos: tuple[int, int]):
        self.__walk_anim: Animator = game.skins.current.walk
        self.__dead_anim: Animator = game.skins.current.dead
        Character.__init__(self, game, self.__walk_anim, start_pos)
        self.hp = HealthController(self.game, 3)
        self.dead = False
        self.kb = PacmanKeyboard()
        self.__feature_rotate = (0, 0, 0)

    # region Public

    # region Implementation of parent classes

    def process_event(self, event: pg.event.Event) -> None:
        self.hp.process_event(event)
        if event.type in self.dir_action.keys() and not self.dead:
            self.go()
            self.__feature_rotate = self.dir_action[event.type]

    def process_logic(self) -> None:
        self.kb.process_logic()
        self.hp.process_logic()
        self.animator.timer_check()
        if self.dead:
            return
        if self.in_center():
            if self.move_to(self.rotate):
                self.go()
            else:
                self.stop()
                self.animator.change_cur_image(0)
            if self.move_to(self.__feature_rotate[2]):
                self.set_dir()
        Character.process_logic(self)

    def process_draw(self, screen: pg.Surface) -> None:
        Character.process_draw(self, screen)
        self.hp.process_draw(screen)

    # endregion

    @property
    def dead_anim(self):
        return self.__dead_anim

    def get_rect(self):
        return self.animator.current_image.get_rect()

    def set_dir(self):
        self.shift_x, self.shift_y, rotate = self.__feature_rotate
        if self.rotate == rotate:
            return
        self.rotate = rotate
        if isinstance(self.animator, SpriteSheetAnimator):
            self.animator.rotate = rotate

    def death(self) -> None:
        self.game.sounds.siren.pause()
        self.game.sounds.pellet.stop()
        self.game.sounds.pacman.play()

        self.animator = self.__dead_anim
        self.animator.start()

        self.dead = True

    # endregion

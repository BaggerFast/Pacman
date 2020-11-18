import pygame

from misc.path import get_image_path
from objects.character_base import Character
from misc.animator import Animator


class Pacman(Character):
    def __init__(self, game, start_pos: tuple):
        self.animator = Animator(
            get_image_path("Pacman1.png"),
            get_image_path('Pacman2.png')
        )
        super().__init__(game, self.animator, start_pos)

    def process_event(self, event):
        action = {
            pygame.K_w: 'up',
            pygame.K_a: 'left',
            pygame.K_s: 'down',
            pygame.K_d: 'right'
        }
        if event.type == pygame.KEYDOWN and event.key in action.keys():
            self.go()
            self.set_direction(action[event.key])

    def process_logic(self):
        self.animator.timer_check()
        super().process_logic()


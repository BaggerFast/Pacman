import pygame

from misc.animator import Animator
from misc.constants import CELL_SIZE
from misc.path import get_image_path
from objects.character_base import Character


class Pacman(Character):
    def __init__(self, game, start_pos: tuple):
        self.animator = Animator(
            get_image_path("Pacman1.png"),
            get_image_path('Pacman2.png')
        )
        super().__init__(game, self.animator, start_pos)
        self.feature_rotate = "none"

    def process_event(self, event):
        action = {
            pygame.K_w: 'up',
            pygame.K_a: 'left',
            pygame.K_s: 'down',
            pygame.K_d: 'right'
        }
        if event.type == pygame.KEYDOWN and event.key in action.keys():
            self.go()
            self.feature_rotate = action[event.key]

    def process_logic(s):
        s.animator.timer_check()
        if s.in_center():
            if s.move_to(s.rotate):
                s.go()
            else:
                s.stop()
            c = s.direction[s.feature_rotate][2]
            if s.move_to(c):
                s.set_direction(s.feature_rotate)
        super().process_logic()

    def movement_cell(self):
        scene = self.game.scenes[self.game.current_scene_index]
        cell = scene.movements_data[(self.rect.y-12) // CELL_SIZE][self.rect.x // CELL_SIZE+1]
        return "{0:04b}".format(cell)[::-1]

    def move_to(self,direction):
        return self.movement_cell()[direction] == "1"

    def in_center(self) -> bool:
        return self.rect.x % CELL_SIZE == 6 and (self.rect.y-20) % CELL_SIZE == 6

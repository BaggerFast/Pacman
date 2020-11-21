import pygame

from misc.path import get_image_path_for_animator
from misc.constants import CELL_SIZE
from objects.character_base import Character
from misc.animator import Animator


class Pacman(Character):
    def __init__(self, game, start_pos: tuple):
        self.animator = Animator(
            get_image_path_for_animator('Pacman', 'walk')
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

    def process_logic(self):
        self.animator.timer_check()
        if self.in_center():
            if self.move_to(self.rotate):
                self.go()
            else:
                self.stop()
            c = self.direction[self.feature_rotate][2]
            if self.move_to(c):
                self.set_direction(self.feature_rotate)
        super().process_logic()

    def movement_cell(self):
        scene = self.game.scenes[self.game.current_scene_index]
        cell = scene.movements_data[(self.rect.y-12) // CELL_SIZE][self.rect.x // CELL_SIZE+1]
        return "{0:04b}".format(cell)[::-1]

    def move_to(self, direction):
        return self.movement_cell()[direction] == "1"

    def in_center(self) -> bool:
        return self.rect.x % CELL_SIZE == 6 and (self.rect.y-20) % CELL_SIZE == 6

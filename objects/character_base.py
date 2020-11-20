from misc.health import Health
from objects.base import DrawableObject
from misc.animator import Animator


class Character(DrawableObject):
    direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
    }

    def __init__(self, game, animator: Animator, start_pos: tuple):
        super().__init__(game)
        self.hp = Health()
        self.animator = animator
        self.rect = self.animator.current_image.get_rect()
        self.shift_x, self.shift_y = self.direction["right"][:2]
        self.move(*start_pos)
        self.speed = 0
        self.rotate = 0

    def step(self):
        self.rect.x = (self.rect.x + self.shift_x * self.speed + self.game.width) % self.game.width
        self.rect.y = (self.rect.y + self.shift_y * self.speed + self.game.height) % self.game.height

    def go(self):
        self.speed = 1

    def stop(self):
        self.speed = 0

    def set_direction(self, new_direction=None):
        if new_direction:
            self.shift_x, self.shift_y, rotate = self.direction[new_direction]
            if self.rotate != rotate:
                self.rotate = rotate
                self.animator.rotate = rotate
                self.animator.change_rotation()

    def process_logic(self):
        self.step()

    def process_draw(self):
        self.game.screen.blit(self.animator.current_image, self.rect)

from misc.constants import CELL_SIZE
from misc.health import Health
from objects.base import DrawableObject
from misc.animator import Animator


class Character(DrawableObject):
    direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
        "none": (0, 0, None)
    }

    def __init__(self, game, animator: Animator, start_pos: tuple):
        super().__init__(game)
        self.animator = animator
        self.rect = self.animator.current_image.get_rect()
        self.shift_x, self.shift_y = self.direction["right"][:2]
        self.start_pos = start_pos
        self.move(*self.start_pos)
        self.speed = 0
        self.rotate = 0

    def step(self):
        self.rect.centerx = (self.rect.centerx + self.shift_x * self.speed + self.game.width) % self.game.width
        self.rect.centery = (self.rect.centery + self.shift_y * self.speed + self.game.height) % self.game.height

    def go(self):
        if self.speed != 0:
            self.animator.start()
        self.speed = 1

    def stop(self):
        self.animator.stop()
        self.speed = 0

    def set_direction(self, new_direction='none'):
        if new_direction:
            self.shift_x, self.shift_y, rotate = self.direction[new_direction]
            if self.rotate != rotate:
                self.rotate = rotate
                self.animator.rotate = rotate
                if self.animator.is_rotation:
                    self.animator.change_rotation()

    def process_logic(self):
        self.step()

    def process_draw(self):
        for i in range(-1, 2):
            self.game.screen.blit(self.animator.current_image, (self.rect.x+self.game.width*i, self.rect.y))

# Обработка коллизий (не трогайте пажожда, я сам не понимаю как это работает, я пытался понять, но я так и не смог)

    def movement_cell(self):
        scene = self.game.scenes_dict[self.game.current_scene_name]
        cell = scene.movements_data[(self.rect.y-12) // CELL_SIZE][self.rect.x // CELL_SIZE+1]
        return "{0:04b}".format(cell)[::-1]

    def move_to(self, direction):
        return self.movement_cell()[direction] == "1"

    def in_center(self) -> bool:
        return self.rect.x % CELL_SIZE == 6 and (self.rect.y-20) % CELL_SIZE == 6

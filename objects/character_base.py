from misc import CELL_SIZE, Animator
from objects import DrawableObject


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
        self.start_pos = self.pos_from_cell(start_pos)
        self.move_center(*self.start_pos)
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
            self.game.screen.blit(self.animator.current_image, (self.rect.x + self.game.width * i, self.rect.y))

    def movement_cell(self, cell: tuple) -> list:
        scene = self.game.scenes[self.game.current_scene_name]
        cell = scene.movements_data[cell[1]][cell[0]]
        return [i == '1' for i in "{0:04b}".format(cell)[::-1]]

    def move_to(self, direction) -> bool:
        return self.movement_cell(self.get_cell())[direction]

    def in_center(self) -> bool:
        return self.rect.centerx % CELL_SIZE == CELL_SIZE // 2 \
               and (self.rect.centery - 20) % CELL_SIZE == CELL_SIZE // 2

    def get_cell(self) -> tuple:
        return self.rect.centerx // CELL_SIZE, (self.rect.centery - 20) // CELL_SIZE

    @staticmethod
    def two_cells_dis(cell1: tuple, cell2: tuple) -> float:
        return ((cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2) ** 0.5

    @staticmethod
    def pos_from_cell(cell: tuple) -> tuple:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2

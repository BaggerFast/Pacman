from .base import Base


class Inky(Base):

    def process_logic(self):
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.animator = self.right_walk_anim
                self.shift_x = 1
                self.shift_y = 0
                self.speed = 1
                scene = self.game.scenes[self.game.current_scene_name]
                if self.rect.x == scene.pinky.start_pos[0]:
                    self.animator = self.top_walk_anim
                    self.shift_x = 0
                    self.shift_y = -1
                if self.rect.y == scene.blinky.start_pos[1]:
                    self.shift_x = 1
                    self.shift_y = 0
                    self.is_in_home = False
                    self.collision = True

    def get_love_cell(self, pacman, blinky=None):
        pacman_cell = pacman.get_cell()
        blinky_cell = blinky.get_cell()
        rotate = pacman.rotate
        pinky_love_cell = (
        pacman_cell[0] + self.direction2[rotate][0] * 2, pacman_cell[1] + self.direction2[rotate][1] * 2)
        vector_blinky_cell_pinky_love_cell = (blinky_cell[0] - pinky_love_cell[0], blinky_cell[1] - pinky_love_cell[1])
        self.love_cell = (pinky_love_cell[0] + vector_blinky_cell_pinky_love_cell[0],
                          pinky_love_cell[1] + vector_blinky_cell_pinky_love_cell[1])

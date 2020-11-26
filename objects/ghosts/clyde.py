from .base import Base


class Clyde(Base):

    def process_logic(self):
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("left")
                self.go()
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

    def get_love_cell(self, pacman, blinky = None):
        pass

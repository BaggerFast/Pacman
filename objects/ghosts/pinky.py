from .base import Base


class Pinky(Base):

    def process_logic(self):
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.animator = self.top_walk_anim
                self.shift_x = 0
                self.shift_y = -1
                self.speed = 1
                scene = self.game.scenes[self.game.current_scene_name]
                if self.rect.y == scene.blinky.start_pos[1]:
                    self.shift_x = 1
                    self.shift_y = 0
                    self.is_in_home = False
                    self.collision = True

    def get_love_cell(self, pacman, blinky = None):
        rotate = pacman.rotate
        self.love_cell = (pacman.get_cell()[0]+self.direction2[rotate][0]*2, pacman.get_cell()[1]+self.direction2[rotate][1]*2)


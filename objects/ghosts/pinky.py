from .base import Base


class Pinky(Base):
    love_point_in_runaway_mode = (2, -3)
    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("up")
                self.go()
                scene = self.game.current_scene
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    def get_love_cell(self, pacman, blinky) -> None:
        super().get_love_cell()
        if self.mode == 'Chase':
            rotate = pacman.rotate
            self.love_cell = (pacman.get_cell()[0]+self.direction2[rotate][0]*2, pacman.get_cell()[1]+self.direction2[rotate][1]*2)

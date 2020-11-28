from .base import Base


class Inky(Base):
    max_count_eat_seeds_in_home = 30

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("right")
                self.go()
                scene = self.game.current_scene
                if self.rect.centerx == scene.pinky.start_pos[0]:
                    self.set_direction("up")
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    def get_love_cell(self, pacman) -> None:
        pacman_cell = pacman.get_cell()
        rotate = pacman.rotate
        pinky_love_cell = (
            pacman_cell[0] + self.direction2[rotate][0] * 2, pacman_cell[1] + self.direction2[rotate][1] * 2)
        vector_blinky_cell_pinky_love_cell = (pacman_cell[0] - pinky_love_cell[0], pacman_cell[1] - pinky_love_cell[1])
        self.love_cell = (pinky_love_cell[0] + vector_blinky_cell_pinky_love_cell[0],
                          pinky_love_cell[1] + vector_blinky_cell_pinky_love_cell[1])

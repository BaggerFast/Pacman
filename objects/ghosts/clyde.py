from .base import Base


class Clyde(Base):
    max_count_eat_seeds_in_home = 59

    def process_logic(self):
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("left")
                self.go()
                scene = self.game.current_scene
                if self.rect.centerx == scene.pinky.start_pos[0]:
                    self.set_direction("up")
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    def get_love_cell(self, pacman):
        pass

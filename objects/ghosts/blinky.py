from .base import Base


class Blinky(Base):
    love_point_in_runaway_mode = (33, -3)
    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            self.collision = True
            self.go()

    def get_love_cell(self, pacman, blinky) -> None:
        super().get_love_cell()
        if self.mode == 'Chase':
            self.love_cell = pacman.get_cell()

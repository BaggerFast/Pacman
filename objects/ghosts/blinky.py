from .base import Base


class Blinky(Base):

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            self.collision = True
            self.go()

    def get_love_cell(self, pacman, blinky) -> None:
        self.love_cell = pacman.get_cell()

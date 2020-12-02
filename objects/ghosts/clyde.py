from .base import Base
import pygame as pg

class Clyde(Base):
    max_count_eat_seeds_in_home = 60
    love_point_in_runaway_mode = (0, 32)
    def process_logic(self) -> None:
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

    def ghosts_ai(self, pacman, blinky) -> None:
        if self.mode == 'Scater':
            self.love_cell = self.love_point_in_runaway_mode
            if pg.time.get_ticks() - self.ai_timer <= 7000:
                self.toggle_mode()

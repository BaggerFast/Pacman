from pygame import Surface

from pacman.data_core.game_objects import GameObjects
from pacman.data_core.interfaces import IDrawable
from pacman.objects import Inky, Pinky, Clyde, Blinky


class GhostManager(IDrawable):
    def __init__(self, game, level_loader, seeds_count):
        self.ghosts = GameObjects()

        self.inky = Inky(game, level_loader, seeds_count)
        self.pinky = Pinky(game, level_loader, seeds_count)
        self.clyde = Clyde(game, level_loader, seeds_count)
        self.blinky = Blinky(game, level_loader, seeds_count)

        self.ghosts += [self.inky, self.pinky, self.blinky, self.clyde]

    def draw(self, screen: Surface) -> None:
        self.ghosts.draw(screen)

    def toggle_mode_to_frightened(self):
        for ghost in self.ghosts:
            ghost.toggle_mode_to_frightened()

    def ghost_home_ai(self, eaten_seeds):
        home_ghosts = filter(lambda g: g.is_in_home, self.ghosts)
        for ghost in home_ghosts:
            ghost.home_ai(eaten_seeds)

    def update_timers(self):
        for ghost in self.ghosts:
            ghost.update_ai_timer()

import pygame

from misc.loader import LevelLoader
from objects.map import Map
from objects.seed import SeedContainer
from scenes.base import BaseScene


class GameScene(BaseScene):
    def __init__(self, game):
        self.loader = LevelLoader()
        self.map_data = self.loader.get_map_data()
        self.seed_data = self.loader.get_seed_data()
        self.energizer_data = self.loader.get_energizer_data()
        self.movements_data = self.loader.get_movements_data()
        self.player_position = self.loader.get_player_position()
        self.ghost_positions = self.loader.get_ghost_positions()
        self.fruit_position = self.loader.get_fruit_position()
        super().__init__(game)

    def create_objects(self) -> None:
        self.map = Map(self.game, self.map_data)
        self.objects.append(self.map)
        self.seeds = SeedContainer(self.game, self.seed_data, self.energizer_data)
        self.objects.append(self.seeds)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.start_pause()

    def start_pause(self):
        self.game.set_scene(self.game.SCENE_PAUSE)

    def additional_draw(self) -> None:
        # Temporary draw
        x_shift = 0
        y_shift = 20

        # pacman
        pygame.draw.circle(self.screen, (255, 255, 0),
                           (x_shift + self.player_position[0] * 8 + 4, y_shift + self.player_position[1] * 8 + 4), 8)

        # ghosts
        pygame.draw.circle(self.screen, (255, 0, 0),
                           (x_shift + self.ghost_positions[0][0] * 8 + 4, y_shift + self.ghost_positions[0][1] * 8 + 4),
                           8)
        pygame.draw.circle(self.screen, (255, 0, 255),
                           (x_shift + self.ghost_positions[1][0] * 8 + 4, y_shift + self.ghost_positions[1][1] * 8 + 4),
                           8)
        pygame.draw.circle(self.screen, (0, 0, 255),
                           (x_shift + self.ghost_positions[2][0] * 8 + 4, y_shift + self.ghost_positions[2][1] * 8 + 4),
                           8)
        pygame.draw.circle(self.screen, (0, 255, 0),
                           (x_shift + self.ghost_positions[3][0] * 8 + 4, y_shift + self.ghost_positions[3][1] * 8 + 4),
                           8)

        # fruit
        pygame.draw.circle(self.screen, (255, 0, 0),
                           (x_shift + self.fruit_position[0] * 8 + 4, y_shift + self.fruit_position[1] * 8 + 4), 4)

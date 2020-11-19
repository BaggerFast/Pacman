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

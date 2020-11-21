import pygame as pg

from misc.loader import LevelLoader
from objects.map import Map
from objects.seed import SeedContainer
from misc.constants import Color, Points
from misc.path import get_image_path
from objects.image import ImageObject
from objects.text import Text
from objects.pacman import Pacman
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

    def prepare_lives_meter(self):
        for i in range(int(self.game.lives)):
            hp_image = ImageObject(self.game, get_image_path('1.png', 'Pacman', 'Walk'), 5 + i * 20, 271)
            hp_image.scale(12, 12)
            hp_image.rotate(180)
            self.objects.append(hp_image)

    def create_objects(self) -> None:
        self.map = Map(self.game, self.map_data)
        self.objects.append(self.map)
        self.seeds = SeedContainer(self.game, self.seed_data, self.energizer_data)
        self.objects.append(self.seeds)

        self.prepare_lives_meter()

        self.scores_label_text = Text(self.game, 'SCORE', 8, rect=pg.Rect(10, 2, 20, 20), color=Color.WHITE)
        self.objects.append(self.scores_label_text)
        self.scores_value_text = Text(self.game, str(self.game.score), 8, rect=pg.Rect(10, 9, 20, 20),
                                      color=Color.WHITE)
        self.objects.append(self.scores_value_text)

        self.highscores_label_text = Text(self.game, 'HIGHSCORE', 8, rect=pg.Rect(130, 2, 20, 20),
                                          color=Color.WHITE)
        self.objects.append(self.highscores_label_text)
        self.highscores_value_text = Text(self.game, str(self.game.records.data[-1]), 8,
                                          rect=pg.Rect(130, 9, 20, 20),
                                          color=Color.WHITE)
        self.objects.append(self.highscores_value_text)


        self.pacman = Pacman(self.game, (-6 + self.player_position[0] * 8 + 4, 14 + self.player_position[1] * 8 + 4))
        self.objects.append(self.pacman)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.start_pause()

    def start_pause(self):
        self.game.set_scene(self.game.SCENE_PAUSE)

    def draw_ghost(self, index, color, x, y):
        pg.draw.circle(
            self.screen, color,
            (x + self.ghost_positions[index][0] * 8 + 4, y + self.ghost_positions[index][1] * 8 + 4),
            8
        )

    def additional_draw(self) -> None:
        # Temporary draw
        x_shift = 0
        y_shift = 20

        # ghosts
        self.draw_ghost(0, (255, 0, 0), x_shift, y_shift)
        self.draw_ghost(1, (255, 0, 255), x_shift, y_shift)
        self.draw_ghost(2, (0, 0, 255), x_shift, y_shift)
        self.draw_ghost(3, (0, 255, 0), x_shift, y_shift)

        # fruit
        pg.draw.circle(self.screen, (255, 0, 0),
                           (x_shift + self.fruit_position[0] * 8 + 4, y_shift + self.fruit_position[1] * 8 + 4), 4)

    def process_collision(self) -> None:
        if_eats, type = self.seeds.process_collision(self.pacman)
        if if_eats:
            if type == "seed":
                self.game.score.eat_seed()
            elif type == "energizer":
                self.game.score.eat_energizer()


    def process_logic(self) -> None:
        super(GameScene, self).process_logic()
        self.process_collision()

        # todo: make text update only when new value appeares
        self.scores_value_text.update_text(str(self.game.score))

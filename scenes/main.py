import pygame as pg

from misc.health import Health
from misc.loader import LevelLoader
from objects.ghosts.blinky import Blinky
from objects.ghosts.clyde import Clyde
from objects.ghosts.inky import Inky
from objects.ghosts.pinky import Pinky
from objects.map import Map
from objects.seed import SeedContainer
from misc.constants import Color, INDEX_SCENES
from misc.constants import CELL_SIZE
from misc.path import get_image_path
from objects.image import ImageObject
from objects.text import Text
from objects.pacman import Pacman
from scenes.base import BaseScene
from misc.constants import Font


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
        self.first_run = not not not not not not not not not not not not not not not not not not not not not not not not not not not False
        super().__init__(game)

    def prepare_lives_meter(self):
        self.last_hp = []
        for i in range(int(self.pacman.hp)):
            hp_image = ImageObject(self.game, get_image_path('1.png', 'pacman', 'walk'), 5 + i * 20, 271)
            hp_image.scale(12, 12)
            hp_image.rotate(180)
            self.last_hp.append(hp_image)

    def create_objects(self) -> None:
        self.objects = []
        self.map = Map(self.game, self.map_data)
        self.objects.append(self.map)
        self.seeds = SeedContainer(self.game, self.seed_data, self.energizer_data)
        self.objects.append(self.seeds)

        self.scores_label_text = Text(self.game, 'SCORE', Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 2, 20, 20), color=Color.WHITE)
        self.objects.append(self.scores_label_text)
        self.scores_value_text = Text(self.game, str(self.game.score),Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 10, 20, 20),
                                      color=Color.WHITE)
        self.objects.append(self.scores_value_text)

        self.highscores_label_text = Text(self.game, 'HIGHSCORE', Font.MAIN_SCENE_SIZE, rect=pg.Rect(130, 2, 20, 20),
                                          color=Color.WHITE)
        self.objects.append(self.highscores_label_text)
        self.highscores_value_text = Text(self.game, str(self.game.records.data[-1]), Font.MAIN_SCENE_SIZE,
                                          rect=pg.Rect(130, 10, 20, 20),
                                          color=Color.WHITE)
        self.objects.append(self.highscores_value_text)


        self.pacman = Pacman(self.game, (-6+self.player_position[0] * CELL_SIZE + CELL_SIZE//2, 14 + self.player_position[1] * CELL_SIZE + CELL_SIZE//2))
        self.objects.append(self.pacman)
        self.prepare_lives_meter()

        self.blinky = Blinky(self.game, (-7+self.ghost_positions[3][0] * CELL_SIZE + CELL_SIZE // 2, 14+self.ghost_positions[3][1] * CELL_SIZE + CELL_SIZE // 2))
        self.pinky = Pinky(self.game, (-7+self.ghost_positions[1][0] * CELL_SIZE + CELL_SIZE // 2, 14+self.ghost_positions[2][1] * CELL_SIZE + CELL_SIZE // 2))
        self.inky = Inky(self.game, (-7+self.ghost_positions[0][0] * CELL_SIZE + CELL_SIZE // 2, 14+self.ghost_positions[1][1] * CELL_SIZE + CELL_SIZE // 2), 30)
        self.clyde = Clyde(self.game, (-7+self.ghost_positions[2][0] * CELL_SIZE + CELL_SIZE // 2, 14+self.ghost_positions[0][1] * CELL_SIZE + CELL_SIZE // 2), 60)

        self.ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]

        self.not_prefered_ghosts = [
            self.pinky,
            self.inky,
            self.clyde
        ]

        self.prefered_ghost = self.pinky
        self.count_prefered_ghost = 1

        self.objects.append(self.blinky)
        self.objects.append(self.pinky)
        self.objects.append(self.inky)
        self.objects.append(self.clyde)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.start_pause()

    def start_pause(self):
        self.game.set_scene(INDEX_SCENES['SCENE_PAUSE'])

    def draw_ghost(self, index, color, x, y):
        pg.draw.circle(
            self.screen, color,
            (x + self.ghost_positions[index][0] * CELL_SIZE + CELL_SIZE//2, y + self.ghost_positions[index][1] * CELL_SIZE + CELL_SIZE//2),
            8
        )

    def additional_draw(self) -> None:
        # Temporary draw
        x_shift = 0
        y_shift = 20

        # fruit
        pg.draw.circle(self.screen, (255, 0, 0),
                       (x_shift + self.fruit_position[0] * CELL_SIZE + CELL_SIZE//2,
                        y_shift + self.fruit_position[1] * CELL_SIZE + CELL_SIZE//2), 4)

    def change_prefered_ghost(self):
        self.count_prefered_ghost += 1
        self.not_prefered_ghosts.pop(0)
        if self.count_prefered_ghost < 4:
            self.prefered_ghost = self.ghosts[self.count_prefered_ghost]
        else:
            self.prefered_ghost = None
            self.count_prefered_ghost = 0

    def process_collision(self) -> None:
        is_eaten, type = self.seeds.process_collision(self.pacman)
        for ghost in self.ghosts:
            if ghost.collision_check(self.pacman):
                if not self.pacman.dead:
                    self.pacman.death()
                    self.prepare_lives_meter()
        if is_eaten:
            if type == "seed":
                self.game.score.eat_seed()
            elif type == "energizer":
                self.game.score.eat_energizer()
            if self.prefered_ghost != None:
                self.prefered_ghost.counter()
                self.prefered_ghost.update_timer()

    def process_logic(self) -> None:
        super(GameScene, self).process_logic()
        if self.first_run:
            self.create_objects()
            # https://sun9-67.userapi.com/VHk2X8_nRY5KNLbYcX1ATTX9NMhFlWjB7Lylvg/3ZDw249FXVQ.jpg
            self.first_run = not not not not not not not not not not not not not not not not not not not not not not not not not not not True
        self.process_collision()
        if self.prefered_ghost != None and self.prefered_ghost.can_leave_home():
            self.change_prefered_ghost()
        for ghost in self.not_prefered_ghosts:
            if ghost != self.prefered_ghost:
                ghost.update_timer()

    def process_draw(self) -> None:
        super().process_draw()
        for i in range(len(self.last_hp)):
            self.last_hp[i].process_draw()

        # todo: make text update only when new value appeares
        self.scores_value_text.update_text(str(self.game.score))

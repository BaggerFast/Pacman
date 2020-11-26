import pygame as pg

from misc import LevelLoader, Color, MAPS, CELL_SIZE, Font, get_image_path
from objects import SeedContainer, Map, ImageObject, Text, Pacman
from objects.ghosts import *
from scenes import BaseScene


class GameScene(BaseScene):

    def __init__(self, game):
        self.__loader = LevelLoader(MAPS[game.level_name])
        self.__map_data = self.__loader.get_map_data()
        self.__seed_data = self.__loader.get_seed_data()
        self.__energizer_data = self.__loader.get_energizer_data()
        self.__movements_data = self.__loader.get_movements_data()
        self.__player_position = self.__loader.get_player_position()
        self.__ghost_positions = self.__loader.get_ghost_positions()
        self.__fruit_position = self.__loader.get_fruit_position()
        self.first_run = not not not not not not not not not not not not not not not not not not not not not not not not not not not False
        self.__timer_reset_pacman = 0
        self.__seeds_eaten = 0
        self.__work_ghost_counters = True
        self.__max_seeds_eaten_to_prefered_ghost = 7
        super().__init__(game)

    def __prepare_lives_meter(self):
        self.__last_hp = []
        for i in range(self.__pacman.hp):
            hp_image = ImageObject(self.game, get_image_path('1.png', 'pacman', 'walk'), 5 + i * 20, 270)
            hp_image.rotate(180)
            self.__last_hp.append(hp_image)

    def create_objects(self) -> None:
        self.objects = []
        self.__map = Map(self.game, self.__map_data)
        self.objects.append(self.__map)
        self.__seeds = SeedContainer(self.game, self.__seed_data, self.__energizer_data)
        self.objects.append(self.__seeds)

        self.__scores_label_text = Text(self.game, 'SCORE', Font.MAIN_SCENE_SIZE,
                                        rect=pg.Rect(10, 0, 20, 20), color=Color.WHITE)
        self.objects.append(self.__scores_label_text)
        self.__scores_value_text = Text(self.game, str(self.game.score), Font.MAIN_SCENE_SIZE,
                                        rect=pg.Rect(10, 8, 20, 20), color=Color.WHITE)
        self.objects.append(self.__scores_value_text)

        self.__highscores_label_text = Text(self.game, 'HIGHSCORE', Font.MAIN_SCENE_SIZE,
                                            rect=pg.Rect(130, 0, 20, 20), color=Color.WHITE)
        self.objects.append(self.__highscores_label_text)
        self.__highscores_value_text = Text(self.game, str(self.game.records.data[-1]), Font.MAIN_SCENE_SIZE,
                                            rect=pg.Rect(130, 8, 20, 20), color=Color.WHITE)
        self.objects.append(self.__highscores_value_text)

        self.__pacman = Pacman(self.game, self.__player_position)

        self.objects.append(self.__pacman)
        self.__prepare_lives_meter()

        self.__blinky = Blinky(self.game, self.__ghost_positions[3])
        self.__pinky = Pinky(self.game, self.__ghost_positions[1])
        self.__inky = Inky(self.game, self.__ghost_positions[0])
        self.__clyde = Clyde(self.game, self.__ghost_positions[2])

        self.__ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]

        self.__not_prefered_ghosts = self.__ghosts.copy()

        self.__prefered_ghost = self.pinky
        self.__count_prefered_ghost = 0

        self.objects.append(self.blinky)
        self.objects.append(self.pinky)
        self.objects.append(self.inky)
        self.objects.append(self.clyde)

    @property
    def blinky(self):
        return self.__blinky

    @property
    def pinky(self):
        return self.__pinky

    @property
    def inky(self):
        return self.__inky

    @property
    def clyde(self):
        return self.__clyde

    @property
    def movements_data(self):
        return self.__movements_data

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.__start_pause()

    def __start_pause(self):
        self.game.set_scene('SCENE_PAUSE', reset=True)

    def additional_draw(self) -> None:
        # Temporary draw
        x_shift = 0
        y_shift = 20

        # fruit
        pg.draw.circle(self.screen, (255, 0, 0),
                       (x_shift + self.__fruit_position[0] * CELL_SIZE + CELL_SIZE // 2,
                        y_shift + self.__fruit_position[1] * CELL_SIZE + CELL_SIZE // 2), 4)

    def __change_prefered_ghost(self):
        if self.__prefered_ghost != None and self.__prefered_ghost.can_leave_home():
            self.__count_prefered_ghost += 1
            self.__not_prefered_ghosts.pop(0)
            if self.__count_prefered_ghost < 4:
                self.__prefered_ghost = self.__ghosts[self.__count_prefered_ghost]
            else:
                self.__prefered_ghost = None
                self.__count_prefered_ghost = 0

    def __process_collision(self) -> None:
        is_eaten, type = self.__seeds.process_collision(self.__pacman)
        for ghost in self.__ghosts:
            if ghost.collision_check(self.__pacman):
                self.__timer_reset_pacman = pg.time.get_ticks()
                if not self.__pacman.dead:
                    self.__pacman.death()
                    self.__prepare_lives_meter()
                # todo
                elif not self.__pacman.animator.run:
                    self.game.set_scene("SCENE_GAMEOVER")
                    break
                for ghost2 in self.__ghosts:
                    ghost2.invisible()
        if is_eaten:
            if type == "seed":
                self.game.score.eat_seed()
            elif type == "energizer":
                self.game.score.eat_energizer()
            if self.__prefered_ghost != None and self.__work_ghost_counters:
                self.__prefered_ghost.counter()
                self.__prefered_ghost.update_timer()
            elif not self.__work_ghost_counters and self.__prefered_ghost != None:
                self.global_counter()
                self.__prefered_ghost.update_timer()

    def global_counter(self):
        self.__seeds_eaten += 1

    def check_first_run(self):
        if self.first_run:
            self.create_objects()
            # https://sun9-67.userapi.com/VHk2X8_nRY5KNLbYcX1ATTX9NMhFlWjB7Lylvg/3ZDw249FXVQ.jpg
            self.first_run = not not not not not not not not not not not not not not not not not not not not not not not not not not not True

    def process_logic(self) -> None:
        super(GameScene, self).process_logic()
        self.check_first_run()
        self.__process_collision()
        if pg.time.get_ticks()-self.__timer_reset_pacman >= 3000 and self.__pacman.animator.anim_finished:
            self.create_objects()
            self.__seeds_eaten = 0
            self.__work_ghost_counters = False
            self.__max_seeds_eaten_to_prefered_ghost = 7
        if self.__seeds_eaten == self.__max_seeds_eaten_to_prefered_ghost and self.__prefered_ghost != None:
            self.__prefered_ghost.is_can_leave_home = True
            print(self.__max_seeds_eaten_to_prefered_ghost)
            if self.__max_seeds_eaten_to_prefered_ghost == 7:
                self.__max_seeds_eaten_to_prefered_ghost = 17
            elif self.__max_seeds_eaten_to_prefered_ghost == 17:
                self.__max_seeds_eaten_to_prefered_ghost = 32

        self.__change_prefered_ghost()
        for ghost in self.__ghosts:
            ghost.get_love_cell(self.__pacman, self.blinky)
        if self.__prefered_ghost is not None and self.__prefered_ghost.can_leave_home():
            self.__change_prefered_ghost()
        for ghost in self.__not_prefered_ghosts:
            if ghost != self.__prefered_ghost:
                ghost.update_timer()

    def process_draw(self) -> None:
        super().process_draw()
        for i in range(len(self.__last_hp)):
            self.__last_hp[i].process_draw()
        # todo: make text update only when new value appeares
        self.__scores_value_text.update_text(str(self.game.score))

    def on_deactivate(self) -> None:
        pass
        # self.game.records.set_new_record(int(self.game.score))
        # self.game.scenes["SCENE_GAME"] = GameScene(self.game)

    def on_activate(self) -> None:
        pass
        # self.game.scenes["SCENE_GAME"] = GameScene(self.game)

    def on_reset(self) -> None:
        self.game.score.reset()
        self.game.scenes["SCENE_GAME"] = GameScene(self.game)

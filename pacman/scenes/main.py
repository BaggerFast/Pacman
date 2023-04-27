import pygame as pg
from pygame.event import Event

from pacman.data_core import PathManager, Config
from pacman.data_core.enums import GameStateEnum, GhostStateEnum
from pacman.misc import ControlCheats, LevelLoader, Font, Health, INFINITY_LIVES
from pacman.misc.serializers import LevelStorage, MainStorage
from pacman.misc.util import is_esc_pressed
from pacman.objects import SeedContainer, Map, ImageObject, Text, Pacman
from pacman.objects.fruits import Fruit
from pacman.objects.ghosts import *
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class MainScene(BaseScene):

    # region COMPLETE:
    def __play_sound(self):
        if not self.game.sounds.siren.is_busy():
            self.game.sounds.siren.play()
        if self.pacman.animator != self.pacman.dead_anim:
            if any(ghost.state is GhostStateEnum.FRIGHTENED for ghost in self.__ghosts):
                self.game.sounds.siren.pause()
                if not self.game.sounds.pellet.is_busy():
                    self.game.sounds.pellet.play()
            else:
                self.game.sounds.siren.unpause()
                self.game.sounds.pellet.stop()

    def __create_start_anim(self):
        self.text = []
        for i, txt in enumerate(["READY", "GO!"]):
            self.text.append(Text(txt, 30, font=Font.TITLE, rect=pg.Rect(20, 0, 20, 20)))
            self.text[-1].move_center(Config.RESOLUTION.half_width, Config.RESOLUTION.half_height)

    def __create_hud(self):
        self.objects += [
            Text("HIGHSCORE", Font.MAIN_SCENE_SIZE, rect=pg.Rect(130, 0, 20, 20)),
            Text(
                f"{MainStorage().get_highscore()}",
                size=Font.MAIN_SCENE_SIZE,
                rect=pg.Rect(130, 8, 20, 20),
            ),
            Text(
                text="MEMORY" if self.game.skins.current.name == "chrome" else "SCORE",
                size=Font.MAIN_SCENE_SIZE,
                rect=pg.Rect(10, 0, 20, 20),
            ),
            self.__scores_value_text,
        ]
        for i in range(int(self.hp) - 1):
            self.objects.append(
                ImageObject(
                    PathManager.get_image_path(f"pacman/{self.game.skins.current.name}/walk/1"), (5 + i * 20, 270)
                ).rotate(180)
            )

    @property
    def movements_data(self):
        return self.__loader.get_movements_data()

    # endregion

    # region Intro

    def intro_logic(self) -> None:
        if self.state is not GameStateEnum.INTRO:
            return
        self.__start_label()
        if not self.game.sounds.intro.is_busy():
            self.state = GameStateEnum.ACTION
            self.text.clear()
            for ghost in self.__ghosts:
                ghost.update_timer()
                ghost.update_ai_timer()

    def __start_label(self) -> None:
        current_time = pg.time.get_ticks() / 1000
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.state_text = not self.state_text
        text_alpha = 255 if self.state_text else 0
        if current_time - self.start_time > self.intro_sound.sound.get_length() / 4 * 3:
            if len(self.text) > 1:
                del self.text[0]
        self.text[0].surface.set_alpha(text_alpha)

    # endregion

    # region Base

    def process_logic(self) -> None:
        match self.state:
            case GameStateEnum.INTRO:
                self.intro_logic()
            case GameStateEnum.ACTION:
                self.game_logic()

    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
        if self.state.INTRO:
            for txt in self.text[0:1]:
                txt.draw(screen)

    # endregion

    # region Old

    # def additional_logic(self) -> None:
    #     self.__scores_label_text.text = "MEMORY" if self.game.skins.current.name == "chrome" else "SCORE"
    #     self.__scores_value_text.text = (
    #         str(self.game.score) + " Mb" if self.game.skins.current.name == "chrome" else str(self.game.score)
    #     )
    #     self.__prepare_lives_meter()

    # endregion

    # region Temp

    def add_hp(self):
        self.hp += 1

    def on_enter(self) -> None:
        if self.pacman.animator != self.pacman.dead_anim:
            self.game.sounds.siren.unpause()
        if any(ghost.state is GhostStateEnum.FRIGHTENED for ghost in self.__ghosts):
            self.game.sounds.siren.pause()
            self.game.sounds.pellet.play()

    def on_exit(self) -> None:
        self.game.sounds.siren.stop()
        self.game.sounds.pellet.stop()

    # endregion

    def pre_init(self):
        self.game.sounds.intro.play()
        self.game.sounds.reload_sounds(self.game)
        self.state = GameStateEnum.INTRO
        self.__loader = LevelLoader(self.game.maps.levels[LevelStorage().current])
        self.__seed_data = self.__loader.get_seed_data()
        self.__energizer_data = self.__loader.get_energizer_data()
        self.slow_ghost_rect = self.__loader.get_slow_ghost_rect()
        self.__map = Map(self.__loader.get_map_data())

        self.game.score.reset()
        self.intro_sound = self.game.sounds.intro

        self.__create_start_anim()

        self.hp = Health(3, 4)

        self.__timer_reset_pacman = 0
        self.__seeds_eaten = 0

        self.fruit = Fruit(self.game, self.__loader.get_fruit_position())
        self.ghost_text_timer = pg.time.get_ticks()
        self.ghost_text_flag = False
        self.state_text = True

        self.__scores_value_text = Text(
            f"{'Mb' if self.game.skins.current.name == 'chrome' else self.game.score}",
            size=Font.MAIN_SCENE_SIZE,
            rect=pg.Rect(10, 8, 20, 20),
        )

    def _create_objects(self):
        super()._create_objects()
        self.__seeds_eaten = 0
        self.__timer_reset_pacman = 0
        self.ghost_text_flag = False
        self.ghost_text_timer = pg.time.get_ticks()
        self.__create_map()
        self.__create_characters()
        self.__create_hud()

        self.objects += [self.fruit, ControlCheats([["aezakmi", self.add_hp]])]

    def __create_map(self):
        self.__seeds = SeedContainer(self.game, self.__seed_data, self.__energizer_data)
        self.objects += [self.__map, self.__seeds]

    def __create_characters(self):
        hero_pos = self.__loader.get_hero_postions()
        seed_count = sum([1 for i in self.__seed_data for j in i if j])

        self.pacman = Pacman(self.game, hero_pos["pacman"])
        self.inky = Inky(self.game, hero_pos["inky"], seed_count)
        self.pinky = Pinky(self.game, hero_pos["pinky"], seed_count)
        self.clyde = Clyde(self.game, hero_pos["clyde"], seed_count)
        self.blinky = Blinky(self.game, hero_pos["blinky"], seed_count)
        self.__ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

        self.objects.append(self.pacman)
        for ghost in self.__ghosts:
            self.objects += [ghost, ghost.gg_text]

    def __change_prefered_ghost(self) -> None:
        for ghost in self.__ghosts:
            if ghost.is_in_home:
                ghost.home_ai(self.__seeds_eaten)

    def __process_collision(self) -> None:
        if self.fruit.process_collision(self.pacman.rect):
            self.game.sounds.fruit.play()
        elif self.__seeds.energizer_collision(self.pacman.rect):
            self.game.score.eat_energizer()
            for ghost in self.__ghosts:
                ghost.toggle_mode_to_frightened()
        elif self.__seeds.seed_collision(self.pacman.rect):
            self.__seeds_eaten += 1
            self.game.score.eat_seed()
            if not self.game.sounds.seed.is_busy():
                self.game.sounds.seed.play()
        else:
            for ghost in self.__ghosts:
                if ghost.collision_check(self.pacman.rect)[0]:
                    if ghost.collision_check(self.pacman.rect)[1]:
                        self.__timer_reset_pacman = pg.time.get_ticks()
                        if not self.pacman.dead and not INFINITY_LIVES:
                            self.hp -= 1
                            self.pacman.death()
                        for ghost2 in self.__ghosts:
                            ghost2.invisible()
                        break
                    if ghost.state is GhostStateEnum.FRIGHTENED:
                        ghost.gg_text.text = f"{200 * 2 ** self.game.score.fear_count}"
                        ghost.invisible()
                        self.game.score.eat_ghost()
                        self.ghost_text_flag = True
                        self.ghost_text_timer = pg.time.get_ticks()
                        ghost.toggle_mode_to_eaten()

    def check_game_status(self):
        if self.__seeds.is_field_empty():
            from pacman.scenes.game_win import GameWinScene
            SceneManager().reset(GameWinScene(self.game, self.game.score))
        elif self.pacman.dead_anim.anim_finished and int(self.hp) < 1 and not self.game.sounds.pacman.is_busy():
            from pacman.scenes.game_over import GameOverScene
            SceneManager().reset(GameOverScene(self.game, self.game.score))

    def update_score_text(self):
        self.__scores_value_text.text = f"{'Mb' if self.game.skins.current.name == 'chrome' else self.game.score}"

    def game_logic(self):
        super().process_logic()
        self.__play_sound()
        self.__change_prefered_ghost()
        self.__process_collision()
        self.update_score_text()
        if pg.time.get_ticks() - self.__timer_reset_pacman >= 3000 and self.pacman.animator.anim_finished:
            self._create_objects()
        if self.ghost_text_flag:
            if pg.time.get_ticks() - self.ghost_text_timer >= 500:
                for ghost in self.__ghosts:
                    ghost.visible()
                    ghost.gg_text.text = " "
                self.ghost_text_flag = False
        self.check_game_status()

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event) and self.state != GameStateEnum.INTRO:
            from pacman.scenes.pause import PauseScene
            SceneManager().append(PauseScene(self.game))

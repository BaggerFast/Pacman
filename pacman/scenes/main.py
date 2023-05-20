from pygame import Rect, Surface, time
from pygame.event import Event

from pacman.data_core import Cfg, FontCfg
from pacman.data_core.enums import GameStateEnum, GhostStateEnum
from pacman.misc import Health, LevelLoader, Score, is_esc_pressed, rand_color
from pacman.misic import Music
from pacman.objects import Fruit, ImgObj, Map, SeedContainer, Text
from pacman.objects.heroes import Blinky, Clyde, Inky, Pacman, Pinky
from pacman.storage import LevelStorage, SettingsStorage, SkinStorage
from pacman.tmp_skin import SkinEnum

from ..objects.cheat_codes import ControlCheats
from .base_scene import BaseScene
from .scene_manager import SceneManager


class MainScene(BaseScene):
    # region COMPLETE:

    def __init__(self, game, map_color=None):
        self._map_color = rand_color() if not map_color else map_color
        super().__init__(game)
        Music().update_random_sounds()

    def __play_sound(self):
        if not Music().BACK.is_busy():
            Music().BACK.play()
        if self.pacman.animator != self.pacman.dead_anim:
            if any(ghost.state is GhostStateEnum.FRIGHTENED for ghost in self.__ghosts):
                Music().BACK.pause()
                if not Music().FRIGHTENED.is_busy():
                    Music().FRIGHTENED.play()
            else:
                Music().BACK.unpause()
                Music().FRIGHTENED.stop()

    def __create_start_anim(self):
        self.text = []
        for i, txt in enumerate(["READY", "GO!"]):
            self.text.append(Text(txt, 30, rect=Rect(20, 0, 20, 20), font=FontCfg.TITLE))
            self.text[-1].move_center(Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height)

    def __create_hud(self):
        text = f"{'MAX MB' if SkinStorage().equals(SkinEnum.CHROME) else 'HIGHSCORE'}"
        self.objects += [
            Text(text, FontCfg.MAIN_SCENE_SIZE, rect=Rect(130, 0, 20, 20)),
            Text(f"{LevelStorage().get_highscore()}", size=FontCfg.MAIN_SCENE_SIZE, rect=Rect(130, 8, 20, 20)),
            Text(
                text="MEMORY" if SkinStorage().equals(SkinEnum.CHROME) else "SCORE",
                size=FontCfg.MAIN_SCENE_SIZE,
                rect=Rect(10, 0, 20, 20),
            ),
            self.__scores_value_text,
        ]

        for i in range(int(self.hp) - 1):
            image = ImgObj(SkinStorage().current_instance.walk.current_image, (5 + i * 16, 270))
            self.objects.append(image)

    # endregion

    # region Intro

    def intro_logic(self) -> None:
        if self.state is not GameStateEnum.INTRO:
            return
        self.__start_label()
        if not Music().INTRO.is_busy():
            self.state = GameStateEnum.ACTION
            self.text.clear()
            for ghost in self.__ghosts:
                ghost.update_ai_timer()

    def __start_label(self) -> None:
        current_time = time.get_ticks() / 1000
        if time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.state_text = not self.state_text
        text_alpha = 255 if self.state_text else 0
        if current_time - self._start_time > Music().INTRO.length / 4 * 3:
            if len(self.text) > 1:
                del self.text[0]
        self.text[0].set_alpha(text_alpha)

    # endregion

    # region Base

    def process_logic(self) -> None:
        if self.state in self.actions:
            self.actions[self.state]()

    def draw(self) -> Surface:
        super().draw()
        if self.state.INTRO:
            for txt in self.text[0:1]:
                txt.draw(self._screen)
        return self._screen

    # endregion

    # region Temp

    def on_enter(self) -> None:
        if self.pacman.animator != self.pacman.dead_anim:
            Music().BACK.unpause()
        if any(ghost.state is GhostStateEnum.FRIGHTENED for ghost in self.__ghosts):
            Music().BACK.pause()
            Music().FRIGHTENED.unpause()

    def on_exit(self) -> None:
        Music().BACK.stop()
        Music().FRIGHTENED.stop()

    # endregion

    def pre_init(self):
        self.actions = {
            GameStateEnum.INTRO: self.intro_logic,
            GameStateEnum.ACTION: self.game_logic,
        }

        self.score = Score()
        Music().INTRO.play()
        self.state = GameStateEnum.INTRO
        self.__loader = LevelLoader(self.game.maps.levels[LevelStorage().current])
        self.__seeds = SeedContainer(self.game, self.__loader.seeds_map, self.__loader.energizers_pos)
        self.__map = Map(self.__loader.map, self._map_color)
        self.__create_start_anim()
        hp = 3 - SettingsStorage().difficulty
        self.hp = Health(hp, 4)
        self.__seeds_eaten = 0
        self.fruit = Fruit(self.__loader.fruit_pos)
        self.state_text = True
        self.__scores_value_text = Text(
            f"{self.score} {'Mb' if SkinStorage().equals(SkinEnum.CHROME) else ''}",
            size=FontCfg.MAIN_SCENE_SIZE,
            rect=Rect(10, 8, 20, 20),
        )

    def _create_objects(self):
        super()._create_objects()
        self.__seeds_eaten = 0
        self.objects += [self.__map, self.__seeds, self.fruit]
        self.__create_characters()
        self.__create_hud()
        self.objects.append(ControlCheats([["aezakmi", self.hp.add]]))

    def __create_characters(self):
        self.pacman = Pacman(self.__loader)
        self.inky = Inky(self.__loader, len(self.__seeds))
        self.pinky = Pinky(self.__loader, len(self.__seeds))
        self.clyde = Clyde(self.__loader, len(self.__seeds))
        self.blinky = Blinky(self.__loader, len(self.__seeds))

        self.__ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

        self.objects += [self.pacman]
        self.objects.extend(self.__ghosts)

    def __change_prefered_ghost(self) -> None:
        for ghost in self.__ghosts:
            ghost.home_ai(self.__seeds_eaten)

    def __process_collision(self) -> None:
        pacman_rect = self.pacman.rect
        if self.fruit.process_collision(pacman_rect):
            Music().FRUIT.play()
            score = self.score.eat_fruit()
            self.fruit.toggle_mode_to_eaten(score)
        elif self.__seeds.energizer_collision(pacman_rect):
            self.score.eat_energizer()
            for ghost in self.__ghosts:
                ghost.toggle_mode_to_frightened()
        elif self.__seeds.seed_collision(pacman_rect):
            self.__seeds_eaten += 1
            self.score.eat_seed()
            if not Music().SEED.is_busy():
                Music().SEED.play()
        else:
            for ghost in self.__ghosts:
                if ghost.collision_check(pacman_rect):
                    if ghost.state is GhostStateEnum.FRIGHTENED:
                        score = self.score.eat_ghost()
                        ghost.toggle_to_hidden(score)
                        break
                    else:
                        if not self.pacman.is_dead:
                            self.hp.remove()
                            self.pacman.death()
                        break

    def __check_game_status(self):
        if self.__seeds.is_field_empty():
            from pacman.scenes.game_win import GameWinScene

            SceneManager().reset(GameWinScene(self.game, self._screen, int(self.score)))
        elif self.pacman.death_is_finished() and not Music().DEATH.is_busy():
            if self.hp:
                self._create_objects()
                return
            from pacman.scenes.game_over import GameOverScene

            SceneManager().reset(GameOverScene(self.game, self._screen, int(self.score)))

    def __update_score_text(self):
        self.__scores_value_text.text = f"{self.score} {'Mb' if SkinStorage().equals(SkinEnum.CHROME) else ''}"

    def game_logic(self):
        super().process_logic()
        self.__play_sound()
        self.__change_prefered_ghost()
        self.__process_collision()
        self.__update_score_text()
        self.__check_game_status()

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event) and self.state != GameStateEnum.INTRO:
            from pacman.scenes.pause import PauseScene

            SceneManager().append(PauseScene(self.game, self._screen))

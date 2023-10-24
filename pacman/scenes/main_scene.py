from typing import Generator

from pygame import Rect, Surface, time
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, FontCfg, PathUtl, event_append
from pacman.data_core.data_classes import Cheat
from pacman.data_core.enums import DifficultEnum, GameStateEnum, GhostStateEnum, SoundCh
from pacman.misc import HpSystem, ImgObj, LevelLoader, ScoreSystem, is_esc_pressed, rand_color
from pacman.objects import Blinky, CheatController, Clyde, Fruit, Inky, Map, Pacman, Pinky, SeedContainer, Text
from pacman.skin import SkinEnum
from pacman.sound import SoundController, Sounds
from pacman.storage import LevelStorage, SettingsStorage, SkinStorage

from .base import BaseScene, SceneManager


class MainScene(BaseScene):
    def __init__(self, map_color=None):
        super().__init__()

        self._map_color = rand_color() if not map_color else map_color

        self.actions = {
            GameStateEnum.INTRO: self.__intro_logic,
            GameStateEnum.ACTION: self.__game_logic,
        }
        self.__state = GameStateEnum.INTRO

        self.__anim_step = 125
        self._anim_timer = time.get_ticks() / 1000

        hp_value = len(DifficultEnum) - SettingsStorage().DIFFICULTY

        self.hp = HpSystem(hp_value, 4)

        self.__score = ScoreSystem()

        self.__loader = LevelLoader(PathUtl.get_asset(f"maps/{LevelStorage().current}.json"))

        self.__seeds_eaten = 0

        self.__state_text = True

        self.__scores_value_text = Text("", size=FontCfg.MAIN_SCENE_SIZE, rect=Rect(10, 8, 20, 20))
        self.__seeds = SeedContainer(self.__loader.seeds_map, self.__loader.energizers_pos, self.__anim_step)
        self.__into_text = self.__get__intro_text()
        self.__cheats = self.__get_cheats()
        self.__fruit = Fruit(self.__loader.fruit_pos)

        self.__create_heroes()

        self.__seeds.create_buffer()

        self.__update_score_text()

    # region Private

    def _generate_objects(self) -> Generator:
        self.__seeds_eaten = 0

        self.__create_heroes()

        yield Map(self.__loader.map, self._map_color)

        yield Text(
            "MEMORY" if SkinStorage().equals(SkinEnum.CHROME) else "SCORE", FontCfg.MAIN_SCENE_SIZE, Rect(10, 0, 20, 20)
        )

        yield Text(
            f"{'MAX MB' if SkinStorage().equals(SkinEnum.CHROME) else 'HIGHSCORE'}",
            FontCfg.MAIN_SCENE_SIZE,
            Rect(130, 0, 20, 20),
        )
        yield Text(f"{LevelStorage().get_highscore()}", FontCfg.MAIN_SCENE_SIZE, Rect(130, 8, 20, 20))
        yield self.__scores_value_text

        yield self.__seeds
        yield self.__fruit

        yield self.pacman

        for ghost in self.__ghosts:
            yield ghost

        for i in range(int(self.hp) - 1):
            yield ImgObj(SkinStorage().current_instance.walk.current_image, (5 + i * 16, 270))

    def __get_cheats(self) -> CheatController:
        from .lose_scene import LoseScene
        from .win_scene import WinScene

        return CheatController(
            [
                Cheat("aezakmi", self.hp.add),
                Cheat("god", lambda: SceneManager().reset(WinScene(self._screen, int(self.__score)))),
                Cheat("kill", lambda: SceneManager().reset(LoseScene(self._screen, int(self.__score)))),
            ]
        )

    @staticmethod
    def __get__intro_text() -> list[Text]:
        text = []
        for txt in ["READY", "GO!"]:
            text.append(
                Text(txt, 30, rect=Rect(20, 0, 20, 20), font=FontCfg.TITLE).move_center(
                    Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height
                )
            )
        return text

    def __create_heroes(self) -> None:
        self.pacman = Pacman(self.__loader)
        self.inky = Inky(self.__loader, len(self.__seeds))
        self.pinky = Pinky(self.__loader, len(self.__seeds))
        self.clyde = Clyde(self.__loader, len(self.__seeds))
        self.blinky = Blinky(self.__loader, len(self.__seeds))

        self.__ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __update_score_text(self):
        self.__scores_value_text.text = f"{self.__score} {'Mb' if SkinStorage().equals(SkinEnum.CHROME) else ''}"

    def __play_sound(self):
        if self.pacman.animator == self.pacman.dead_anim:
            return
        if any(ghost.state is GhostStateEnum.FRIGHTENED for ghost in self.__ghosts):
            SoundController.reset_play(SoundCh.BACKGROUND, Sounds.FRIGHTENED)
        else:
            SoundController.reset_play(SoundCh.BACKGROUND, Sounds.BACK)

    def __start_label(self) -> None:
        current_time = time.get_ticks() / 1000
        if time.get_ticks() - self._anim_timer > self.__anim_step:
            self.__state_text = not self.__state_text
            self._anim_timer = time.get_ticks()
        text_alpha = 255 if self.__state_text else 0
        if current_time - self._start_time > Sounds.INTRO.get_length() * 0.75:
            self._start_time = time.get_ticks()
            if len(self.__into_text) > 1:
                del self.__into_text[0]
        self.__into_text[0].set_alpha(text_alpha)

    def __process_collision(self) -> None:
        pacman_rect = self.pacman.rect
        if self.__fruit.process_collision(pacman_rect):
            SoundController.play(SoundCh.PLAYER, Sounds.FRUIT)
            score = self.__score.eat_fruit()
            self.__fruit.toggle_mode_to_eaten(score)
        elif self.__seeds.energizer_collision(pacman_rect):
            self.__score.eat_energizer()
            event_append(EvenType.GHOST_FRIGHTENED)
        elif self.__seeds.seed_collision(pacman_rect):
            self.__seeds_eaten += 1
            self.__score.eat_seed()
            SoundController.play_if_not_busy(SoundCh.PLAYER, Sounds.SEED)
        else:
            self.__check_ghost_collision()

    def __check_ghost_collision(self):
        for ghost in self.__ghosts:
            if not ghost.collision_check(self.pacman.rect):
                continue
            if ghost.state is GhostStateEnum.FRIGHTENED:
                score = self.__score.eat_ghost()
                ghost.toggle_to_hidden(score)
                break
            if not self.pacman.is_dead:
                self.hp.remove()
                SoundController.stop(SoundCh.BACKGROUND)
                SoundController.reset_play(SoundCh.PLAYER, Sounds.DEATH)
                self.pacman.death()
            return

    def __check_game_status(self):
        if self.__seeds.is_field_empty():
            from pacman.scenes.win_scene import WinScene

            SceneManager().reset(WinScene(self._screen, int(self.__score)))
        elif self.pacman.death_is_finished() and not SoundController.is_busy(SoundCh.PLAYER):
            if self.hp:
                self.setup()
                return
            from pacman.scenes.lose_scene import LoseScene

            SceneManager().reset(LoseScene(self._screen, int(self.__score)))

    def __intro_logic(self) -> None:
        if self.__state is not GameStateEnum.INTRO:
            return
        self.__start_label()
        if not SoundController.is_busy(SoundCh.BACKGROUND):
            self.__state = GameStateEnum.ACTION
            self.__into_text.clear()
            for ghost in self.__ghosts:
                ghost.update_ai_timer()

    def __ghost_ai(self) -> None:
        for ghost in self.__ghosts:
            ghost.home_ai(self.__seeds_eaten)

    def __game_logic(self):
        super().process_logic()
        self.__play_sound()
        self.__ghost_ai()
        self.__process_collision()
        self.__update_score_text()
        self.__check_game_status()

    # endregion

    # region Public

    def process_logic(self) -> None:
        if self.__state in self.actions:
            self.actions[self.__state]()
        self.__cheats.update()

    def draw(self) -> Surface:
        super().draw()
        if self.__state.INTRO:
            for txt in self.__into_text[0:1]:
                txt.draw(self._screen)
        return self._screen

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            from pacman.scenes.pause_scene import PauseScene

            SceneManager().append(PauseScene(self._screen))
        self.__cheats.event_handler(event)

    def on_enter(self) -> None:
        for ch in SoundCh:
            SoundController.unpause(ch)

    def on_exit(self) -> None:
        for ch in SoundCh:
            SoundController.pause(ch)

    def on_first_enter(self) -> None:
        Sounds.update_random_sounds()
        SoundController.play(SoundCh.BACKGROUND, Sounds.INTRO)

    def on_last_exit(self) -> None:
        for ch in SoundCh:
            SoundController.stop(ch)

    # endregion

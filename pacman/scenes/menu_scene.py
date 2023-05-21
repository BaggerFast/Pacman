from pygame import Rect, Surface
from pygame.event import Event

from pacman.data_core import Cfg, Colors, EvenType, FontCfg, event_append
from pacman.misc import ImgObj, is_esc_pressed, rand_color
from pacman.objects import Text
from pacman.objects.buttons import Btn, ButtonController
from pacman.storage import LevelStorage, SkinStorage

from .base import BaseScene, SceneManager


class MenuScene(BaseScene):
    def _create_objects(self) -> None:
        super()._create_objects()
        self.__map_color = rand_color()
        self.preview = self.generate_map_preview()
        self.__level_text = Text(f"{LevelStorage()}", 15, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 60)
        self.objects += [
            Text("PACMAN", 36, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30),
            self.__level_text,
        ]
        self.pacman_anim = SkinStorage().current_instance.walk
        self.create_buttons()

    def play_game(self) -> None:
        from pacman.scenes.main_scene import MainScene

        event_append(EvenType.SET_SETTINGS)
        SceneManager().append(MainScene(self.game, self.__map_color))

    def create_buttons(self) -> None:
        from .levels_scene import LevelsScene
        from .records_scene import RecordsScene
        from .settings_scene import SettingsScene
        from .skins_scene import SkinsScene

        scene_manager = SceneManager()
        names = [
            ("PLAY", self.play_game),
            ("LEVELS", lambda: scene_manager.append(LevelsScene(self.game))),
            ("SKINS", lambda: scene_manager.append(SkinsScene(self.game))),
            ("RECORDS", lambda: scene_manager.append(RecordsScene(self.game))),
            ("SETTINGS", lambda: scene_manager.append(SettingsScene(self.game))),
            ("EXIT", lambda: event_append(EvenType.EXIT)),
        ]
        buttons = []
        for i, (name, fn) in enumerate(names):
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 180, 26),
                    text=name,
                    function=fn,
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width // 1.5, 92 + i * 28)
            )
        self.objects.append(ButtonController(buttons))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            self.preview = self.generate_map_preview()

    def draw(self) -> Surface:
        self.preview.draw(self._screen)
        self.objects.draw(self._screen)
        ImgObj(self.pacman_anim.current_image).scale(75, 75).move_center(
            Cfg.RESOLUTION.h_width + Cfg.RESOLUTION.h_width // 2, Cfg.RESOLUTION.h_height
        ).draw(self._screen)
        return self._screen

    def process_logic(self) -> None:
        self.pacman_anim.update()

    def generate_map_preview(self) -> ImgObj:
        self.__map_color = rand_color()
        return (
            ImgObj(self.game.maps.full_surface)
            .swap_color(Colors.MAIN_MAP, self.__map_color)
            .scale(*tuple(Cfg.RESOLUTION))
            .blur(3)
        )

    def on_enter(self) -> None:
        self.pacman_anim = SkinStorage().current_instance.walk
        self.__level_text.text = f"{LevelStorage()}"

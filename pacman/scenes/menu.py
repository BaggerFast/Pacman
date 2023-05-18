from pygame import Rect, Surface
from pygame.event import Event

from pacman.data_core import Cfg, Colors
from pacman.events.events import EvenType
from pacman.events.utils import event_append
from pacman.misc.constants import Font
from pacman.misc.serializers import LevelStorage
from pacman.misc.util import is_esc_pressed, rand_color
from pacman.objects import ImageObject, Text
from pacman.objects.buttons import Button, ButtonController
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class MenuScene(BaseScene):
    def _create_objects(self) -> None:
        super()._create_objects()
        self.__map_color = rand_color()
        self.preview = self.generate_map_preview()
        self.__level_text = Text(f"{LevelStorage()}", 15, font=Font.TITLE).move_center(Cfg.RESOLUTION.half_width, 60)
        self.objects += [
            Text("PACMAN", 36, font=Font.TITLE).move_center(Cfg.RESOLUTION.half_width, 30),
            self.__level_text,
        ]
        self.create_buttons()

    def play_game(self) -> None:
        from pacman.scenes.main import MainScene

        event_append(EvenType.SET_SETTINGS)
        SceneManager().append(MainScene(self.game, self.__map_color))

    def create_buttons(self) -> None:
        from pacman.scenes.levels import LevelsScene
        from pacman.scenes.records import RecordsScene
        from pacman.scenes.settings import SettingsScene
        from pacman.scenes.skins import SkinsScene

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
                Button(
                    rect=Rect(0, 0, 180, 26),
                    text=name,
                    function=fn,
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.half_width, 95 + i * 28)
            )
        self.objects.append(ButtonController(buttons))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            self.preview = self.generate_map_preview()

    def draw(self) -> Surface:
        self.preview.draw(self._screen)
        self.objects.draw(self._screen)
        return self._screen

    def generate_map_preview(self) -> ImageObject:
        self.__map_color = rand_color()
        return (
            ImageObject(self.game.maps.full_surface)
            .swap_color(Colors.MAIN_MAP, self.__map_color)
            .scale(*tuple(Cfg.RESOLUTION))
            .blur(3)
        )

    def on_enter(self) -> None:
        self.__level_text.text = f"{LevelStorage()}"

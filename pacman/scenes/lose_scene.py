from pygame import Rect, Surface

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.objects import Btn, ButtonController, Text
from pacman.sound import SoundController
from pacman.storage import LevelStorage

from .base import BlurScene, SceneManager


class LoseScene(BlurScene):
    def __init__(self, game, blur_surface: Surface, score: int):
        super().__init__(game, blur_surface)
        self.score = score

    def _create_objects(self) -> None:
        super()._create_objects()
        self.objects += [
            Text("GAME", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30),
            Text("OVER", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 70),
            Text(f"Score: {self.score}", 20).move_center(Cfg.RESOLUTION.h_width, 135),
            Text(f"High score: {LevelStorage().get_highscore()}", 20).move_center(Cfg.RESOLUTION.h_width, 165),
        ]
        self.create_buttons()

    def create_buttons(self) -> None:
        from .main_scene import MainScene
        from .menu_scene import MenuScene

        names = [
            ("RESTART", lambda: SceneManager().reset(MainScene(self.game))),
            ("MENU", lambda: SceneManager().reset(MenuScene(self.game))),
        ]
        buttons = []
        for i, (name, fn) in enumerate(names):
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 180, 35),
                    text=name,
                    function=fn,
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width, 210 + 40 * i)
            )
        self.objects.append(ButtonController(buttons))

    def on_enter(self) -> None:
        event_append(EvenType.GET_SETTINGS)
        SoundController().LOSE.play()

    def on_exit(self) -> None:
        SoundController().LOSE.stop()

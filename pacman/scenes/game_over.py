from pygame import Rect, Surface

from pacman.data_core import Cfg, EvenType, event_append, FontCfg
from pacman.misic import Music
from pacman.objects import Text
from pacman.objects.buttons import Btn, ButtonController
from pacman.storage import LevelStorage
from .blur_scene import BlurScene
from .scene_manager import SceneManager


class GameOverScene(BlurScene):
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
        from .main import MainScene
        from .menu import MenuScene

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
        Music().LOSE.play()

    def on_exit(self) -> None:
        Music().LOSE.stop()

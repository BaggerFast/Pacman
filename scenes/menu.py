from constants import Color
from objects import ButtonObject
from scenes import BaseScene


class MenuScene(BaseScene):
    def create_objects(self) -> None:
        self.button_start = ButtonObject(
            self.game,
            self.game.WIDTH // 2 - 100, self.game.HEIGHT // 2 - 20 - 25, 200, 50,
            Color.RED, self.start_game, "Запуск игры"
        )
        self.button_exit = ButtonObject(
            self.game,
            self.game.WIDTH // 2 - 100, self.game.HEIGHT // 2 + 25, 200, 50,
            Color.RED, self.game.exit_game, 'Выход'
        )
        self.objects = [self.button_start, self.button_exit]

    def start_game(self) -> None:
        self.game.set_scene(self.game.MAIN_SCENE_INDEX)

    def on_window_resize(self) -> None:
        self.button_start.move(self.game.WIDTH // 2 - 100, self.game.HEIGHT // 2 - 20 - 25)
        self.button_exit.move(self.game.WIDTH // 2 - 100, self.game.HEIGHT // 2 + 25)

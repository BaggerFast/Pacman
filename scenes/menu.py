from constants import Color
from objects.button import ButtonObject
from scenes.base import BaseScene


class MenuScene(BaseScene):
    def create_objects(self):
        self.button_start = ButtonObject(
            self.game,
            self.game.width // 2 - 100, self.game.height // 2 - 20 - 25, 200, 50,
            Color.RED, self.start_game, "Запуск игры"
        )
        self.button_exit = ButtonObject(
            self.game,
            self.game.width // 2 - 100, self.game.height // 2 + 25, 200, 50,
            Color.RED, self.game.exit_game, 'Выход'
        )
        self.objects = [self.button_start, self.button_exit]

    def start_game(self):
        self.game.set_scene(self.game.MAIN_SCENE_INDEX)

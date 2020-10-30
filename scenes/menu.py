from constants import Color
from objects.button import ButtonObject
from scenes.base import Scene


class MenuScene(Scene):
    def create_objects(self):
        self.button_start = ButtonObject(self.game, 350, 255, 100, 40, Color.WHITE, self.set_main_scene, "Запуск игры")
        self.button_exit = ButtonObject(self.game, 350, 305, 100, 40, Color.WHITE, self.exit, 'Выход')
        self.objects = [self.button_start, self.button_exit]

    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True
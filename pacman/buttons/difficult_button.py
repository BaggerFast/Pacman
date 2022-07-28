from misc.storage import SettingStorage
from .button import Button


class DifficultyButton(Button):
    __dificulties = {
        0: "easy",
        1: "medium",
        2: "hard"
    }

    def __init__(self, **args):
        super().__init__(**args)
        self.value = SettingStorage().difficulty
        self.update_text()

    def click(self) -> None:
        self.value += 1
        if self.value > 2:
            self.value = 0
        self.update_text()
        self.select()
        SettingStorage().difficulty = self.value

    def update_text(self):
        self.text = self.__dificulties[self.value]

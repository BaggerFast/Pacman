from objects.button import Button


class DifficultyButton(Button):
    __difficulties = [
        "easy",
        "medium",
        "hard"
    ]

    def __init__(self, **args):
        super().__init__(**args)
        self.update_text()

    def click(self) -> None:
        self.game.sounds.click.play()
        self.game.settings.DIFFICULTY = (self.game.settings.DIFFICULTY + 1) % 3
        self.update_text()
        self.select()

    def update_text(self) -> None:
        self.text = self.__difficulties[self.game.settings.DIFFICULTY]

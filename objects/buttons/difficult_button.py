from objects.buttons import Button


class DifficultyButton(Button):
    __difficulties = [
        "easy",
        "medium",
        "hard"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_text()

    def click(self) -> None:
        self.game.sounds.click.play()
        self.game.settings.change_difficulty()
        self.update_text()
        self.select()

    def update_text(self) -> None:
        self.text = self.__difficulties[self.game.settings.DIFFICULTY]

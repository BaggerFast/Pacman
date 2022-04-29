from serializers.serializers import SettingsSerializer
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
    # region Public

    def click(self) -> None:
        self.game.sounds.click.play()
        SettingsSerializer().difficulty += 1
        self.update_text()
        self.select()

    def update_text(self) -> None:
        self.text = self.__difficulties[SettingsSerializer().difficulty]

    # endregion

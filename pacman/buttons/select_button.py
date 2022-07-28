from misc.storage import SettingStorage
from .button import Button


class SelectButton(Button):
    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    def click(self) -> None:
        SettingStorage().volume += self.value
        self.game.scenes.current.volume_value.text = f'{SettingStorage().volume}%'
        for sound in self.game.sounds.__dict__.keys():
            self.game.sounds.__dict__[sound].update()

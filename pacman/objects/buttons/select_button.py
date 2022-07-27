from pacman.objects.buttons import Button
from pacman.serializers import SettingsSerializer


class SelectButton(Button):

    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    def click(self) -> None:
        self.select()
        self.game.sounds.click.play()
        SettingsSerializer().volume += self.value
        self.game.scene_manager.scenes[-1].volume_value.text = f"{ SettingsSerializer().volume} %"

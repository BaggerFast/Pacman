from pacman.misc.constants import BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from pacman.objects.buttons import Button
from pacman.serializers import SettingsSerializer


class SettingButton(Button):

    def __init__(self, **args):
        self.name, self.var = args.pop("name"), args.pop("var")
        super().__init__(**args)

    # region Public

    def update(self, var: str) -> None:
        if var in ["SOUND", "FUN"]:
            self.game.sounds.reload_sounds()

    def click(self) -> None:
        self.game.sounds.click.play()
        self.select()
        if not hasattr(SettingsSerializer(), self.var):
            return
        active_mode = not getattr(SettingsSerializer(), self.var)
        setattr(SettingsSerializer(), self.var, active_mode)
        self.update(self.var)
        self.text = f"{self.name} {'ON' if active_mode else 'OFF'}"
        self.colors = BUTTON_GREEN_COLORS if active_mode else BUTTON_RED_COLORS

    # endregion

from .button import Button


class SettingButton(Button):

    def __init__(self, game, name, i, var):
        pass
        # flag_var = getattr(game.settings, var)
        # super().__init__(
        #     game=game,
        #     geometry=pg.Rect(0, 0, 180, 35),
        #     text=name + (" ON" if flag_var else " OFF"),
        #     center=(game.width // 2, 75 + i * 40),
        #     text_size=Font.BUTTON_TEXT_SIZE,
        #     colors=BUTTON_GREEN_COLORS if flag_var else BUTTON_RED_COLORS,
        # )
        # self.name = name
        # self.var = var

    def update(self, var):
        if var == "MUTE" or var == "FUN":
            sounds = self.game.sounds.__dict__
            for sound in sounds.keys():
                sounds[sound].update()

    def click(self):
        pass
        # flag_var = not getattr(self.game.settings, self.var)
        # setattr(self.game.settings, self.var, flag_var)
        # if flag_var:
        #     self.text = self.name + " ON"
        #     self.colors = BUTTON_GREEN_COLORS
        # else:
        #     self.text = self.name + " OFF"
        #     self.colors = BUTTON_RED_COLORS
        # self.update(self.var)

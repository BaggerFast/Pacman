from objects.button import Button


class SelectButton(Button):

    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    def click(self) -> None:
        self.game.sounds.click.play()
        self.select()
        self.game.settings.change_volume(self.value)
        self.game.scene_manager.scenes[-1].volume_value.text = f"{self.game.settings.VOLUME} %"

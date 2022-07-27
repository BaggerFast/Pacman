from pacman.objects.buttons import Button


class SkinButton(Button):

    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    # region Public

    def click(self) -> None:
        self.game.sounds.click.play()
        self.game.skins.current = self.value
        self.select()
        # self.game.scenes.current.update_button_text()

    def deselect(self) -> None:
        scene = self.game.scene_manager.current
        scene.preview.image = self.game.skins.current.image.image
        super().deselect()

    def select(self) -> None:
        scene = self.game.current_scene
        scene.is_current = True
        scene.preview.image = self.value.image.image
        super().select()

    # endregion

from .button import Button


class SceneButton(Button):
    def __init__(self, **args):
        self.scene = args.pop("scene")
        super().__init__(**args)

    def click(self) -> None:
        if callable(self.scene[0]):
            self.scene[0]()
        else:
            self.game.scenes.set(self.scene[0], reset=self.scene[1])

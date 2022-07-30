from .button import Button


class LvlButton(Button):

    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    def click(self):
        self.game.maps.cur_id = self.value[0]
        self.game.records.update_records()
        self.game.scenes.set(self.game.scenes.MENU, reset=True)

    def select(self) -> None:
        self.game.scenes.current.is_current = True
        self.game.scenes.current.preview.image = self.value[1].image

        super().select()

    def deselect(self) -> None:
        if not self.game.scenes.current.is_current:
            self.game.scenes.current.preview.image = self.game.maps.images[self.game.maps.cur_id].image

        super().deselect()

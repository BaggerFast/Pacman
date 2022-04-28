import scenes
from objects.buttons import Button


class LvlButton(Button):

    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    # region Public

    def click(self):
        self.game.sounds.click.play()
        self.game.maps.cur_id = self.value[0]
        # self.game.records.update_records()
        self.game.scene_manager.pop()

    def select(self) -> None:
        self.game.scene_manager.scenes[-1].is_current = True
        self.game.scene_manager.scenes[-1].preview.image = self.value[1].image
        super().select()

    def deselect(self) -> None:
        if not self.game.scene_manager.scenes[-1].is_current:
            self.game.scene_manager.current.preview.image = self.game.maps.images[self.game.maps.cur_id].image
        super().deselect()

    # endregion

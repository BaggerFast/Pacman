from .button import Button


class BuyButton(Button):
    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    def click(self) -> None:
        flag = True
        for key in self.value[1].skin_cost.keys():
            if self.game.eaten_fruits[key] < self.value[1].skin_cost[key]:
                flag = False

        self.select()
        if flag:
            for key in self.value[1].skin_cost.keys():
                self.game.store_fruit(key, -self.value[1].skin_cost[key])
            self.game.unlock_skin(self.value[1].name)
            self.game.scenes.current.create_objects()

    def deselect(self) -> None:
        scene = self.game.scenes.current
        if not scene.is_current:
            scene.preview.image = self.game.skins.current.image.image
        super().deselect()

    def select(self) -> None:
        scene = self.game.scenes.current
        scene.is_current = True
        scene.preview.image = self.value[1].image.image
        super().select()

from objects.buttons import Button


class BuyButton(Button):
    def __init__(self, **args):
        self.value = args.pop("value")
        super().__init__(**args)

    def click(self) -> None:
        self.game.sounds.click.play()
        flag = True
        self.select()
        for key in self.value.skin_cost.keys():
            flag = self.game.eaten_fruits[key] > self.value.skin_cost[key]
        if not flag:
            return
        for key in self.value.skin_cost.keys():
            self.game.store_fruit(key, -self.value.skin_cost[key])
        self.game.unlock_skin(self.value.name)
        self.game.scenes.current.create_objects()

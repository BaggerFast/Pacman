import pygame as pg


class Scene:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.static_object = []
        self.create_static_objects()

    def process_event(self, event: pg.event.Event) -> None:
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def process_logic(self) -> None:
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def process_draw(self) -> None:
        for item in self.objects:
            item.process_draw()
        self.additional_draw()

    def create_static_objects(self):
        pass

    def create_objects(self) -> None:
        self.objects = []
        self.create_buttons()

    def on_activate(self) -> None:
        self.create_objects()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MENU)

    def additional_logic(self) -> None:
        pass

    def additional_draw(self) -> None:
        for item in self.static_object:
            item.process_draw()

    def on_deactivate(self) -> None:
        pass

    def on_reset(self) -> None:
        pass

    def create_buttons(self):
        pass

    def recreate(self) -> None:
        self.create_static_objects()
        self.create_objects()


class SubScene(Scene):
    def __init__(self, game, rect: pg.rect):
        super(SubScene, self).__init__(game)
        self.rect = rect
        self.screen = pg.Surface(rect)

    def process_draw(self) -> None:
        super(SubScene, self).process_draw()
        self.game.screen.blit(self.screen, self.rect)

    def recreate(self) -> None:
        self.__init__(self.game, self.rect)

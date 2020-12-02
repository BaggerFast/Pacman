import pygame as pg


class Scene:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.pre_init()
        self.create_objects()

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

    def create_objects(self) -> None:
        pass

    def on_activate(self) -> None:
        pass

    def additional_event_check(self, event: pg.event.Event) -> None:
        pass

    def additional_logic(self) -> None:
        pass

    def additional_draw(self) -> None:
        pass

    def on_deactivate(self) -> None:
        pass

    def on_reset(self) -> None:
        pass

    def recreate(self) -> None:
        self.pre_init()
        self.objects = []
        self.create_objects()

    def pre_init(self):
        pass

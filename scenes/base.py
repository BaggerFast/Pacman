import pygame


class BaseScene:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.create_objects()

    def create_objects(self) -> None:
        pass

    def on_activate(self) -> None:
        pass

    def on_window_resize(self) -> None:
        pass

    def process_event(self, event: pygame.event.Event) -> None:
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def additional_logic(self) -> None:
        pass

    def process_draw(self) -> None:
        for item in self.objects:
            item.process_draw()
        self.additional_draw()

    def additional_draw(self) -> None:
        pass

    def on_deactivate(self) -> None:
        pass

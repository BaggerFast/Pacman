import pygame as pg


class BasePattern:

    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass

    def process_draw(self) -> None:
        pass

    def additional_event_check(self, event: pg.event.Event) -> None:
        pass

    def additional_logic(self) -> None:
        pass

    def additional_draw(self) -> None:
        pass


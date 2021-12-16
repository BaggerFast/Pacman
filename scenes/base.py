from collections import Generator
import pygame as pg
from objects.button import ButtonController


class BaseScene:

    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = self.game.screen
        self.scene_manager = self.game.scene_manager

        self.objects: list = []
        self.static_objects: list = []

        self.start_logic()
        self.create_static_objects()
        self.create_objects()

    def start_logic(self):
        pass

    def process_event(self, event: pg.event.Event) -> None:
        for obj in self.objects:
            obj.process_event(event)
        self.additional_event_check(event)

    def process_logic(self) -> None:
        for obj in self.objects:
            obj.process_logic()
        self.additional_logic()

    def process_draw(self, blur_count: int = 0) -> None:
        all_objects = self.objects+self.static_objects
        for obj in all_objects:
            obj.process_draw()
        self.additional_draw()
        """"if blur_count:
            surify = pg.image.tostring(self.screen, 'RGBA')
            impil = Image.frombytes('RGBA', (224, 285), surify)
            piler = impil.filter(ImageFilter.GaussianBlur(radius=blur_count))
            surface = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()
            self.screen.blit(surface, (0, 0)) """

    def create_static_objects(self) -> None:
        self.create_title()

    def create_objects(self) -> None:
        buttons = list(self.button_init())
        if buttons:
            self.objects.append(ButtonController(self.game, buttons))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.scene_manager.pop()

    def additional_logic(self) -> None:
        pass

    def additional_draw(self) -> None:
        pass

    def create_title(self) -> None:
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def button_init(self) -> Generator:
        yield []

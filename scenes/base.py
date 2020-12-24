import pygame as pg
from PIL import ImageFilter, Image

from objects.button import Button


class Scene:
    class SceneButton(Button):
        def __init__(self, **args):
            args["function"] = args.pop("scene")
            super(Scene.SceneButton, self).__init__(**args)

    def __init__(self, game):
        self.game = game
        self.prev_scene = None
        self.screen: pg.Surface = self.game.screen
        self.objects: list = []
        self.static_objects = []
        self.create_static_objects()

    def process_event(self, event: pg.event.Event) -> None:
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def process_logic(self) -> None:
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def process_draw(self, blur_count: int = 0) -> None:
        for item in self.objects:
            item.process_draw()
        self.additional_draw()
        if blur_count:
            surify = pg.image.tostring(self.screen, 'RGBA')
            impil = Image.frombytes('RGBA', (224, 285), surify)
            piler = impil.filter(
                ImageFilter.GaussianBlur(radius=blur_count))
            surface = pg.image.fromstring(
                piler.tobytes(), piler.size, piler.mode).convert()
            self.screen.blit(surface, (0, 0))

    def create_static_objects(self) -> None:
        self.create_title()

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
        for item in self.static_objects:
            item.process_draw()

    def on_deactivate(self) -> None:
        pass

    def on_reset(self) -> None:
        pass

    def create_buttons(self) -> None:
        pass

    def create_title(self) -> None:
        pass

    def recreate(self) -> None:
        self.objects = []
        self.static_objects = []
        self.create_static_objects()

    def __call__(self, *args, **kwargs):
        self.game.scenes.set(self)

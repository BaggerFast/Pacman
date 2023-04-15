import pygame as pg

from pacman.data_core.game_objects import GameObjects


class Scene:
    def __init__(self, game) -> None:
        self.game = game
        self.prev_scene = None
        self.screen: pg.Surface = self.game.screen
        self.objects = GameObjects()
        self.static_objects = GameObjects()
        self.create_static_objects()

    def click_btn(self, scene, status):
        self.game.sounds.click.play()
        if callable(scene):
            scene()
        else:
            self.game.scenes.set(scene, reset=status)

    def process_event(self, event: pg.event.Event) -> None:
        self.objects.event_handler(event)
        self.additional_event_check(event)

    def process_logic(self) -> None:
        self.objects.update()
        self.additional_logic()

    def process_draw(self, screen: pg.Surface) -> None:
        self.objects.draw(screen)
        self.additional_draw(screen)

    def create_static_objects(self) -> None:
        self.create_title()

    def create_objects(self) -> None:
        self.objects = GameObjects()
        self.create_buttons()

    def on_activate(self) -> None:
        self.create_objects()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MENU)

    def additional_logic(self) -> None:
        pass

    def additional_draw(self, screen: pg.Surface) -> None:
        for item in self.static_objects:
            item.draw(screen)

    def on_deactivate(self) -> None:
        pass

    def on_reset(self) -> None:
        pass

    def create_buttons(self) -> None:
        pass

    def create_title(self) -> None:
        pass

    def recreate(self) -> None:
        self.__init__(self.game)

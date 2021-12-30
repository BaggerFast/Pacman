from copy import copy
import pygame as pg
from misc import Font
from objects.button import ButtonController, LvlButton, Button
from objects import Text
from scenes.base import BaseScene


class LevelsScene(BaseScene):
    __buttons_on_scene = 4

    def create_static_objects(self):
        self.is_current = False
        self.__scroll = max(min(self.game.maps.cur_id, self.game.maps.count - self.__buttons_on_scene), 0)
        self.__create_title()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def button_init(self):
        for i in range(self.__scroll, self.__scroll + self.__buttons_on_scene):
            yield LvlButton(
                game=self.game,
                rect=pg.Rect(0, 0, 100, 40),
                value=(i, self.game.maps.images[i]),
                text=f'LEVEL {i + 1}',
                center=(self.game.width // 2 - 55, (85 + 40 * (i - self.__scroll))),
                text_size=Font.BUTTON_TEXT_SIZE - 4,
                active=i in self.game.unlocked_levels)
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=self.game.scene_manager.pop,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

    def create_buttons(self) -> None:
        button_controller = ButtonController(self.game, list(self.button_init()))
        for button in button_controller.buttons:
            if hasattr(button, "value"):
                if self.game.maps.cur_id == button.value[0]:
                    button.text = '-' + button.text + '-'
        self.objects.append(button_controller)

    def unlocked(self) -> int:
        return len(self.game.unlocked_levels)

    def create_objects(self) -> None:
        self.objects = []
        self.preview = copy(self.game.maps.images[self.game.maps.cur_id])
        self.objects.append(self.preview)
        self.create_buttons()

    def scroll_threshold(self) -> None:
        self.__scroll = min(self.__scroll, self.game.maps.count - self.__buttons_on_scene)
        self.__scroll = max(self.__scroll, 0)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEWHEEL:
            self.__scroll -= event.y
            self.scroll_threshold()
            self.create_objects()
        elif event.type == pg.KEYDOWN and not (event.key in [pg.K_e, pg.K_q]):
            if event.key == pg.K_e:
                self.__scroll += 1
            elif event.key == pg.K_q:
                self.__scroll -= 1
            self.scroll_threshold()
            self.create_objects()
        super().additional_event_check(event)


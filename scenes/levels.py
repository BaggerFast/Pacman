from copy import copy
import pygame as pg
from misc import Font, EvenType
from objects.buttons import ButtonController, LvlButton, Button
from objects import Text
from scenes.base import BaseScene


class LevelsScene(BaseScene):
    __buttons_on_scene = 4

    def start_logic(self):
        self.is_current = False
        self.__scroll = max(min(self.game.maps.cur_id, self.game.maps.count - self.__buttons_on_scene), 0)

    def create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        title2 = Text(self.game, 'Scroll - [q, e]', 15, font=Font.DEFAULT)
        title2.move_center(self.game.width // 2, 50)
        self.objects += [title, title2]

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
        buttons = list(self.button_init())
        for button in buttons:
            if hasattr(button, "value") and self.game.maps.cur_id == button.value[0]:
                button.text = '-' + button.text + '-'
        self.objects.append(ButtonController(self.game, buttons))

    def create_objects(self) -> None:
        self.preview = copy(self.game.maps.images[self.game.maps.cur_id])
        self.objects.append(self.preview)
        self.create_buttons()

    def update_scroll(self, index: int) -> None:
        self.__scroll = min(self.__scroll+index, self.game.maps.count - self.__buttons_on_scene)
        self.__scroll = max(self.__scroll, 0)

    def additional_event_check(self, event: pg.event.Event) -> None:
        actions = {
            pg.K_e: lambda: self.update_scroll(1),
            pg.K_q: lambda: self.update_scroll(-1),
        }
        if event.type == pg.MOUSEWHEEL:
            self.update_scroll(-event.y)
            self.recreate()
        elif event.type == pg.KEYDOWN and event.key in actions.keys():
            actions[event.key]()
            self.recreate()
        super().additional_event_check(event)


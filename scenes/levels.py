from copy import copy
import pygame as pg
import scenes
from misc.constants import Font
from objects import Text
from objects.buttons import ButtonController, LvlButton, Button


class LevelsScene(scenes.BaseScene):
    __buttons_on_scene = 4

    # todo Game is used in __init__
    def __init__(self, game):
        super().__init__(game)
        self.is_current = False
        self.__scroll = max(min(self.game.maps.cur_id, len(self.game.maps) - self.__buttons_on_scene), 0)

    # region Public

    # region Implementation of BaseScene

    def additional_event(self, event: pg.event.Event) -> None:
        actions = {
            pg.K_e: lambda: self.update_scroll(1),
            pg.K_q: lambda: self.update_scroll(-1),
        }
        if event.type == pg.MOUSEWHEEL:
            self.update_scroll(-event.y)
            self.objects.clear()
            self.configure()
        elif event.type == pg.KEYDOWN and event.key in actions.keys():
            actions[event.key]()
            self.objects.clear()
            self.configure()
        super().additional_event(event)

    # endregion

    def update_scroll(self, index: int) -> None:
        self.__scroll = min(self.__scroll + index, len(self.game.maps) - self.__buttons_on_scene)
        self.__scroll = max(self.__scroll, 0)

    def create_buttons(self) -> None:
        buttons = list(self._button_init())
        for button in buttons:
            if hasattr(button, "value") and self.game.maps.cur_id == button.value[0]:
                button.text = '-' + button.text + '-'
        self.objects.append(ButtonController(self.game, buttons))

    # endregion

    # region Private

    # region Implementation of BaseScene

    def _create_title(self) -> None:
        title = Text('SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        title2 = Text('Scroll - [q, e]', 15, font=Font.DEFAULT)
        title2.move_center(self.game.width // 2, 50)
        self.objects.append(title, title2)

    def _button_init(self):
        for i in range(self.__scroll, self.__scroll + self.__buttons_on_scene):
            yield LvlButton(
                game=self.game,
                rect=pg.Rect(0, 0, 100, 40),
                value=(i, self.game.maps.images[i]),
                text=f'LEVEL {i + 1}',
                center=(self.game.width // 2 - 55, (85 + 40 * (i - self.__scroll))),
                text_size=Font.BUTTON_TEXT_SIZE - 4,
                active=i in range(len(self.game.unlocked_levels)))
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=self._scene_manager.pop,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

    def _create_objects(self) -> None:
        self.preview = copy(self.game.maps.images[self.game.maps.cur_id])
        self.objects.append(self.preview)
        self.create_buttons()

    # endregion

    # endregion

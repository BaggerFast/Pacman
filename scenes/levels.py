import pygame as pg

from misc import Font, Maps
from objects import ButtonController, Text
from objects.button.button import LvlButton, SceneButton
from scenes import base


class Scene(base.Scene):
    __scroll = 0
    __counter = 0
    __current_level = 0

    def create_static_objects(self):
        self.__create_title()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_object.append(title)

    def create_buttons(self) -> None:
        buttons = []
        for i in range(Maps.count):
            buttons.append(
                LvlButton(
                   game=self.game,
                   geometry=pg.Rect(0, 0, 180, 40),
                   value=i,
                   text='LEVEL' + str(i+1),
                   center=(self.game.width // 2, 90+50*i),
                   text_size=Font.BUTTON_TEXT_SIZE,
                   active=i in self.game.unlocked_levels)
            )
        buttons.append(SceneButton(self.game, pg.Rect(0, 0, 180, 40),
                   text='MENU',
                   scene=(self.game.scenes.MENU, False),
                   center=(self.game.width // 2, 250),
                   text_size=Font.BUTTON_TEXT_SIZE))

        for index in range(len(buttons)):
            if str(self.game.level_id + 1) == buttons[index].text[-1:]:
                buttons[index] = LvlButton(self.game, pg.Rect(0, 0, 180, 40),
                                        value=buttons[index].value,
                                        text='» ' + buttons[index].text + ' «',
                                        center=(buttons[index].rect.centerx, buttons[index].rect.centery),
                                        text_size=Font.BUTTON_TEXT_SIZE)
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def button_y_cord(self, y):
        if 80 < self.__scroll + y < 290:
            return self.__scroll+y
        return 1000

    def on_activate(self) -> None:
        self.create_objects()
        self.__button_controller.reset_state()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.scenes.set(self.game.scenes.MENU)
                self.game.set_scene(self.game.scenes.MENU)
            elif event.type == pg.KEYDOWN and event.key == pg.K_w and self.__counter > 0:
                self.__counter -= 1
                print(self.__counter)
                self.__scroll += 50
                self.objects = []
                self.game.set_scene(self.game.scenes.LEVELS)
                self.create_buttons()
            elif event.type == pg.KEYDOWN and event.key == pg.K_s and self.__counter < 5:
                self.__counter += 1
                print(self.__counter)
                self.__scroll -= 50
                self.objects = []
                self.game.set_scene(self.game.scenes.LEVELS)
                self.create_buttons()



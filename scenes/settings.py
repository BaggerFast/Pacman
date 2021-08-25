import pygame as pg
from misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from objects import Text
from objects.button import Button
from scenes import base


class Scene(base.Scene):
    class DifficultyButton(Button):

        __difficulties = [
            "easy",
            "medium",
            "hard"
        ]

        def __init__(self, **args):
            super().__init__(**args)
            self.update_text()

        def click(self) -> None:
            self.game.settings.DIFFICULTY = (self.game.settings.DIFFICULTY + 1) % 3
            self.update_text()
            self.select()

        def update_text(self) -> None:
            self.text = self.__difficulties[self.game.settings.DIFFICULTY]

    class SelectButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self) -> None:
            self.select()
            self.game.settings.change_volume(self.value)
            self.game.scenes.current.volume_value.text = f"{self.game.settings.VOLUME} %"

    class SettingButton(Button):
        def __init__(self, **args):
            self.name, self.var = args.pop("name"), args.pop("var")
            super().__init__(**args)

        def update(self, var: str) -> None:
            if var in ["SOUND", "FUN"]:
                self.game.sounds.reload_sounds()

        def click(self) -> None:
            self.select()
            if not hasattr(self.game.settings, self.var):
                return
            active_mode = not getattr(self.game.settings, self.var)
            setattr(self.game.settings, self.var, active_mode)
            self.update(self.var)
            self.text = f"{self.name} {'ON' if active_mode else 'OFF'}"
            self.colors = BUTTON_GREEN_COLORS if active_mode else BUTTON_RED_COLORS

    __volume_position = 150
    __difficulty_pos = 210

    def create_static_objects(self) -> None:

        volume_text = Text(self.game, "VOLUME", 20)
        volume_text.move_center(self.game.width // 2, self.__volume_position)

        self.volume_value = Text(self.game, f"{self.game.settings.VOLUME} %", 20)
        self.volume_value.move_center(self.game.width // 2, self.__volume_position + 30, )

        self.static_objects += [volume_text, self.volume_value, self.create_title()]

    def create_title(self) -> Text:
        text = Text(self.game, "SETTINGS", 30, font=Font.TITLE)
        text.move_center(self.game.width // 2, 30)
        return text

    def button_init(self) -> None:
        yield self.SettingButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 35),
            text=f"SOUND {'ON' if self.game.settings.SOUND else 'OFF'}",
            center=(self.game.width // 2, 75),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_GREEN_COLORS if self.game.settings.SOUND else BUTTON_RED_COLORS,
            var="SOUND",
            name="SOUND")

        yield self.SettingButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 35),
            text=f"FUN {'ON' if self.game.settings.FUN else 'OFF'}",
            center=(self.game.width // 2, 75 + 40),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_GREEN_COLORS if self.game.settings.FUN else BUTTON_RED_COLORS,
            var="FUN",
            name="FUN",
            active=self.prev_scene == self.game.scenes.MENU
        )

        yield self.SelectButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 40, 35),
            text='-',
            center=(self.game.width // 2 - 60, self.__volume_position + 30),
            value=-5
        )
        yield self.SelectButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 40, 35),
            text='+',
            center=(self.game.width // 2 + 65, self.__volume_position + 30),
            value=5,
        )

        yield self.DifficultyButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 120, 35),
            center=(self.game.width // 2, self.__difficulty_pos),
            text_size=Font.BUTTON_TEXT_SIZE,
            active=self.prev_scene == self.game.scenes.MENU
        )

        yield self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='BACK',
            scene=self.prev_scene,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE
        )

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.prev_scene)

    def __call__(self, *args, **kwargs):
        self.game.scenes.set(self, reset=True)

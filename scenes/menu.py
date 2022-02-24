import pygame as pg
from PIL import ImageFilter, Image

from misc.constants.classes import MenuPreset
from objects import Text, ImageObject
from objects.buttons import Button
from objects.map import rand_color
from misc import Font, Color, VERSION
from scenes.base import BaseScene


class MenuScene(BaseScene):

    def start_logic(self):
        self.preview = self.game.maps.full_surface
        self.color = rand_color()
        self.game.map_color = self.color
        self.change_color()
        self.blur_preview()

    def create_objects(self) -> None:
        image = ImageObject(self.preview, (0, 0))

        ver = Text(VERSION, 8, font=Font.TITLE)
        ver.move(self.game.width - 50, 270)

        self.objects += [image, ver, self.__level_indicator]

        super().create_objects()

    def create_title(self) -> None:
        title = Text('PACMAN', 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)

        self.objects.append(title)

    @property
    def __level_indicator(self) -> Text:
        indicator = Text(self.game.maps.level_name, 15, font=Font.TITLE)
        indicator.move_center(self.game.width // 2, 60)
        return indicator

    def change_color(self) -> None:
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Color.MAIN_MAP:
                    self.preview.set_at((x, y), self.color)

    def blur_preview(self) -> None:
        blur_count = 5
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, 'RGBA')
        impil = Image.frombytes('RGBA', (rect.width, rect.height), surify)
        piler = impil.resize(self.game.size). \
            filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

    def button_init(self):
        names = [
            MenuPreset("PLAY", lambda: self.scene_manager.reset(self.scenes.MAIN(self.game))),
            MenuPreset("LEVELS", lambda: self.scene_manager.append(self.scenes.LEVELS(self.game))),
            MenuPreset("SKINS", lambda: self.scene_manager.append(self.scenes.SKINS(self.game))),
            MenuPreset("RECORDS", lambda: self.scene_manager.append(self.scenes.RECORDS(self.game))),
            MenuPreset("SETTINGS", lambda: self.scene_manager.append(self.scenes.SETTINGS(self.game))),
            MenuPreset("CREDITS", lambda: self.scene_manager.append(self.scenes.CREDITS(self.game))),
            MenuPreset("EXIT", self.game.exit_game),
        ]
        for i, menu_preset in enumerate(names):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 26),
                text=menu_preset.header,
                function=menu_preset.function,
                center=(self.game.width // 2, 95 + i * 28),
                text_size=Font.BUTTON_TEXT_SIZE
            )

    def additional_event_check(self, event: pg.event.Event) -> None:
        pass

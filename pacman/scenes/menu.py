import pygame as pg
from PIL import ImageFilter, Image
from pacman import scenes
from settings import VERSION
from pacman.misc.constants import Font
from pacman.misc.constants.classes import MenuPreset, Color
from pacman.objects import Text, ImageObject
from pacman.objects.buttons import Button
from pacman.objects.map import rand_color, Map
from pacman.serializers import LevelSerializer


class MenuScene(scenes.BaseScene):

    # todo Game is used in __init__
    def __init__(self, game):
        super().__init__(game)
        self.preview = self.game.maps.full_surface
        Map.color = rand_color()
        self.change_color()
        self.blur_preview()

    # region Public

    def change_color(self) -> None:
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Color.MAIN_MAP:
                    self.preview.set_at((x, y), Map.color)

    def blur_preview(self) -> None:
        blur_count = 5
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, 'RGBA')
        impil = Image.frombytes('RGBA', (rect.width, rect.height), surify)
        piler = impil.resize(self.game.resolution). \
            filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

    # endregion

    # region Private

    # region Implementation of BaseScene

    def _create_objects(self) -> None:
        image = ImageObject(self.preview, (0, 0))

        ver = Text(VERSION, 8, font=Font.TITLE)
        ver.move(self.game.width - 50, 270)
        self.objects.append(image, ver, self.__level_indicator)

        super()._create_objects()

    def _create_title(self) -> None:
        title = Text('PACMAN', 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)

        self.objects.append(title)

    def _button_init(self):
        names = (
            MenuPreset("PLAY", lambda: self._scene_manager.reset(scenes.MainScene(self.game))),
            MenuPreset("LEVELS", lambda: self._scene_manager.append(scenes.LevelsScene(self.game))),
            MenuPreset("SKINS", lambda: self._scene_manager.append(scenes.SkinsScene(self.game))),
            MenuPreset("RECORDS", lambda: self._scene_manager.append(scenes.RecordsScene(self.game))),
            MenuPreset("SETTINGS", lambda: self._scene_manager.append(scenes.SettingsScene(self.game))),
            MenuPreset("EXIT", self.game.exit_game),
        )
        for i, menu_preset in enumerate(names):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 26),
                text=menu_preset.header,
                function=menu_preset.function,
                center=(self.game.width // 2, 95 + i * 28),
                text_size=Font.BUTTON_TEXT_SIZE
            )

    # endregion

    @property
    def __level_indicator(self) -> Text:
        indicator = Text(f'{LevelSerializer()}', 15, font=Font.TITLE)
        indicator.move_center(self.game.width // 2, 60)
        return indicator

    def additional_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pass
    # endregion

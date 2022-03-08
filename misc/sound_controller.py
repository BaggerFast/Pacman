from typing import Union
import pygame as pg


class SoundController:

    def __init__(self, game, channel: int = 0, path: Union[str, pg.mixer.Sound] = '', volume: int = 1):
        # todo delete game
        self.game = game
        self.sound = pg.mixer.Sound(path)
        self.volume = volume
        self.channel = pg.mixer.Channel(channel)
        self.update()

    # region Public

    def update(self) -> None:
        self.volume = 0 if not self.game.settings.SOUND else self.game.settings.VOLUME / 100
        self.sound.set_volume(self.volume)

    def play(self) -> None:
        self.update()
        self.channel.play(self.sound)

    def stop(self) -> None:
        self.channel.stop()

    def pause(self) -> None:
        self.channel.pause()

    def unpause(self) -> None:
        self.channel.unpause()

    def is_busy(self) -> bool:
        return self.channel.get_busy()

    # endregion

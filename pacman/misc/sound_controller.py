import pygame as pg

from pacman.serializers import SettingsSerializer


class SoundController:

    def __init__(self, channel: int = 0, path: str = '', volume: int = 1):
        self.sound = pg.mixer.Sound(path)
        self.channel = pg.mixer.Channel(channel)
        self.volume = volume
        self.update()

    # region Public

    def update(self) -> None:
        self.volume = 0 if not SettingsSerializer().sound else SettingsSerializer().volume / 100
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

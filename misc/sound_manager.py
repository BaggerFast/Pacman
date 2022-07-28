import pygame as pg

from misc import PathManager


class Sound:

    # todo sound

    def __init__(self, sound: str, channel: int = 0, volume: int = 1):
        self.sound = pg.mixer.Sound(PathManager.get_sound(sound))
        self.channel = pg.mixer.Channel(channel)
        self.volume = volume
        self.update()

    def update(self):
        self.volume = 0 if not True else self.volume / 100
        self.sound.set_volume(self.volume)

    def play(self):
        self.update()
        self.channel.play(self.sound)

    def pause(self) -> None:
        self.channel.pause()

    def unpause(self) -> None:
        self.channel.unpause()

    def stop(self) -> None:
        self.channel.stop()

    def is_busy(self) -> bool:
        return self.channel.get_busy()

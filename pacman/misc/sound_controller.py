import pygame as pg

from pacman.data_core import PathManager
from pacman.misc.serializers import SettingsStorage


class SoundController:
    def __init__(self, sound_path: str, channel: int = 0, volume: int = 1):
        self.sound = pg.mixer.Sound(PathManager.get_sound_path(sound_path))
        self.channel = pg.mixer.Channel(channel)
        self.volume = volume
        self.update()

    def update(self):
        self.volume = 0 if not SettingsStorage().mute else SettingsStorage().volume / 100
        self.sound.set_volume(self.volume)

    def play(self):
        self.update()
        self.channel.play(self.sound)

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()

    def stop(self):
        self.channel.stop()

    def is_busy(self):
        return self.channel.get_busy()

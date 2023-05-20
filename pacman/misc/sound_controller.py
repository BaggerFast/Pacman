import pygame as pg

from pacman.storage import SettingsStorage

from .utils import load_sound


class Sound:
    def __init__(self, sound_path: str, channel: int = 0, volume: int = 1):
        self.sound = load_sound(sound_path)
        self.channel = pg.mixer.Channel(channel)
        self.volume = volume
        self.update()

    def set(self, sound_path: str):
        self.sound = load_sound(sound_path)

    def update(self):
        self.volume = 0 if not SettingsStorage().mute else SettingsStorage().volume / 100
        self.sound.set_volume(self.volume)

    def play(self, loop: int = 0):
        self.update()
        self.channel.play(self.sound, loops=loop)

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()

    def stop(self):
        self.channel.stop()

    def is_busy(self):
        return self.channel.get_busy()

import pygame as pg


def update(object):
    object.update_volume()


class SoundController:
    def __init__(self, game, sound, channel: int = 0, volume: int = 1):
        self.sound = sound
        self.game = game
        self.volume_on = volume
        self.channel = pg.mixer.Channel(channel)
        self.update_volume()

    def update_volume(self):
        self.volume = 0 if self.game.settings.MUTE else self.volume_on
        self.sound.set_volume(self.volume)

    def play(self):
        self.channel.play(self.sound)

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()

    def stop(self):
        self.channel.stop()

    def get_busy(self):
        return self.channel.get_busy()


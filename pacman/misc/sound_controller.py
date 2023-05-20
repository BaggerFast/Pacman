from pygame.mixer import Channel

from pacman.storage import SettingsStorage

from .utils import load_sound


class Sound:
    def __init__(self, sound_path: str, channel: int = 0, volume: int = 1):
        self.__sound = load_sound(sound_path)
        self.__channel = Channel(channel)
        self.__volume = volume
        self.__update()

    # region Public

    @property
    def length(self) -> float:
        return self.__sound.get_length()

    def set(self, sound_path: str):
        self.__sound = load_sound(sound_path)

    def play(self, loop: int = 0):
        self.__update()
        self.__channel.play(self.__sound, loops=loop)

    def stop(self):
        self.__channel.stop()

    def pause(self):
        self.__channel.pause()

    def unpause(self):
        self.__channel.unpause()

    def is_busy(self):
        return self.__channel.get_busy()

    # endregion

    # region Private

    def __update(self):
        self.__volume = 0 if not SettingsStorage().mute else SettingsStorage().volume / 100
        self.__sound.set_volume(self.__volume)

    # endregion

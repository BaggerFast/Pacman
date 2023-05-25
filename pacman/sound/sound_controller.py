from pygame.mixer import Sound

from pacman.data_core.enums import SoundCh
from pacman.storage import SettingsStorage


class SoundController:
    @staticmethod
    def play(channel: SoundCh, sound: Sound) -> None:
        channel.value.play(sound)

    @staticmethod
    def get_sound(channel: SoundCh) -> Sound:
        return channel.value.get_sound()

    @staticmethod
    def play_if_not_busy(channel: SoundCh, sound: Sound) -> None:
        if not channel.value.get_busy():
            channel.value.play(sound)

    @staticmethod
    def reset_play(channel: SoundCh, sound: Sound) -> None:
        if channel.value.get_sound() is sound:
            return
        channel.value.play(sound)

    @staticmethod
    def update_volume():
        for ch in SoundCh:
            ch.value.set_volume(0 if SettingsStorage().MUTE else SettingsStorage().volume / 100)

    @staticmethod
    def is_busy(channel: SoundCh) -> bool:
        return channel.value.get_busy()

    @staticmethod
    def stop(channel: SoundCh) -> None:
        channel.value.stop()

    @staticmethod
    def pause(channel: SoundCh) -> None:
        channel.value.pause()

    @staticmethod
    def unpause(channel: SoundCh) -> None:
        channel.value.unpause()

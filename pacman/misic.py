from random import choice

from pacman.data_core.constants import Sounds
from pacman.misc.serializers import SettingsStorage, SkinStorage
from pacman.misc.singleton import Singleton
from pacman.misc.sound_controller import SoundController
from pacman.misc.tmp_skin import SkinEnum


class Music(Singleton):
    def __init__(self):
        self.click = SoundController(sound_path=Sounds.CLICK)
        self.siren = SoundController(channel=3, sound_path=choice(Sounds.SIREN))
        self.fruit = SoundController(channel=4, sound_path=Sounds.FRUIT)
        self.ghost = SoundController(channel=4, sound_path=Sounds.GHOST)
        self.pellet = SoundController(channel=6, sound_path=Sounds.PELLET)
        self.menu = SoundController(channel=4, sound_path=Sounds.INTERMISSION)

        if SettingsStorage().fun:
            self.pacman = SoundController(sound_path=choice(Sounds.DEAD))
            self.seed = SoundController(channel=4, sound_path=Sounds.SEED_FUN)
            self.intro = SoundController(channel=1, sound_path=choice(Sounds.INTRO))
            self.gameover = SoundController(channel=2, sound_path=choice(Sounds.GAME_OVER))
        else:
            self.pacman = SoundController(sound_path=Sounds.DEAD[0])
            self.seed = SoundController(channel=4, sound_path=Sounds.SEED)
            self.intro = SoundController(
                channel=1,
                sound_path=(Sounds.INTRO[0] if not SkinStorage().equals(SkinEnum.POKEBALL) else Sounds.POC_INTRO),
            )
            self.gameover = SoundController(channel=2, sound_path=Sounds.GAME_OVER[0])

    def reload_sounds(self):
        self.siren = SoundController(channel=3, sound_path=choice(Sounds.SIREN))
        if SettingsStorage().fun:
            self.pacman = SoundController(sound_path=choice(Sounds.DEAD))
            self.seed = SoundController(channel=4, sound_path=Sounds.SEED_FUN)
            self.intro = SoundController(channel=1, sound_path=choice(Sounds.INTRO))
            self.gameover = SoundController(channel=2, sound_path=choice(Sounds.GAME_OVER))
        else:
            self.pacman = SoundController(sound_path=Sounds.DEAD[0])
            self.seed = SoundController(channel=4, sound_path=Sounds.SEED)
            self.intro = SoundController(
                channel=1,
                sound_path=(Sounds.INTRO[0] if not SkinStorage().equals(SkinEnum.POKEBALL) else Sounds.POC_INTRO),
            )
            self.gameover = SoundController(channel=2, sound_path=Sounds.GAME_OVER[0])

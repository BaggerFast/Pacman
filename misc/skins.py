from typing import Union

from misc import Animator, get_list_path


class Skins:
    class __Skin:

        def __init__(self, skin_name):
            self.name = skin_name
            self.walk = Animator(get_list_path('png', 'images', 'pacman', self.name, 'walk'))
            self.dead = Animator(get_list_path('png', 'images', 'pacman', self.name, 'dead'), 100, False, True)

    def __init__(self):
        """
        param must be named like folder with skin
        """
        self.default = None
        self.chrome = None
        self.half_life = None
        self.load_skins()

        self.__current = self.default

    def load_skins(self):
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                self.__dict__[key] = self.__Skin(key)

    @property
    def all_skins(self):
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    @property
    def names(self):
        return self.__dict__.keys()

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value: Union[str, __Skin]):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, self.__Skin):
            self.__current = value

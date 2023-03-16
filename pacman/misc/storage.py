# import json
# import os
# from json import JSONDecodeError
#
# from pacman.data_core import Dirs
# from pacman.misc import FRUITS_COUNT, HIGHSCORES_COUNT
#
#
# class Field:
#     def dict(self):
#         data = {}
#         for key in self.__dict__.keys():
#             if hasattr(self.__dict__[key], "dict"):
#                 data[key] = self.__dict__[key].dict()
#             else:
#                 if hasattr(self.__dict__[key], "__dict__"):
#                     data[key] = self.__dict__[key].__dict__
#                 else:
#                     data[key] = self.__dict__[key]
#         return data
#
#     def read_dict(self, value):
#         for key in self.__dict__.keys():
#             if key in value.keys():
#                 if hasattr(self.__dict__[key], "dict"):
#                     self.__dict__[key].read_dict(value[key])
#                 else:
#                     self.__dict__[key] = value[key]
#
#
# class Storage(Field):
#     class __Settings(Field):
#         def __init__(self):
#             self.MUTE = False
#             self.FUN = False
#             self.VOLUME = 100
#             self.DIFFICULTY = 0
#
#     __storage_filepath = os.path.join(Dirs.ROOT, "storage.json")
#
#     def __init__(self, game) -> None:
#
#         self.unlocked_skins = ["default"]
#         self.last_skin = "default"
#         self.last_level_id = 0
#         self.unlocked_levels = [0]
#
#         self.settings = self.__Settings()
#         self.eaten_fruits = [0 for _ in range(FRUITS_COUNT)]
#         self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(game.maps.count)]
#         self.load()
#
#     def save(self) -> None:
#         string = json.dumps(self.dict(), indent=2)
#         with open(self.__storage_filepath, "w") as file:
#             file.write(string)
#
#     def load(self) -> None:
#         try:
#             with open(self.__storage_filepath, "r") as f:
#                 json_dict = json.load(f)
#                 self.read_dict(json_dict)
#         except FileNotFoundError or JSONDecodeError:
#             with open(self.__storage_filepath, "w") as f:
#                 json.dump(self.dict(), f, indent=2)
#         finally:
#             self.save()

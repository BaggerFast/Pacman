from misc.patterns import Singleton
from misc.storage.base import SerDes


class FruitStorage(SerDes, Singleton):

    def __init__(self):
        self.__fruits = []

    def __getitem__(self, item: int) -> int:
        try:
            return self.__fruits[item]
        except IndexError:
            return 0

    def __setitem__(self, key: int, value: int) -> None:
        if key in range(8):
            if isinstance(value, int):
                try:
                    self.__fruits[key] = value
                except IndexError:
                    self.__fruits.append(value)
            else:
                raise Exception(f"Fruit value must be int type, instead of {type(value)}")
        else:
            raise Exception(f"Id error. FruitController id: {key} doesn't exist")

    def __len__(self):
        return len(self.__fruits)

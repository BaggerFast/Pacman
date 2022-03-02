from copy import deepcopy

from misc.interfaces import IGenericObject, ILogical, IEventful, IDrawable


class Objects:
    __allowed_types = (ILogical, IEventful, IDrawable)

    def __init__(self, *args):
        if args is None:
            data = []
        self.__obj = self.__parse_list(args)

    def __parse_list(self, data: tuple) -> list:
        for i in data:
            self.__check_types(i)
        return list(data)

    def __check_types(self, obj):
        for tp in self.__allowed_types:
            if isinstance(obj, tp):
                return True
        raise TypeError("class Object поддерживает только определенные интерфейсы")

    def append(self, *args) -> None:
        for obj in self.__parse_list(args):
            if self.__check_types(obj):
                self.__obj.append(obj)

    def extend(self, obj: "Objects") -> None:
        if isinstance(obj, Objects):
            self.__obj.extend(obj.__obj)
        else:
            raise TypeError("class Object может быть расширен только Objects")

    def __getitem__(self, index: int):
        return self.__obj[index]

    def __len__(self):
        return len(self.__obj)

    def clear(self):
        self.__obj.clear()

from enum import IntEnum


class Rotation(IntEnum):
    right = (0, 1, 0)
    down = (1, 0, 1)
    left = (2, -1, 0)
    up = (3, 0, -1)

    def __new__(cls, index, x_offset, y_offset):
        obj = int.__new__(cls, index)
        obj._value_ = index
        obj.x_offset = x_offset
        obj.y_offset = y_offset
        return obj

    def __add__(self, other):
        index = self.__index__() + other.__index__()
        length = len(self.__class__)
        index += length * (round(abs(index) / length) + 1)
        index %= length
        return self.__class__(index)

    def __sub__(self, other):
        index = self.__index__() - other.__index__()
        length = len(self.__class__)
        index += length * (round(abs(index) / length) + 1)
        index %= length
        return self.__class__(index)

    __iadd__ = __add__
    __isub__ = __sub__

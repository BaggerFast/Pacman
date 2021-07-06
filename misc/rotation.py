from enum import IntEnum


class Rotation(IntEnum):
    up = (0, 0, -1)
    left = (1, -1, 0)
    down = (2, 0, 1)
    right = (3, 1, 0)

    def __new__(cls, index, x_offset, y_offset):
        obj = int.__new__(cls, index)
        obj._value_ = index
        obj.x_offset = x_offset
        obj.y_offset = y_offset
        return obj


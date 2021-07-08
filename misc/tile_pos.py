from .rotation import Rotation


class TilePos:
    def __init__(self, x: int, y: int): self.x, self.y = int(x), int(y)
    def __repr__(self): return str((self.x, self.y))
    def __eq__(self, other): return self[0] == other[0] and self[1] == other[1]

    def __add__(self, other):
        if isinstance(other, (type(self), tuple, list)):
            return type(self)(self[0] + other[0], self[1] + other[1])
        raise TypeError

    __iadd__, __radd__ = __add__, __add__

    def __sub__(self, other):
        if isinstance(other, (type(self), tuple, list)):
            return type(self)(self[0] - other[0], self[1] - other[1])

    __isub__, __rsub__ = __sub__, __sub__

    def length_to(self, other) -> float: return sum(i ** 2 for i in (self - other)) ** (1 / 2)

    def __getitem__(self, item):
        if isinstance(item, str):
            return {"x": self.x, "y": self.y}[item.lower()]
        else:
            return (self.x, self.y)[item]

    def __setitem__(self, key, value):
        value = int(value)
        if isinstance(key, str):
            if key.lower() == "x":
                self.x = value
            elif key.lower() == "y":
                self.y = value
            else:
                raise AttributeError("Не известная координата")
        else:
            key = abs(key.__index__()) % 2
            if key == 0:
                self.x = value
            else:
                self.y = value

    def offset(self, rotation: Rotation, n: int = 1): return self + (rotation.x_offset * n, rotation.y_offset * n)
    def up(self, n: int = 1): return self.offset(Rotation.up, n)
    def left(self, n: int = 1): return self.offset(Rotation.left, n)
    def down(self, n: int = 1): return self.offset(Rotation.down, n)
    def right(self, n: int = 1): return self.offset(Rotation.right, n)

    def iterator_to(self, other):
        for y in range(min(self[1], other[1]), max(self[1], other[1]) + 1):
            for x in range(min(self[0], other[0]), max(self[0], other[0]) + 1):
                yield type(self)(x, y)

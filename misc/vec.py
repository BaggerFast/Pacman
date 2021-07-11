from .rotation import Rotation
from typing import Iterable, Union


class Vec:
    def __init__(self, x: float, y: float): self.x, self.y = x, y
    def __repr__(self): return str((self.x, self.y))
    def __eq__(self, other): return self[0] == other[0] and self[1] == other[1]

    @property
    def length(self): return sum(self ** 2) ** (1 / 2)
    def length_to(self, other): return (self - other).length
    def __neg__(self): return self*-1
    def __pos__(self): return self.copy()
    def copy(self): return Vec(*self)
    def __abs__(self): return Vec(*(abs(i) for i in self))

    def __mul__(self, other):
        other = (other, other) if isinstance(other, (int, float)) else other
        return Vec(self[0] * other[0], self[1] * other[1])

    def __imul__(self, other): return self.__mul__(other)
    def __rmul__(self, other): return self.__mul__(other)

    def mul_on_matrix(self, other: Iterable[Iterable]): return Vec(*(sum(self * i) for i in other))
    def __matmul__(self, other: Iterable[Iterable]): return self.mul_on_matrix(other)
    def __imatmul__(self, other: Iterable[Iterable]): return self @ other

    def __truediv__(self, other):
        other = (other, other) if isinstance(other, (int, float)) else other
        return Vec(self[0] / other[0], self[1] / other[1])
    
    def __itruediv__(self, other): return self.__truediv__(other)
    def __rtruediv__(self, other): return Vec.__truediv__(other, self)
    
    def __floordiv__(self, other):
        other = (other, other) if isinstance(other, (int, float)) else other
        return Vec(self[0] // other[0], self[1] // other[1])

    def __ifloordiv__(self, other): return self.__floordiv__(other)
    def __rfloordiv__(self, other): return Vec.__floordiv__(other, self)

    def __mod__(self, other):
        other = (other, other) if isinstance(other, (int, float)) else other
        return Vec(self[0] % other[0], self[1] % other[1])

    def __imod__(self, other): return self.__mod__(other)
    def __rmod__(self, other): return Vec.__mod__(other, self)
    
    def __divmod__(self, other): return self // other, self % other
    
    def __add__(self, other): return Vec(self[0] + other[0], self[1] + other[1])
    def __iadd__(self, other): return self + other
    def __radd__(self, other): return self + other

    def __sub__(self, other): return Vec(self[0] - other[0], self[1] - other[1])
    def __isub__(self, other): return Vec.__sub__(self, other)
    def __rsub__(self, other): return Vec.__sub__(other, self)

    def __pow__(self, power):
        power = (power, power) if isinstance(power, (int, float)) else power
        return Vec(self[0] ** power[0], self[1] ** power[1])
    
    def __ipow__(self, power): self.__pow__(power)

    def __getitem__(self, item):
        if isinstance(item, str):
            return {"x": self.x, "y": self.y}[item.lower()]
        else:
            return (self.x, self.y)[item]

    def __setitem__(self, key, value):
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

    def offset(self, rotation: Union[Rotation, int], n: float = 1):
        rotation = Rotation(rotation)
        return self + (rotation.x_offset * n, rotation.y_offset * n)

    def up(self, n: float = 1): return self.offset(Rotation.up, n)
    def left(self, n: float = 1): return self.offset(Rotation.left, n)
    def down(self, n: float = 1): return self.offset(Rotation.down, n)
    def right(self, n: float = 1): return self.offset(Rotation.right, n)

    def iterator_to(self, other):
        for y in range(min(self[1], other[1]), max(self[1], other[1])):
            for x in range(min(self[0], other[0]), max(self[0], other[0])):
                yield type(self)(x, y)

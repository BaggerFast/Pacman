
class Rotation:
    up: object
    left: object
    down: object
    right: object

    __by_name_dict: dict = {}
    __tuple: tuple = ()

    def __init__(self, index: int, name: str, offset): self.id, self.name, self.offset = index, name, offset
    def __index__(self) -> int: return self.id
    def __repr__(self) -> str: return self.name
    def get_offset(self) -> tuple: return self.offset
    def get_offset_x(self) -> int: return self.offset[0]
    def get_offset_y(self) -> int: return self.offset[1]

    def __add__(self, other): return self[self.id + other.__index__()]
    __iadd__, __radd__ = __add__, __add__

    def __sub__(self, other): return self[self.id - other.__index__()]
    __isub__, __rsub__ = __sub__, __sub__

    @classmethod
    def __iter__(cls): return iter(cls.__tuple)

    @classmethod
    def by_name(cls, name: str):
        rot: Rotation = cls.__by_name_dict.get(name, None)
        if rot is None:
            raise ArithmeticError("Не в этом мире")
        return rot

    @classmethod
    def by_id(cls, index): return cls.__tuple[index]

    @classmethod
    def __getitem__(cls, item):
        if isinstance(item, str):
            return cls.by_name(item)
        else:
            return cls.by_id(item)

    @classmethod
    def __compile(cls):
        """
        Заполняет поля класса (up, down, __by_name_dict)
        """
        cls.up = cls(0, "up", (0, -1))
        cls.left = cls(1, "left", (-1, 0))
        cls.down = cls(2, "down", (0, 1))
        cls.right = cls(3, "right", (1, 0))

        cls.__tuple = (cls.up, cls.left, cls.down, cls.right)
        for rot in cls.__tuple:
            cls.__by_name_dict[rot.name] = rot

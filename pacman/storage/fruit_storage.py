from .utils import SerDes


class FruitStorage(SerDes):
    def __init__(self):
        self.__fruit_count = 7
        self.__eaten_fruits = [0 for _ in range(self.__fruit_count)]

    @property
    def eaten_fruits(self) -> list[int]:
        return self.__eaten_fruits

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        if fruit_id in range(self.__fruit_count):
            self.__eaten_fruits[fruit_id] += value
        else:
            raise ValueError(f"id error. Fruit id: {fruit_id} doesn't exist")

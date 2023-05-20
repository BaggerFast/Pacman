from .utils import SerDes


class FruitStorage(SerDes):
    def __init__(self):
        self.__fruit_count = 7
        self.eaten_fruits = [0 for _ in range(self.__fruit_count)]

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        if fruit_id in range(7):
            self.eaten_fruits[fruit_id] += value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")

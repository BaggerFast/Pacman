class HpSystem:
    def __init__(self, lives: int = 1, max_lives: int = 5):
        self.__lives = lives
        self.__max_lives = max_lives

    # region Public

    @property
    def lives(self):
        return self.__lives

    def add(self) -> None:
        self.__lives += 1
        self.__check_min_and_max()

    def remove(self) -> None:
        self.__lives -= 1
        self.__check_min_and_max()

    # endregion

    # region Private

    def __check_min_and_max(self) -> None:
        self.__lives = max(0, self.__lives)
        self.__lives = min(self.__max_lives, self.__lives)

    def __int__(self) -> int:
        return self.__lives

    def __bool__(self) -> bool:
        return self.__lives > 0

    # endregion

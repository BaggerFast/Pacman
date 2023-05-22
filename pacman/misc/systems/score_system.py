class ScoreSystem:
    def __init__(self) -> None:
        self.__score = 0
        self.__fear_count = 0
        self.__eaten_fruits = 0

    # region Public

    @property
    def score(self):
        return self.__score

    def eat_seed(self) -> int:
        return self.__update_score(10)

    def eat_fruit(self) -> int:
        from pacman.storage import FruitStorage

        FruitStorage().store_fruit(self.__eaten_fruits, 1)
        self.__eaten_fruits += 1
        return self.__update_score(300 * self.__eaten_fruits, True)

    def eat_ghost(self) -> int:
        score_diff = self.__update_score(200 * 2**self.__fear_count, True)
        self.__fear_count += 1
        return score_diff

    def eat_energizer(self) -> int:
        self.__fear_count = 0
        return self.__update_score(50, True)

    # endregion

    # region Private

    def __update_score(self, value: int, diff_boost: bool = False) -> int:
        tmp_score = self.__score
        if diff_boost:
            from pacman.storage import SettingsStorage

            value *= SettingsStorage().DIFFICULTY + 1
        self.__score += value
        return self.score - tmp_score

    def __str__(self):
        return f"{self.__score}"

    def __int__(self):
        return self.__score

    # endregion

class Health:
    def __init__(self, lives=1, max_lives=5):
        self.__lives = lives
        self.max_lives = max_lives

    @property
    def lives(self):
        return self.__lives

    def __add__(self, value):
        self.__lives = self.__lives + value
        self.__check_min_and_max()
        return self

    def __iadd__(self, value):
        return self + value

    def __sub__(self, value):
        self.__lives = self.__lives - value
        self.__check_min_and_max()
        return self

    def __isub__(self, value):
        return self - value

    def __check_min_and_max(self):
        self.__lives = max(0, self.__lives)
        self.__lives = min(self.max_lives, self.__lives)

    def change_count_lives(self, number):
        self.__lives += number


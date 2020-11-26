class Health:
    def __init__(self, lives=1, max_lives=5):
        self.__lives = lives
        self.max_lives = max_lives

    @property
    def lives(self):
        return self.__lives

    def change_count_lives(self, number):
        self.__lives += number
        self.__lives = max(0, self.__lives)
        self.__lives = min(self.max_lives, self.__lives)

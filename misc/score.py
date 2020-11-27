from misc.constants import Points


class Score:
    def __init__(self):
        self.__score = 0
        self.fear_mode = False
        self.fear_count = 0

    def __int__(self):
        return self.__score

    def __str__(self):
        return str(self.__score)

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, val):
        self.__score = val

    def __add_to_score(self, amount):
        self.__score += amount

    def eat_seed(self):
        self.__add_to_score(Points.POINT_PER_SEED)

    def eat_energizer(self):
        self.__add_to_score(Points.POINT_PER_ENERGIZER)

    def eat_fruit(self):
        self.__add_to_score(Points.POINT_PER_FRUIT)

    def activate_fear_mode(self):
        self.fear_mode = True

    def deactivate_fear_mode(self):
        self.fear_mode = False
        self.fear_count = 0

    def eat_ghost(self):
        self.fear_count += 1
        self.__add_to_score(100 * 2 ** self.fear_count)

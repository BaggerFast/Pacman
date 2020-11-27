from misc import Points


class Score:
    def __init__(self):
        self.__score = 0
        self.fear_mode = False
        self.fear_count = 0

    def __str__(self):
        return str(self.__score)

    def __int__(self):
        return self.__score

    @property
    def score(self):
        return self.__score

    def reset(self):
        self.__score = 0

    def __add__(self, value):
        self.__score = self.__score + value
        return self

    def __iadd__(self, value):
        return self + value

    def eat_seed(self):
        self + Points.POINT_PER_SEED

    def eat_energizer(self):
        self + Points.POINT_PER_ENERGIZER

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

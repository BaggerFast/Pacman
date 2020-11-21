class Health:
    def __init__(self, lives=1, max_lives=5):
        self.lives = lives
        self.max_lives = max_lives

    def __int__(self):
        return self.lives

    def change_count_lives(self, number):
        if self.max_lives >= self.lives + number >= 0:
            self.lives += number
        elif self.lives + number >= self.max_lives:
            self.lives = 5
        elif self.lives + number <= 0:
            self.lives = 0

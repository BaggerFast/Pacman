from py.constants import *


class Lives:
    def __init__(self, lives=1, max_lives=5):
        self.lives = lives
        self.max_lives = max_lives

    def change_count_lives(self, number):  # Функция для изменеия количества жизней
        if self.max_lives >= self.lives + number >= 0:
            self.lives += number
        elif self.lives + number >= self.max_lives:
            self.lives = 5
        elif self.lives + number <= 0:
            self.lives = 0

        print('lives: ', self.lives)


def main():
    gameover = False
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    lives = Lives()  # Создание объекта типа Lives с координатами\
    # 10,100 и размером текста 50
    while not gameover:
        screen.fill(Color.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    lives.change_count_lives(1)
                elif event.key == pygame.K_a:
                    lives.change_count_lives(-1)

        pygame.display.flip()


if __name__ == '__main__':
    main()

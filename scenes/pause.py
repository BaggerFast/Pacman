import pygame
from lib.BasicObjects.button import Button
from lib.BasicObjects.text import Text
from scenes.base import BaseScene
from constants import Color


class PauseScene(BaseScene):
    def create_objects(self) -> None:
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text('PAUSE', 50, (self.screen_width // 2, 100),
                              Color.WHITE)
        self.text_width = self.main_text.surface.get_rect().width
        self.main_text = Text('PAUSE', 50,
                              (self.screen_width // 2 - (self.text_width // 2),
                               40), Color.WHITE)

        # Создание и обработка кнопок
        self.continue_button = Button(
            self.screen, pygame.Rect(
                self.screen_width, 200, 50, 50
            ),
            self.continue_game(), 'CONTINUE', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64)
        )

    def update_objects(self):
        self.main_text.draw(self.screen)
        self.continue_button.draw()
        self.continue_button.update()

    @staticmethod
    def continue_game():
        print('Заглушка CONTINUE')

    @staticmethod
    def restart_game():
        print('Заглушка RESTART')

    @staticmethod
    def main_menu():
        print('Заглушка MAIN MENU')


# Тест работы меню паузы. Нужен только для разработчиков самого меню
def test_pause():
    pygame.init()
    screen = pygame.display.set_mode([1000, 600])
    pause = PauseScene(screen)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pause.continue_button.checkEvents(event)
        screen.fill(Color.BLACK)
        pause.update_objects()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    test_pause()

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
            self.screen, pygame.Rect(self.screen_width // 2, 200, 180, 60),
            continue_game, 'CONTINUE', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64)
        )
        self.continue_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                150, 180, 60),
            continue_game, 'CONTINUE', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64)
        )
        self.restart_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                250, 180, 60),
            restart_game, 'RESTART', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64)
        )
        self.menu_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                350, 180, 60),
            main_menu, 'MAIN MENU', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64)
        )

    def update_objects(self):
        self.main_text.draw(self.screen)
        self.continue_button.draw()
        self.continue_button.update()
        self.restart_button.draw()
        self.restart_button.update()
        self.menu_button.draw()
        self.menu_button.update()

    def event_update(self, event):
        self.continue_button.checkEvents(event)
        self.restart_button.checkEvents(event)
        self.menu_button.checkEvents(event)


def continue_game():
    print('Заглушка CONTINUE')


def restart_game():
    print('Заглушка RESTART')


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
            pause.event_update(event)
        screen.fill(Color.BLACK)
        pause.update_objects()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    test_pause()

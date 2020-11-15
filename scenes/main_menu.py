import pygame
from lib.BasicObjects.button import Button
from lib.BasicObjects.text import Text
from scenes.base import BaseScene
from py.constants import Color


class MainMenuScene(BaseScene):
    def createObjects(self) -> None:
        self.is_on = True
        self.check = None
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text('Pacman', 60, (self.screen_width // 2, 100),
                              Color.WHITE)
        self.text_width = self.main_text.surface.get_width()
        self.main_text = Text('Pacman', 60,
                              (self.screen_width // 2 - (self.text_width // 2),
                               10), Color.WHITE)

        # Создание и обработка кнопок
        self.continue_button = Button(
            self.screen, pygame.Rect(self.screen_width // 2, 200, 180, 60),
            self.play_game, 'PLAY', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )
        self.play_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                75, 180, 45),
            self.play_game, 'PLAY', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )
        self.records_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                138, 180, 45),
            self.records_game, 'RECORDS', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )
        self.exit_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                201, 180, 45),
            self.exit_game, 'EXIT', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )

    def updateObjects(self):
        self.main_text.draw(self.screen)
        self.play_button.draw()
        self.play_button.update()
        self.records_button.draw()
        self.records_button.update()
        self.exit_button.draw()
        self.exit_button.update()

    def eventUpdate(self, event):
        self.play_button.checkEvents(event)
        self.records_button.checkEvents(event)
        self.exit_button.checkEvents(event)

    def isOn(self):
        if self.is_on:
            return 1
        else:
            return 0

    def close(self):
        self.is_on = False

    def play_game(self):
        print('Заглушка PLAY')
        self.is_on = False

    def records_game(self):
        self.check = 'RECORDS'
        self.is_on = False

    def exit_game(self):
        self.is_on = False
        exit()


def launch_main_menu(screen):
    main_menu = MainMenuScene(screen)
    while main_menu.isOn():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu.close()
            main_menu.eventUpdate(event)
        screen.fill(Color.BLACK)
        main_menu.updateObjects()
        pygame.display.flip()
        pygame.time.wait(10)
    if main_menu.check == 'RECORDS':
        from scenes.records import launch_records_menu
        launch_records_menu(screen)


# Тест работы главного меню. Нужен только для разработчиков самого меню
def test_main_menu():
    pygame.init()
    screen = pygame.display.set_mode([224, 285], pygame.SCALED)
    launch_main_menu(screen)


if __name__ == '__main__':
    test_main_menu()

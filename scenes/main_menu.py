import pygame
from lib.BasicObjects.button import Button, ButtonControl
from lib.BasicObjects.text import Text
from scenes.base import BaseScene
from py.constants import Color


class MainMenuScene(BaseScene):
    def createObjects(self) -> None:
        self.is_on = True
        self.check = None
        self.current_button = -1
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
        self.buttons = []
        self.buttons.append(self.play_button)
        self.buttons.append(self.records_button)
        self.buttons.append(self.exit_button)

    def updateObjects(self):
        self.main_text.draw(self.screen)
        self.control.mouse_action()
        self.play_button.draw()
        self.records_button.draw()
        self.exit_button.draw()

    def eventUpdate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.control.unset_previous_button(self.current_button)
                self.current_button -= 1
                if self.current_button < 0:
                    self.current_button = 2
                self.control.set_current_button(self.current_button)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.control.unset_previous_button(self.current_button)
                self.current_button += 1
                if self.current_button > 2:
                    self.current_button = 0
                self.control.set_current_button(self.current_button)
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.buttons[self.current_button].onClick()

        self.buttons[0].checkEvents(event)
        self.buttons[1].checkEvents(event)
        self.buttons[2].checkEvents(event)

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
    control = ButtonControl(main_menu.buttons)
    main_menu.control = control
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

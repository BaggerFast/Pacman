import pygame
from lib.BasicObjects.button import Button, ButtonControl
from lib.BasicObjects.text import Text
from scenes.base import BaseScene
from py.constants import Color


class PauseScene(BaseScene):
    def createObjects(self) -> None:
        self.is_on = True
        self.check = None
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text('PAUSE', 60, (self.screen_width // 2, 100),
                              Color.WHITE)
        self.text_width = self.main_text.surface.get_width()

        self.main_text.update_position(self.main_text.surface.get_rect(
            center=(self.screen_width // 2, 35)))

        # Создание и обработка кнопок
        self.continue_button = Button(
            self.screen, pygame.Rect(self.screen_width // 2, 200, 180, 60),
            self.continue_game, 'CONTINUE', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )
        self.continue_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                75, 180, 45),
            self.continue_game, 'CONTINUE', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )
        self.restart_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                138, 180, 45),
            self.restart_game, 'RESTART', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )
        self.menu_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.continue_button.rect.w // 2,
                201, 180, 45),
            self.main_menu, 'MAIN MENU', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )

        # Работа со списками
        self.buttons = []
        self.buttons.append(self.continue_button)
        self.buttons.append(self.restart_button)
        self.buttons.append(self.menu_button)

    def updateObjects(self):
        self.main_text.draw(self.screen)
        self.control.mouse_action()
        self.continue_button.draw()
        self.continue_button.update()
        self.restart_button.draw()
        self.restart_button.update()
        self.menu_button.draw()
        self.menu_button.update()

    def eventUpdate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.continue_game()

    def isOn(self):
        if self.is_on:
            return 1
        else:
            return 0

    def close(self):
        self.is_on = False

    def continue_game(self):
        print('Заглушка CONTINUE')
        self.is_on = False

    def restart_game(self):
        print('Заглушка RESTART')
        self.is_on = False

    def main_menu(self):
        self.check = 'MAIN MENU'
        self.is_on = False


def launch_pause_menu(screen):
    pause = PauseScene(screen)
    control = ButtonControl(pause.buttons)
    pause.control = control
    while pause.isOn():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause.close()
            pause.eventUpdate(event)
        screen.fill(Color.BLACK)
        pause.updateObjects()
        pygame.display.flip()
        pygame.time.wait(10)
    if pause.check == 'MAIN MENU':
        from scenes.main_menu import launch_main_menu
        launch_main_menu(screen)


# Тест работы меню паузы. Нужен только для разработчиков самого меню
def test_pause():
    pygame.init()
    screen = pygame.display.set_mode([224, 285], pygame.SCALED)
    launch_pause_menu(screen)


if __name__ == '__main__':
    test_pause()

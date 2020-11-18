# import pygame
# from lib.BasicObjects.button import Button, ButtonControl
# from lib.BasicObjects.text import Text
# from misc.constants import Color
# from scenes.base import BaseScene
#
#
# class MainMenuScene(BaseScene):
#     def createObjects(self) -> None:
#         self.current_button = -1
#         # Создание и обработка кнопок
#         self.continue_button = Button(
#             self.screen, pygame.Rect(self.screen_width // 2, 200, 180, 60),
#             self.play_game, 'PLAY', Color.GRAY,
#             Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
#             Color.BLACK, Color.DARK_GRAY, 50
#         )
#         self.play_button = Button(
#             self.screen, pygame.Rect(
#                 self.screen_width // 2 - self.continue_button.rect.w // 2,
#                 75, 180, 45),
#             self.play_game, 'PLAY', Color.GRAY,
#             Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
#             Color.BLACK, Color.DARK_GRAY, 50
#         )
#         self.records_button = Button(
#             self.screen, pygame.Rect(
#                 self.screen_width // 2 - self.continue_button.rect.w // 2,
#                 138, 180, 45),
#             self.records_game, 'RECORDS', Color.GRAY,
#             Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
#             Color.BLACK, Color.DARK_GRAY, 50
#         )
#         self.exit_button = Button(
#             self.screen, pygame.Rect(
#                 self.screen_width // 2 - self.continue_button.rect.w // 2,
#                 201, 180, 45),
#             self.exit_game, 'EXIT', Color.GRAY,
#             Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
#             Color.BLACK, Color.DARK_GRAY, 50
#         )
#         self.buttons = []
#         self.buttons.append(self.play_button)
#         self.buttons.append(self.records_button)
#         self.buttons.append(self.exit_button)
#
#
#     def eventUpdate(self, event):
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_w or event.key == pygame.K_UP:
#                 self.control.unset_previous_button(self.current_button)
#                 self.current_button -= 1
#                 if self.current_button < 0:
#                     self.current_button = 2
#                 self.control.set_current_button(self.current_button)
#             if event.key == pygame.K_s or event.key == pygame.K_DOWN:
#                 self.control.unset_previous_button(self.current_button)
#                 self.current_button += 1
#                 if self.current_button > 2:
#                     self.current_button = 0
#                 self.control.set_current_button(self.current_button)
#             if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
#                 self.buttons[self.current_button].onClick()
#
#         self.buttons[0].checkEvents(event)
#         self.buttons[1].checkEvents(event)
#         self.buttons[2].checkEvents(event)
#
#
# def launch_main_menu(screen):
#     main_menu = MainMenuScene(screen)
#
#     while main_menu.isOn():
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 main_menu.close()
#             main_menu.eventUpdate(event)
#         screen.fill(Color.BLACK)
#         main_menu.updateObjects()
#         pygame.display.flip()
#         pygame.time.wait(10)
#     if main_menu.check == 'RECORDS':
#         from scenes.records import launch_records_menu
#         launch_records_menu(screen)
#
#
# # Тест работы главного меню. Нужен только для разработчиков самого меню
# def test_main_menu():
#     pygame.init()
#     screen = pygame.display.set_mode([224, 285], pygame.SCALED)
#     launch_main_menu(screen)
#
#
# if __name__ == '__main__':
#     test_main_menu()

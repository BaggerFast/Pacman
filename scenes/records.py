import pygame
from lib.BasicObjects.button import Button
from lib.BasicObjects.text import Text
from scenes.base import BaseScene
from py.constants import Color
from os.path import join
from lib.BasicObjects.highscores import HighScore


class RecordsScene(BaseScene):
    def createObjects(self) -> None:
        self.records = HighScore().record_table
        self.is_on = True
        self.check = None
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text('RECORDS', 30, color=Color.WHITE)
        self.main_text_width = self.main_text.surface.get_width()
        self.main_text.update_position(self.main_text.surface.get_rect(
            center=(self.screen_width // 2, 25)))

        self.error_text = Text('NO RECORDS', 60, color=Color.RED)
        self.error_text_width = self.error_text.surface.get_width()
        self.error_text.update_position(self.error_text.surface.get_rect(
            center=(self.screen_width // 2, 70)))

        # Создание и обработка рекордов
        self.one_text = Text(str(self.records[4]), 30,
                             (60, 45), Color.GOLD)
        self.one_text_width = self.one_text.surface.get_width()

        self.two_text = Text(str(self.records[3]), 30,
                             (60, 80), Color.SILVER)
        self.two_text_width = self.two_text.surface.get_width()

        self.three_text = Text(str(self.records[2]), 30,
                               (60, 115), Color.BRONZE)
        self.three_text_width = self.three_text.surface.get_width()

        self.four_text = Text('4: ' + str(self.records[1]), 30,
                              (25, 150), Color.WHITE)

        self.five_text = Text('5: ' + str(self.records[0]), 30,
                              (25, 185), Color.WHITE)

        # Создание и обработка кнопок
        self.back_button = Button(
            self.screen, pygame.Rect(self.screen_width // 2, 200, 120, 60),
            self.back, 'BACK', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )

        self.back_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.back_button.rect.w // 2,
                230, 120, 45),
            self.back, 'BACK', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY, 50
        )

        # Создание и обработка изображений
        self.gold_medal_path = join('images', 'golden_medal.png')
        self.silver_medal_path = join('images', 'silver_medal.png')
        self.bronze_medal_path = join('images', 'bronze_medal.png')
        self.stone_medal_path = join('images', 'stone_medal.png')
        self.wooden_medal_path = join('images', 'wooden_medal.png')

        self.gold_medal = pygame.image.load(self.gold_medal_path)
        self.silver_medal = pygame.image.load(self.silver_medal_path)
        self.bronze_medal = pygame.image.load(self.bronze_medal_path)
        self.stone_medal = pygame.image.load(self.stone_medal_path)
        self.wooden_medal = pygame.image.load(self.wooden_medal_path)

        self.gold_medal = pygame.transform.scale(self.gold_medal, (35, 35))
        self.silver_medal = pygame.transform.scale(self.silver_medal, (35, 35))
        self.bronze_medal = pygame.transform.scale(self.bronze_medal, (35, 35))
        self.stone_medal = pygame.transform.scale(self.stone_medal, (35, 35))
        self.wooden_medal = pygame.transform.scale(self.wooden_medal, (35, 35))

    def updateObjects(self):
        self.main_text.draw(self.screen)
        if self.records[4] != 0:
            self.one_text.draw(self.screen)
            self.screen.blit(
                self.gold_medal,
                (16, 45)
            )
        else:
            self.error_text.draw(self.screen)

        if self.records[3] != 0:
            self.two_text.draw(self.screen)
            self.screen.blit(
                self.silver_medal,
                (16, 80)
            )

        if self.records[2] != 0:
            self.three_text.draw(self.screen)
            self.screen.blit(
                self.bronze_medal,
                (16, 115)
            )

        if self.records[1] != 0:
            self.four_text.draw(self.screen)
            self.screen.blit(
                self.stone_medal,
                (16, 150)
            )

        if self.records[0] != 0:
            self.five_text.draw(self.screen)
            self.screen.blit(
                self.wooden_medal,
                (16, 185)
            )

        self.back_button.draw()
        self.back_button.update()

    def eventUpdate(self, event):
        self.back_button.checkEvents(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()

    def isOn(self):
        if self.is_on:
            return 1
        else:
            return 0

    def close(self):
        self.is_on = False

    def back(self):
        self.check = 'BACK'
        self.is_on = False


def launch_records_menu(screen):
    records_menu = RecordsScene(screen)
    while records_menu.isOn():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                records_menu.close()
            records_menu.eventUpdate(event)
        screen.fill(Color.BLACK)
        records_menu.updateObjects()
        pygame.display.flip()
        pygame.time.wait(10)
    if records_menu.check == 'BACK':
        from scenes.main_menu import launch_main_menu
        launch_main_menu(screen)


# Тест работы меню рекордов. Нужен только для разработчиков самого меню
def test_records():
    pygame.init()
    screen = pygame.display.set_mode([224, 285], pygame.SCALED)
    launch_records_menu(screen)


if __name__ == '__main__':
    test_records()

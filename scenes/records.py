import pygame
from lib.BasicObjects.button import Button
from lib.BasicObjects.text import Text
from scenes.base import BaseScene
from py.constants import Color


RECORDS = [1, 5, 228, 556, 6666]


class RecordsScene(BaseScene):
    def __init__(self, screen, records):
        self.records = records
        super().__init__(screen)

    def createObjects(self) -> None:
        self.is_on = True
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text('RECORDS', 30, (self.screen_width // 2, 100),
                              Color.WHITE)
        self.main_text_width = self.main_text.surface.get_width()
        self.main_text = Text('RECORDS', 30,
                              (self.screen_width // 2 - (self.main_text_width
                                                         // 2), 7),
                              Color.WHITE)

        # Создание и обработка рекордов
        self.one_text = Text('1: ' + str(self.records[4]), 30,
                             (self.screen_width // 2, 100), Color.WHITE)
        self.one_text_width = self.one_text.surface.get_width()
        self.one_text = Text('1: ' + str(self.records[4]), 30,
                             (25, 45),
                             (255, 215, 0))

        self.two_text = Text('2: ' + str(self.records[3]), 30,
                             (self.screen_width // 2, 100), Color.WHITE)
        self.two_text_width = self.two_text.surface.get_width()
        self.two_text = Text('2: ' + str(self.records[3]), 30,
                             (25, 80),
                             (192, 192, 192))

        self.three_text = Text('3: ' + str(self.records[2]), 30,
                               (self.screen_width // 2, 100), Color.WHITE)
        self.three_text_width = self.three_text.surface.get_width()
        self.three_text = Text('3: ' + str(self.records[2]), 30,
                               (25, 115),
                               (205, 127, 50))

        self.four_text = Text('4: ' + str(self.records[1]), 30,
                              (self.screen_width // 2, 100), Color.WHITE)
        self.four_text_width = self.four_text.surface.get_width()
        self.four_text = Text('4: ' + str(self.records[1]), 30,
                              (25, 150),
                              Color.WHITE)

        self.five_text = Text('5: ' + str(self.records[0]), 30,
                              (self.screen_width // 2, 100), Color.WHITE)
        self.five_text_width = self.five_text.surface.get_width()
        self.five_text = Text('5: ' + str(self.records[0]), 30,
                              (25, 185),
                              Color.WHITE)

        # Создание и обработка кнопок
        self.back_button = Button(
            self.screen, pygame.Rect(self.screen_width // 2, 200, 120, 60),
            self.back, 'BACK', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64)
        )
        self.back_button = Button(
            self.screen, pygame.Rect(
                self.screen_width // 2 - self.back_button.rect.w // 2,
                230, 120, 45),
            self.back, 'BACK', (128, 128, 128),
            (64, 64, 64), (255, 255, 255), (64, 64, 64),
            (0, 0, 0), (64, 64, 64), 30
        )

        # Создание и обработка изображений
        self.gold_medal = pygame.image.load('../images/golden_medal.png')
        self.silver_medal = pygame.image.load('../images/silver_medal.png')
        self.bronze_medal = pygame.image.load('../images/bronze_medal.png')
        self.gold_medal = pygame.transform.scale(self.gold_medal, (35, 35))
        self.silver_medal = pygame.transform.scale(self.silver_medal, (35, 35))
        self.bronze_medal = pygame.transform.scale(self.bronze_medal, (35, 35))

    def updateObjects(self):
        self.main_text.draw(self.screen)
        self.one_text.draw(self.screen)
        self.two_text.draw(self.screen)
        self.three_text.draw(self.screen)
        self.four_text.draw(self.screen)
        self.five_text.draw(self.screen)
        self.back_button.draw()
        self.back_button.update()
        self.screen.blit(
            self.gold_medal,
            (25 + self.one_text_width, 45)
        )
        self.screen.blit(
            self.silver_medal,
            (25 + self.two_text_width, 80)
        )
        self.screen.blit(
            self.bronze_medal,
            (25 + self.three_text_width, 115)
        )

    def eventUpdate(self, event):
        self.back_button.checkEvents(event)

    def isOn(self):
        if self.is_on:
            return 1
        else:
            return 0

    def close(self):
        self.is_on = False

    def back(self):
        print('Заглушка BACK')
        self.is_on = False


def launch_records_menu(screen):
    records_menu = RecordsScene(screen, RECORDS)
    while records_menu.isOn():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                records_menu.close()
            records_menu.eventUpdate(event)
        screen.fill(Color.BLACK)
        records_menu.updateObjects()
        pygame.display.flip()
        pygame.time.wait(10)


# Тест работы меню рекордов. Нужен только для разработчиков самого меню
def test_records():
    pygame.init()
    screen = pygame.display.set_mode([224, 285], pygame.SCALED)
    launch_records_menu(screen)


if __name__ == '__main__':
    test_records()

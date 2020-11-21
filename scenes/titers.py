import sys

import pygame as pg
from random import choice, randint

from objects.button import ButtonController, Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color


class TitersScene(BaseScene):
    students = [
        "Архипов Евгений",
        "Смирнов Андрей",
        "Грачев Егор",
        "Александров Даниил",
        "Егоров Александр",
        "Сергеев Сергей",
        "Бурдонов Арсений",
        "Игнатов Иван",
        "Лещенко Вячеcлав",
        "Полиехов Андрей",
        "Акомов Денис",
        "Богомолов Алексей",
        "Вартанян Владимир",
        "Дмитрий Пашков",
        "Киселева Алиса",
        "Николайчев Павел",
        "Оркин Родион(Юрий)",
        "Плотский Богдан",
        "Татаринов Игорь",
        "Терпунов Артём",
        "Тимченко Савелий",
        "Щеников Иван"
    ]

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.on_screen = []

    def create_objects(self) -> None:
        self.create_titles()

    def create_titles(self) -> None:
        pass


    def process_logic(self) -> None:
        if len(self.objects) == 0:
            self.create_objects()
        if pg.time.get_ticks() % 100 == 0:
            student = Text(self.game, self.students[randint(0,len(self.students)-1)], 10, color=Color.WHITE)
            student.move_center(-90, randint(10, self.game.height))
            self.objects.append(student)
        for student in self.objects:
            student.surface.set_alpha(abs((student.rect.x % self.game.width/2) - self.game.width))
            student.rect.x += 1
            self.game.screen.blit(student.surface, (student.rect.x, student.rect.y))
            if student.rect.x >= self.game.width:
                self.objects.remove(student)



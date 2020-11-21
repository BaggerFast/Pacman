import sys

import pygame

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

    def create_objects(self) -> None:
        self.create_titles()

    def create_titles(self) -> None:
        for index in range(len(self.students)):
            title = Text(self.game, self.students[index], 10, color=Color.WHITE)
            title.move_center(self.game.width // 2, self.game.height + 15 + index * 15)
            self.objects.append(title)

    def process_logic(self) -> None:
        for index in range(len(self.students)):
            self.objects[index].move_center(self.game.width // 2, self.objects[index].rect.y - 1)


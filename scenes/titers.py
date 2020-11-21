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
        self.on_screen = 0
        self.start_pos = -100
        self.speed = 0.3
        self.alpha_delta = -15

    def process_logic(self) -> None:
        if len(self.objects) == len(self.students):
            self.objects.clear()
        if pg.time.get_ticks() % 190 == 0:
            students = list(set(self.students) - set((obj.text for obj in self.objects)))
            student = Text(self.game, students[randint(0,len(students)-1)], 10, color=Color.WHITE)
            student.move_center(self.start_pos, randint(10, self.game.height-10))
            student.ttl = 0
            self.objects.append(student)
            self.on_screen += 1
        for student in self.objects:
            if student.rect.x >= self.game.width:
                self.on_screen -= 1
                student.rect.x = -101
            elif student.rect.x != -101:
                student.ttl += 1
                student.rect.x = student.ttl * self.speed + self.start_pos
                student.surface.set_alpha(min(255, self.game.width-((student.rect.midbottom[0] - self.game.width//2)**2
                                                                    * 0.06 - self.alpha_delta)))
                self.game.screen.blit(student.surface, (student.rect.x, student.rect.y))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.set_scene(0)
            self.on_screen = 0
            self.objects = []



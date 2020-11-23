import pygame as pg
from random import randint
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Font


class CreditsScene(BaseScene):
    data = [
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
        "Акимов Денис",
        "Богомолов Алексей",
        "Вартанян Владимир",
        "Дмитрий Пашков",
        "Киселева Алиса",
        "Николайчев Павел",
        "Оркин Родион",
        "Плотский Богдан",
        "Татаринов Игорь",
        "Терпунов Артём",
        "Тимченко Савелий",
        "Щеников Иван",
        "Вадимир Путин",
        "Дмитрий Медведев",
        "Хаяо Миядзаки",
        "Джонатан Джостар",
        "Тору Иватани",
        "Фил Спенсер"
    ]

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.on_screen = 0
        self.start_pos = -30
        self.speed = 0.3
        self.alpha_delta = -15
        self.students = []

    def create_student(self):
        students = list(set(self.data) - set((obj.text for obj in self.students)))
        label = str(students[randint(0, len(students) - 1)])
        student = Text(self.game, label, Font.TITERS_SCENE_SIZE, font=Font.ALTFONT)
        student.move_center(self.start_pos, randint(10, self.game.height - 10))
        student.speed = self.speed + randint(-5, 15) / 100
        student.ttl = 0
        self.students.append(student)
        self.objects.append(student)
        self.on_screen += 1

    def process_students(self) -> None:
        for student in self.students:
            if student.rect.x >= self.game.width:
                self.on_screen -= 1
                student.move(-105, student.rect.y)
            elif student.rect.x != -105:
                student.ttl += 1
                student.move(student.ttl * student.speed + self.start_pos, student.rect.y)
                student.surface.set_alpha(min(255, self.game.width - ((student.rect.midbottom[0] - self.game.width // 2) ** 2
                                                * 0.06 - self.alpha_delta)))

    def additional_logic(self) -> None:
        if len(self.students) == len(self.data) and not self.on_screen:
            self.students.clear()
        elif pg.time.get_ticks() % 190 == 0 and not len(self.students) == len(self.data):
            self.create_student()
        self.process_students()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.scenes[self.game.current_scene_name] == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene('SCENE_MENU')
                self.on_screen = 0
                self.students = []
                self.objects = []

from random import randint

import pygame as pg

import scenes
from misc.constants import Font
from objects import Text
from objects.buttons import Button


class CreditsScene(scenes.BaseScene):

    # todo Name region
    __data = [
        "Смирнов Андрей",
        "Aleksandrov Daniil",
        "Сергеев Сергей",
        "Лещенко Вячеcлав",
        "Вартанян Владимир",
        "Дмитрий Пашков",
        "Николайчев Павел",
    ]

    # region Public

    # region Implementation of IGenericObject

    def additional_logic(self) -> None:
        if self.__students2:
            self.__students2 = self.__data.copy()
        elif len(self.__students) == len(self.__students2) and not self.__on_screen:
            self.__students.clear()
        elif pg.time.get_ticks() // 2 % 100 == 0 and not len(self.__students) == len(self.__students2):
            self.__create_student()
        if not self.game.sounds.credits.is_busy():
            self.game.sounds.reload_sounds()
            self.game.sounds.credits.play()
        self.__process_students()

    # endregion

    def on_exit(self) -> None:
        self.game.sounds.credits.stop()

    # endregion

    # region Private

    # region Implementation of BaseScene

    def _create_objects(self) -> None:
        super()._create_objects()
        self.__on_screen = 0
        self.start_pos = -30
        self.__speed = 0.3
        self.__alpha_delta = -15
        self.__students = []
        self.__students2 = self.__data.copy()

    def _button_init(self) -> None:
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 100, 35),
            function=self._scene_manager.pop,
            text="MENU",
            center=(self.game.width // 4, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

        yield Button(game=self.game,
                     rect=pg.Rect(0, 0, 100, 35),
                     text="SKIP",
                     function=self.__skip_sound,
                     center=(self.game.width // 4 + 110, 250),
                     text_size=Font.BUTTON_TEXT_SIZE)

    # endregion

    def __get_random_student_y(self) -> int:
        return randint(25, self.game.height - 75)

    def __create_student(self) -> None:
        students = list(set(self.__students2) - set((obj.text for obj in self.__students)))
        label = str(students[randint(0, len(students) - 1)])
        self.__students2.pop(self.__students2.index(label))
        student = Text(label, Font.CREDITS_SCENE_SIZE)

        is_student_y_correct = False
        tries = 0
        while not is_student_y_correct:
            student.move_center(self.start_pos, randint(25, self.game.height - 75))
            is_student_y_correct = True
            for student2 in self.__students:
                if abs(student.rect.centery - student2.rect.centery) <= (student.rect.height + student2.rect.height)/2:
                    is_student_y_correct = False
                    break
            tries += 1
            if tries > 100:
                break
        student.speed = self.__speed + randint(-5, 15) / 100
        student.ttl = 0
        self.__students.append(student)
        self.objects.append(student)
        self.__on_screen += 1

    def __process_students(self) -> None:
        students_to_delete = []
        for index, student in enumerate(self.__students):
            if student.rect.x >= self.game.width:
                students_to_delete.append(index)
                self.__on_screen -= 1
            elif student.rect.x != -105:
                student.ttl += 1
                student.move(student.ttl * student.speed + self.start_pos, student.rect.y)
                student.surface.set_alpha(
                    min(
                        255,
                        self.game.width - (
                            (student.rect.midbottom[0] - self.game.width // 2) ** 2 * 0.06 - self.__alpha_delta)
                    )
                )

        for index in sorted(students_to_delete, reverse=True):
            self.objects.remove(self.__students[index])
            del self.__students[index]

    def __skip_sound(self):
        self.game.sounds.reload_sounds()
        self.game.sounds.credits.play()

    # endregion

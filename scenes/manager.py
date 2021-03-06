import pygame as pg

from meta_classes import Singleton
from misc.interfaces import IGenericObject
from scenes.base import BaseScene


class FinalMeta(type(IGenericObject), type(Singleton)):
    pass


class SceneManager(IGenericObject, Singleton, metaclass=FinalMeta):

    def __init__(self):
        self.scenes: list[BaseScene] = []

    @property
    def __is_empty(self) -> bool:
        return len(self.scenes) <= 0

    @property
    def current(self) -> BaseScene:
        if not self.__is_empty:
            return self.scenes[-1]
        raise Exception('Пустая сцена')

    def exit_scene(self) -> None:
        if not self.__is_empty:
            self.current.on_exit()

    def process_logic(self) -> None:
        self.current.process_logic()
        self.current.additional_logic()

    def process_event(self, event) -> None:
        self.current.process_event(event)
        self.current.additional_event(event)

    def process_draw(self, screen: pg.Surface) -> None:
        self.current.process_draw(screen)
        self.current.additional_draw(screen)

    def append(self, scene: BaseScene) -> None:
        self.exit_scene()
        scene.configure()
        self.scenes.append(scene)
        self.current.on_enter()

    def pop(self) -> None:
        self.exit_scene()
        self.scenes.pop()
        self.current.on_enter()

    def swap(self, scene: BaseScene) -> None:
        self.scenes.pop()
        self.scenes.append(scene)

    def reset(self, scene: BaseScene) -> None:
        self.scenes.clear()
        self.append(scene)

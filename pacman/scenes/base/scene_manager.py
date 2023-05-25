from pygame import Surface

from pacman.misc.singleton import Singleton

from .base_scene import BaseScene


class SceneManager(Singleton):
    def __init__(self):
        self.__scenes: list[BaseScene] = []

    @property
    def current(self) -> BaseScene:
        try:
            return self.__scenes[-1]
        except IndexError:
            raise Exception("List of scenes is empty")

    def on_exit_scene(self) -> None:
        if self.__scenes:
            self.current.on_exit()

    def on_last_exit_scene(self) -> None:
        if self.__scenes:
            self.current.on_last_exit()

    def process_logic(self) -> None:
        self.current.process_logic()

    def process_event(self, event) -> None:
        self.current.process_event(event)

    def process_draw(self) -> Surface:
        return self.current.draw()

    def append(self, scene: BaseScene) -> None:
        self.on_exit_scene()
        scene.setup()
        scene.on_first_enter()
        self.__scenes.append(scene)

    def pop(self) -> BaseScene:
        self.on_last_exit_scene()
        pop_scene = self.__scenes.pop()
        self.current.on_enter()
        return pop_scene

    def reset(self, scene: BaseScene) -> None:
        for s in self.__scenes:
            s.on_last_exit()
        scene.setup()
        scene.on_first_enter()
        self.__scenes = [scene]

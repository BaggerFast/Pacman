from pygame import Surface

from pacman.misc.singleton import Singleton

from .base_scene import BaseScene


class SceneManager(Singleton):
    def __init__(self):
        self.scenes: list[BaseScene] = []

    @property
    def current(self) -> BaseScene:
        try:
            return self.scenes[-1]
        except IndexError:
            raise Exception("List of scenes is empty")

    def exit_scene(self) -> None:
        if self.scenes:
            self.current.on_exit()

    def process_logic(self) -> None:
        self.current.process_logic()

    def process_event(self, event) -> None:
        self.current.process_event(event)

    def process_draw(self) -> Surface:
        return self.current.draw()

    def append(self, scene: BaseScene) -> None:
        self.exit_scene()
        scene.setup()
        scene.on_enter()
        self.scenes.append(scene)

    def pop(self) -> BaseScene:
        self.exit_scene()
        pop_scene = self.scenes.pop()
        self.current.on_enter()
        return pop_scene

    def reset(self, scene: BaseScene) -> None:
        self.exit_scene()
        scene.setup()
        self.scenes = [scene]

from misc.patterns import Singleton
import pygame as pg


class SceneManager(Singleton):

    def __init__(self):
        self.scenes: list = []

    @property
    def is_empty(self) -> bool:
        return len(self.scenes) <= 0

    @property
    def current(self):
        if not self.is_empty:
            return self.scenes[-1]
        raise Exception('Пустая сцена')

    def exit_scene(self) -> None:
        if not self.is_empty:
            self.current.on_exit()

    def process_logic(self) -> None:
        self.current.process_logic()
        self.current.additional_logic()

    def process_event(self, event) -> None:
        self.current.process_event(event)
        # self.current.additional_event(event)

    def process_draw(self, screen: pg.Surface) -> None:
        self.current.render()
        self.current.additional_draw()

    def append(self, scene) -> None:
        self.exit_scene()
        scene.on_enter()
        self.scenes.append(scene)

    def pop(self) -> None:
        self.exit_scene()
        self.scenes.pop()

    def swap(self, scene) -> None:
        self.scenes.pop()
        scene.on_enter()
        self.scenes.append(scene)

    def reset(self, scene) -> None:
        self.scenes.clear()
        scene.on_activate()
        self.append(scene)

    def clear(self):
        self.scenes.clear()

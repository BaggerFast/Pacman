import pygame


class BaseScene:
    def __init__(self, screen, control=None) -> None:
        self.screen = screen
        self.control = control
        self.objects = []
        self.createObjects()

    def createObjects(self) -> None:
        pass

    def onActivate(self) -> None:
        pass

    def onWindowResize(self) -> None:
        pass

    def processEvent(self, event: pygame.event.Event) -> None:
        for item in self.objects:
            item.processEvent(event)
        self.additionalEventCheck(event)

    def additionalEventCheck(self, event: pygame.event.Event) -> None:
        pass

    def processLogic(self) -> None:
        for item in self.objects:
            item.processLogic()
        self.additionalLogic()

    def additionalLogic(self) -> None:
        pass

    def processDraw(self) -> None:
        for item in self.objects:
            item.process_draw()
        self.additionalDraw()

    def additionalDraw(self) -> None:
        pass

    def onDeactivate(self) -> None:
        pass

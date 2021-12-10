import pygame as pg


class Cheat:
    def __init__(self, game, code, func):
        self.cheat_code = code
        self.function = func
        self.game = game

    def logic(self) -> None:
        self.game.sounds.cheat.play()
        self.function()


class ControlCheats:

    def __init__(self, cheats: list[Cheat]):
        self.cheats: list[Cheat] = cheats
        self.timer = pg.time.get_ticks()
        self.enter_code: str = ''
        self.old_enter_code: str = ''

    def update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def process_logic(self) -> None:
        for cheat in self.cheats:
            if cheat.cheat_code == self.enter_code:
                cheat.logic()
                self.enter_code = ''
        if self.old_enter_code == self.enter_code and pg.time.get_ticks() - self.timer >= 1000:
            self.enter_code = ''
            self.update_timer()
        elif self.old_enter_code != self.enter_code:
            self.update_timer()
        self.old_enter_code = self.enter_code

    def process_event(self, event) -> None:
        if event.type == pg.KEYDOWN and event.key in range(pg.K_a, pg.K_z + 1):
            self.enter_code += chr(event.key)

    def process_draw(self) -> None:
        pass


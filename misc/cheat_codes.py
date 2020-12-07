import pygame as pg


class ControlCheatCodes:
    class CheatCode:
        def __init__(self, cheat_code: str, function):
            self.cheat_code = cheat_code
            self.function = function

        def run(self):
            self.function()

    def __init__(self, cheat_codes):
        self.cheat_codes = cheat_codes
        self.timer = pg.time.get_ticks()
        self.enter_code = ''
        self.old_enter_code = ''

    def update_timer(self):
        self.timer = pg.time.get_ticks()

    def process_logic(self):
        if self.old_enter_code == self.enter_code and pg.time.get_ticks() - self.timer >= 1000:
            self.enter_code = ''
            self.update_timer()
        elif self.old_enter_code != self.enter_code:
            self.update_timer()
        self.old_enter_code = self.enter_code

    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in range(pg.K_a, pg.K_z + 1):
                self.enter_code += event.unicode

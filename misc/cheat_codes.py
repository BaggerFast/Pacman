import pygame as pg

import misc


class Cheat:
    def __init__(self, cheat):
        self.cheat_code = cheat[0]
        self.function = cheat[1]

    def run(self):
        self.function()

    def check_enter_code(self, enter_code):
        if enter_code == self.cheat_code:
            self.run()


class ControlCheats:
    def __init__(self, cheat_codes):
        self.cheats = []
        for cheat in cheat_codes:
            self.cheats.append(Cheat(cheat))
        self.timer = pg.time.get_ticks()
        self.enter_code = ''
        self.old_enter_code = ''

    def update_timer(self):
        self.timer = pg.time.get_ticks()

    def process_logic(self):
        for cheat in self.cheats:
            cheat.check_enter_code(self.enter_code)
        if self.old_enter_code == self.enter_code and pg.time.get_ticks() - self.timer >= 1000:
            self.enter_code = ''
            self.update_timer()
        elif self.old_enter_code != self.enter_code:
            self.update_timer()
        self.old_enter_code = self.enter_code

    def process_draw(self):
        pass

    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in range(pg.K_a, pg.K_z + 1):
                self.enter_code += event.unicode

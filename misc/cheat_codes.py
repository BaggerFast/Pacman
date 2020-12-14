import pygame as pg


class Cheat:
    def __init__(self, game, cheat) -> None:
        self.cheat_code = cheat[0]
        self.function = cheat[1]
        self.game = game

    def run(self) -> None:
        self.function()

    def check_enter_code(self, enter_code) -> bool:
        if enter_code == self.cheat_code:
            self.game.sounds.cheat.play()
            self.run()
            return True
        return False


class ControlCheats:
    def __init__(self, game, cheat_codes) -> None:
        self.cheats = []
        for cheat in cheat_codes:
            self.cheats.append(Cheat(game, cheat))
        self.timer = pg.time.get_ticks()
        self.enter_code = ''
        self.old_enter_code = ''

    def update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def process_logic(self) -> None:
        for cheat in self.cheats:
            if cheat.check_enter_code(self.enter_code):
                self.enter_code = ''
        if self.old_enter_code == self.enter_code and pg.time.get_ticks() - self.timer >= 1000:
            self.enter_code = ''
            self.update_timer()
        elif self.old_enter_code != self.enter_code:
            self.update_timer()
        self.old_enter_code = self.enter_code

    def process_draw(self) -> None:
        pass

    def process_event(self, event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key in range(pg.K_a, pg.K_z + 1):
                self.enter_code += chr(event.key)

from pygame import KEYDOWN, K_a, K_z, time
from pygame.event import Event

from pacman.data_core import IEventful, ILogical


class Cheat:
    def __init__(self, cheat) -> None:
        self.cheat_code = cheat[0]
        self.function = cheat[1]

    def run(self) -> None:
        self.function()

    def check_enter_code(self, enter_code) -> bool:
        if enter_code == self.cheat_code:
            self.run()
            return True
        return False


class ControlCheats(ILogical, IEventful):
    def __init__(self, cheat_codes) -> None:
        self.cheats = []
        for cheat in cheat_codes:
            self.cheats.append(Cheat(cheat))
        self.timer = time.get_ticks()
        self.enter_code = ""
        self.old_enter_code = ""

    def update_timer(self) -> None:
        self.timer = time.get_ticks()

    def update(self) -> None:
        for cheat in self.cheats:
            if cheat.check_enter_code(self.enter_code):
                self.enter_code = ""
        if self.old_enter_code == self.enter_code and time.get_ticks() - self.timer >= 1000:
            self.enter_code = ""
            self.update_timer()
        elif self.old_enter_code != self.enter_code:
            self.update_timer()
        self.old_enter_code = self.enter_code

    def event_handler(self, event: Event):
        if event.type == KEYDOWN and event.key in range(K_a, K_z + 1):
            self.enter_code += event.unicode

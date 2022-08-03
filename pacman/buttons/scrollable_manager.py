from pacman.buttons import ButtonManager, Button


class ScrollableManager(ButtonManager):
    pass

    # def __init__(self, buttons: list[Button], count):
    #     self.all_buttons = buttons
    #     self.count = count
    #     super().__init__(buttons[:count])
    #
    # def move_down(self):
    #     self.deselect_cur_btn()
    #     self.active_button_index = (self.active_button_index + 1) % len(self.buttons)
    #     print(self.active_button_index, self.active_button_index + 1)
    #     print((self.count - 1 - self.active_button_index) % self.count)
    #     self.select_cur_btn()

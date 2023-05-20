from pygame import Surface, time

from pacman.data_core import ILogical


class Animator(ILogical):
    def __init__(self, images: tuple[Surface], time_out: int = 125, repeat: bool = True):
        self.__time_out = time_out
        self.__animate_timer = 0
        self.__repeat = repeat
        self.__run = True
        self.__images = images
        self._current_index = 0
        self.__is_anim_finished = False

    # region Public

    def update(self) -> None:
        tmp_time = time.get_ticks()
        if tmp_time - self.__animate_timer > self.__time_out and self.__run:
            self.__animate_timer = tmp_time
            self.__next_frame()

    @property
    def is_finished(self) -> bool:
        return self.__is_anim_finished

    @property
    def current_image(self) -> Surface:
        return self.__images[self._current_index]

    def stop(self) -> None:
        self.__run = False

    def start(self) -> None:
        self.__run = True

    def set_cur_image(self, index: int) -> None:
        self._current_index = index

    def reset(self):
        self._current_index = 0

    # endregion

    # region Private

    def __next_frame(self) -> None:
        current_frame_is_last = self._current_index == len(self) - 1
        if current_frame_is_last and not self.__repeat:
            self.stop()
            self.__is_anim_finished = True
            return
        self._current_index = (self._current_index + 1) % len(self)

    def __len__(self) -> int:
        return len(self.__images)

    # endregion

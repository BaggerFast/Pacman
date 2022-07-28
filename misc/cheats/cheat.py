import dataclasses
from typing import Callable

from loguru import logger


@dataclasses.dataclass
class Cheat:
    cheat_code: str
    function: Callable

    def __call__(self):
        logger.info(f'Active cheat: {self.cheat_code.lower()}')
        self.function()

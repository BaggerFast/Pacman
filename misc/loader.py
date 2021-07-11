from typing import Dict

from .base_from_file_loader import BaseFromFileLoader
from .from_image_loader import FromImageLoader
from .from_json_loader import FromJsonLoader
from .path import get_type_from_name

import time


def time_of_function(function):
    def wrapped(*args):
        start_time = time.perf_counter_ns()
        res = function(*args)
        print((time.perf_counter_ns() - start_time) / 1000000)
        return res

    return wrapped


class LevelLoader:
    loaders: Dict[str, BaseFromFileLoader] = {
        "json": FromJsonLoader,
        "png": FromImageLoader,
    }
    base_loader = FromImageLoader

    # @time_of_function
    def __init__(self, filename="1_map.json") -> None:
        self.filename: str = filename
        self.filetype: str = get_type_from_name(self.filename)
        self.data: BaseFromFileLoader = self.loaders.get(self.filetype, self.base_loader)(self.filename)

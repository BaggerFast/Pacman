from typing import Dict
from .base_from_file_loader import BaseFromFileLoader
from .from_json_loader import FromJsonLoader
from .path import get_type_from_name


class LevelLoader:
    loaders: Dict[str, BaseFromFileLoader] = {
        "json": FromJsonLoader
    }
    base_loader = FromJsonLoader

    def __init__(self, filename="1_map.json") -> None:
        self.filename: str = filename
        self.filetype: str = get_type_from_name(filename)
        self.data: BaseFromFileLoader = self.loaders.get(self.filetype, self.base_loader)(filename)

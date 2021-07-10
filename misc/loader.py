from typing import Dict
from .base_from_file_loader import BaseFromFileLoader
from .from_json_loader import FromJsonLoader
from .from_image_loader import FromImageLoader
from .path import get_type_from_name


class LevelLoader:
    loaders: Dict[str, BaseFromFileLoader] = {
        "json": FromJsonLoader,
        "png": FromImageLoader,
    }
    base_loader = FromImageLoader

    def __init__(self, filename="1_map.json") -> None:
        self.filename: str = filename
        self.filetype: str = get_type_from_name(self.filename)
        self.data: BaseFromFileLoader = self.loaders.get(self.filetype, self.base_loader)(self.filename)

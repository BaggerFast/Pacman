import os
from distutils.util import strtobool
from typing import List

ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))


def get_path(path) -> str:
    return os.path.join(*[ROOT_DIR] + path.lower().replace('\\', '/').split('/'))


def bool_venv_var(venv_variable: str):
    return os.getenv(venv_variable, "false").lower() == 'true'


def get_list_path(path, ext) -> List[str]:
    path = get_path(path)
    pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
    pathes.sort(key=lambda x: x.split(f'.{ext.strip(".")}'))
    return [os.path.join(*[path, f]) for f in pathes]


def create_file_if_not_exist(filepath: str, data: str = "") -> None:
    if os.path.exists(filepath):
        return
    file = open(filepath, 'w')
    file.write(data)
    file.close()

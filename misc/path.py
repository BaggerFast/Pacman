import os
from typing import List

ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))


def get_path(filename: str, extension: str, *folder: str) -> str:
    """
    :param filename: имя файла с расширением или без
    :param folder: указать папки через пробел слева на право без image
    :param extension: указать расширение файла
    :return: возращает полный путь файла строкой
    """
    folder = [i.lower() for i in folder]
    extension = '.' + extension.lower()
    filename = filename.lower() + extension
    return os.path.join(*[ROOT_DIR] + list(folder) + [filename])


def get_files_count(path: str) -> int:
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1
    return count


def get_list_path(extension: str, *folder: str) -> List[str]:
    """
    :param folder: указать папки через пробел слева на право без имени файла без image
    :param extension: указать расширение файла
    :return: возращает все пути до файлов для анимации автоматически
    """
    data = []
    folder = [i.lower() for i in folder]
    frames_count = get_files_count(os.path.join(*[ROOT_DIR] + list(folder)))
    extension = '.' + extension.lower()
    for i in range(frames_count):
        filename = str(i) + extension
        data.append(os.path.join(*[ROOT_DIR] + list(folder) + [filename]))
    return data


def create_file_if_not_exist(filepath: str, data: str = "") -> None:
    """
    :param filepath: path to file
    :param data: string which will written in file if it doesn't exist
    """
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.write(data)
        file.close()

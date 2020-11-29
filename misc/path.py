import os


ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))


def get_image_path(filename: str, *folder: str) -> str:
    """
    :param filename: имя файла с расширением или без
    :param folder: указать папки через пробел слева на право без image
    :return: возращает полный путь файла строкой
    """
    extension = '.png'
    if extension not in filename:
        filename += extension
    return os.path.join(*[ROOT_DIR, 'images'] + list(folder) + [filename])


def get_path(folder: str, filename: str, extension: str) -> str:
    """
    :param filename: имя файла с расширением или без
    :param folder: указать папки через пробел слева на право без image
    :param extension: указать расширение файла
    :return: возращает полный путь файла строкой
    """
    extension = '.' + extension
    return os.path.join(*[ROOT_DIR, folder] + [filename + extension])


def get_files_count(path: str) -> int:
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1
    return count


def get_list_path(folder: str, extension: str):
    """
    :param folder: указать папки через пробел слева на право без имени файла без image
    :param extension: указать расширение файла
    :return: возращает все пути до файлов для анимации автоматически
    """
    data = []
    folder_path = ROOT_DIR + '/' + folder
    frames_count = get_files_count(os.path.join(folder_path))
    extension = '.' + extension
    for i in range(frames_count):
        data.append(os.path.join(folder_path + '/' + str(i) + extension))
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

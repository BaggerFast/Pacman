import os

from misc.constants import ROOT_DIR


def get_image_path(name):
    return os.path.join(ROOT_DIR, 'images', name)
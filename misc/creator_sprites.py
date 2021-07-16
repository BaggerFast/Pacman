from PIL import Image
from misc.path import get_list_path, get_path


def create():
    r = 15
    name = 'chrome'
    p = 'dead'
    images = [Image.open(x) for x in get_list_path(path=f'images/pacman/{name}/{p}', ext='png')]
    res = r * len(images), r

    new_im = Image.new(mode='RGBA', size=res)

    for img in range(len(images)):
        new_im.paste(images[img], (img*r, 0))

    new_im.save(get_path(f'images/pacman/{name}/{p}.png'))

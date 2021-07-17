from PIL import Image
from misc.path import get_list_path, get_path


def create():
    r = 14
    data = ['fear1', 'fear2']
    for i in data:
        images = [Image.open(x) for x in get_list_path(path=f'images/ghost/{i}', ext='png')]
        res = r * len(images), r

        new_im = Image.new(mode='RGBA', size=res)

        for img in range(len(images)):
            new_im.paste(images[img], (img*r, 0))

        new_im.save(get_path(f'images/ghost/{i}.png'))

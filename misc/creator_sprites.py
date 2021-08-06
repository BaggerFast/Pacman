from PIL import Image
from misc.path import get_path


def create():
    data = ['right', 'bottom', 'left', 'top']
    images = []
    for name in data:
        images.append(Image.open(get_path(f"images/ghost/eaten/{name}/0.png")))
    width, height = images[0].size
    res = width, height * 4
    r = 12, 14
    new_im = Image.new(mode='RGBA', size=res)
    for i in range(len(images)):
        new_im.paste(images[i], (0, r[1]*i))
    new_im.save(get_path(f'images/ghost/eaten.png'))

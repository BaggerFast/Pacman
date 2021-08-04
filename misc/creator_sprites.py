from PIL import Image
from misc.path import get_path


def create():
    image = Image.open(get_path("images/pacman/default/walk.png"))
    width, height = image.size
    res = width, height * 4
    r = 13
    new_im = Image.new(mode='RGBA', size=res)
    new_im.paste(image, (0, 0))
    rotate = [2, 3, 4]
    for i in range(len(rotate)):
        data = Image.new(mode='RGBA', size=image.size)
        for j in range(4):
            local = image.crop((j*r, j*r, r*(j+1), r*(j+1)))
            data.paste(local.transpose(rotate[i]), (r*j, 0))
        new_im.paste(data, (0, r*(1+i)))
    new_im.save(get_path(f'images/pacman/default/test.png'))

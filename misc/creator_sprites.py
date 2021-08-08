from PIL import Image
from misc.path import get_path


def create():
    for name in ['chrome', 'half_life', 'default', 'edge', 'windows', 'pokeball']:
        image = Image.open(get_path(f"images/pacman/{name}/walk.png"))
        new_im = image.crop((0, 0, 54, 13))
        data = Image.new('RGBA', (54, 13))
        for i in range(4):
            temp = new_im.crop((i*13, 0, (i+1)*13, 13))
            temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
            data.paste(temp, (i*13, 0, (i+1)*13, 13))
        image.paste(data, (0, 26, 54, 39))
        image.save(get_path(f'images/pacman/{name}/walk.png'))

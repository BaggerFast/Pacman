from PIL import Image, ImageDraw
from misc.path import get_path


def create():
    # 14*8, 14
    # images = []
    # for name in range(7):
    #     images.append(Image.open(get_path(f"images/fruit/{name}.png")))
    # res = 14*7, 14
    # r = 14
    new_im = Image.new(mode='RGBA', size=(18, 9))
    black = Image.new(mode='RGBA', size=(9, 9))
    draw = ImageDraw.Draw(black)
    draw.ellipse((0, 0, 8, 8), 'white')
    white = Image.new(mode='RGBA', size=(9, 9))
    new_im.paste(black, (0, 0))
    new_im.paste(white, (10, 0))
    # for i in range(len(images)):
    #     temp = Image.new(mode='RGBA', size=(14, 14))
    #     old_size = images[i].size
    #     new_size = r, r
    #     temp.paste(images[i], (round((new_size[0]-old_size[0])/2), round((new_size[1]-old_size[1])/2)))
    #     new_im.paste(images[i], (i*r, 0))
    new_im.save(get_path(f'images/big_seed.png'))

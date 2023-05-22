from pygame import Surface, transform

from pacman.misc.utils import load_image

SIZE = tuple[int, int]


def sprite_slice(image: str | Surface, size: SIZE, scale: SIZE = None) -> tuple[Surface]:
    image = load_image(image) if isinstance(image, str) else image
    frames = []
    for i in range(image.get_width() // size[0]):
        frame = image.subsurface((i * size[0], 0, *size))
        if scale:
            frame = transform.scale(frame, scale)
        frames.append(frame)
    if not len(frames):
        raise ValueError("Sprite sheet is null")
    return tuple(frames)


def advanced_sprite_slice(image: str | Surface, size: SIZE, scale: SIZE = None) -> tuple[tuple[Surface]]:
    frames = []
    image = load_image(image) if isinstance(image, str) else image
    for i in range(image.get_height() // size[1]):
        frame = image.subsurface((0, i * size[1], image.get_width(), size[1]))
        frames.append(sprite_slice(frame, size, scale))
    if len(frames) != 4:
        raise ValueError("Sprite sheet not compatible with this size")
    return tuple(frames)

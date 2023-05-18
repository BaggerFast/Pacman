from pygame import Surface, transform

from pacman.misc.loaders import load_image


def sprite_slice(image: str | Surface, size: tuple[int, int], scale: tuple[int, int] = None) -> tuple[Surface]:
    if size[0] <= 0 or size[1] <= 0:
        raise Exception
    image = load_image(image) if isinstance(image, str) else image
    frames = []
    for i in range(image.get_width() // size[0]):
        frame = image.subsurface((i * size[0], 0, *size))
        if scale:
            frame = transform.scale(frame, scale)
        frames.append(frame)
    if not len(frames):
        raise Exception
    return tuple(frames)


def advanced_sprite_slice(
    image: str | Surface, size: tuple[int, int], scale: tuple[int, int] = None
) -> tuple[tuple[Surface]]:
    frames = []
    image = load_image(image) if isinstance(image, str) else image
    for i in range(image.get_height() // size[1]):
        frame = image.subsurface((0, i * size[1], image.get_width(), size[1]))
        frames.append(sprite_slice(frame, size, scale))
    if len(frames) != 4:
        raise Exception
    return tuple(frames)

from pygame import transform


def sprite_slice(image, size: tuple[int, int], scale: tuple[int, int] = None):
    if size[0] <= 0 or size[1] <= 0:
        raise Exception
    frames = []
    for i in range(image.get_width() // size[0]):
        frame = image.subsurface((i * size[0], 0, *size))
        if scale:
            scale = int(scale[0]), int(scale[1])
            frame = transform.scale(frame, scale)
        frames.append(frame)
    return tuple(frames)


def advanced_sprite_slice(image, size: tuple[int, int], scale: tuple[int, int] = None):
    frames = []
    for i in range(image.get_height() // size[1]):
        frame = image.subsurface((0, i * size[1], image.get_width(), size[1]))
        frames.append(sprite_slice(frame, size, scale))
    return tuple(frames)

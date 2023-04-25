from pygame import KEYDOWN, K_ESCAPE


def is_esc_pressed(event):
    return event.type == KEYDOWN and event.key == K_ESCAPE

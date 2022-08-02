from loguru import logger

from pacman import CHESS


# region important


@logger.catch(message='Critical problem')
def main():
    game = CHESS()
    game.main_loop()


# endregion


if __name__ == '__main__':
    main()

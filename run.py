from pacman import Game
from loguru import logger

from pacman.scenes import SceneManager


def logger_setup():
    logger.add('logs/log.log', format="{time} {level} {message}", level='INFO', rotation='1 day', compression="zip")


def singleton_init():
    SceneManager()


@logger.catch(message='Critical problem')
def main():
    logger.info('Game start')
    singleton_init()
    game = Game()
    game.main_loop()
    logger.info('Game finished')


if __name__ == '__main__':
    logger_setup()
    main()

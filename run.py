from loguru import logger
from pacman import Game


@logger.catch(message='Critical problem')
def main():
    game = Game()
    game.main_loop()


if __name__ == '__main__':
    main()

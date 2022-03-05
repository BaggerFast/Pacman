import os
import traceback
from datetime import datetime
from misc.constants import DEBUG
from game import Game


def parse_exceptions():
    if DEBUG:
        print(traceback.print_exc())
        return
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    with open(f"{log_directory}/{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log", "w") as file:
        file.write(traceback.format_exc())


def main():
    try:
        game = Game()
        game.main_loop()
    except Exception:
        parse_exceptions()


if __name__ == '__main__':
    main()

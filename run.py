import traceback
from datetime import datetime
from misc.constants import DEBUG
from game import Game


def parse_exceptions():
    if not DEBUG:
        with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
            file.write(traceback.format_exc())
    else:
        print(traceback.print_exc())


def main():
    try:
        game = Game()
        game.main_loop()
    except Exception:
        parse_exceptions()


if __name__ == '__main__':
    main()

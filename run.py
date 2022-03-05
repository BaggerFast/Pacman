import traceback
from datetime import datetime
from misc.constants import DEBUG
from game import Game


def main():
    try:
        game = Game()
        game.main_loop()
    except Exception:
        if not DEBUG:
            with open(f"logs/{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
                file.write(traceback.format_exc())
        else:
            print(traceback.print_exc())


if __name__ == '__main__':
    main()

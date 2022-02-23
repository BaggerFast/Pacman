import traceback
from datetime import datetime

from game import Game
from misc import DEBUG


def main():
    try:
        game = Game()
        game.main_loop()
        game.exit_game()
    except Exception:
        if not DEBUG:
            with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
                file.write(traceback.format_exc())
        else:
            print(traceback.print_exc())


if __name__ == '__main__':
    main()

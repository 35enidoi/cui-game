from src.game import main

from asciimatics.screen import Screen


if __name__ == "__main__":
    Screen.wrapper(main, arguments=[0.01])

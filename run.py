from src.main import main

from asciimatics.screen import Screen


if __name__ == "__main__":
    try:
        Screen.wrapper(main, arguments=[0.01])
    except KeyboardInterrupt:
        pass

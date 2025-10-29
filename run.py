from src.main import main

from asciimatics.screen import Screen


if __name__ == "__main__":
    try:
        Screen.wrapper(main)
    except KeyboardInterrupt:
        pass

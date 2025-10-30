from argparse import ArgumentParser

from src.main import main
from src.player import player_strategys

from asciimatics.screen import Screen


if __name__ == "__main__":
    parser = ArgumentParser(description="Invador game that control with Program.")
    parser.add_argument("--strategy", "-S", type=str, help="Player strategy to use.")
    args = parser.parse_args()

    strategy = 0

    if args.strategy is None:
        pass
    elif args.strategy not in map(lambda x: x.name, player_strategys):
        print(f"Unknown strategy: {args.strategy}")
        print("Available strategies:")
        for strategy in player_strategys:
            print(f"- {strategy.name}")
        exit(1)
    else:
        for i, st in enumerate(player_strategys):
            if st.name == args.strategy:
                strategy = i
                break
        strategy = next(i for i, s in enumerate(player_strategys) if s.name == args.strategy)

    try:
        Screen.wrapper(main, arguments=[strategy])
    except KeyboardInterrupt:
        pass

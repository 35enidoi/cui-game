from typing import Literal, TypedDict


PLAYER_ACTIONS = Literal["left", "right", "shoot", "none"]


class BaseEnemy:
    hitpoint: int
    position: tuple[int, int]
    move_direction: Literal["left", "right", "down"]
    move_distance: int
    move_count: int
    moved_count: int
    base_score: int
    current_count: int

    def move(self, width: int) -> None:
        raise NotImplementedError


class BasePlayerStrategy:
    description: str

    def __init__(self) -> None:
        pass

    def decide_action(self, game_state: "GameState") -> PLAYER_ACTIONS:
        raise NotImplementedError


class PlayerState(TypedDict):
    position: tuple[int, int]
    bullet_cooldown: int


class GameState(TypedDict):
    screen_size: tuple[int, int]
    deadline: int
    player: PlayerState
    enemies: list[BaseEnemy]
    bullets: list[tuple[int, int]]
    scores: list[int]

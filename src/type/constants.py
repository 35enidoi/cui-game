
from typing import Literal, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.type.abstracts import BaseEnemy


PLAYER_ACTIONS = Literal["left", "right", "shoot", "none"]

KEY_Q = 113
KEY_LOWQ = 81


class PlayerState(TypedDict):
    position: tuple[int, int]
    bullet_cooldown: int


class StageState(TypedDict):
    screen_size: tuple[int, int]
    deadline: int
    enemies: list["BaseEnemy"]
    scores: list[int]
    max_score: int
    bullets: list[tuple[int, int]]


class GameState(TypedDict):
    stage: StageState
    player: PlayerState


from typing import Literal, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.type.abstracts import BaseEnemy


PLAYER_ACTIONS = Literal["left", "right", "shoot", "none"]

KEY_Q = 113
KEY_LOWQ = 81


class PlayerState(TypedDict):
    position: tuple[int, int]
    bullet_cooldown: int


class GameState(TypedDict):
    screen_size: tuple[int, int]
    deadline: int
    player: PlayerState
    enemies: list["BaseEnemy"]
    bullets: list[tuple[int, int]]
    scores: list[int]

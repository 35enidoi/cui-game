from uuid import uuid4
from abc import ABC, abstractmethod


from typing import Literal, TypedDict


PLAYER_ACTIONS = Literal["left", "right", "shoot", "none"]


class BaseEnemy(ABC):
    hitpoint: int
    position: tuple[int, int]
    move_direction: Literal["left", "right", "down"]
    move_distance: int
    move_count: int
    base_score: int

    _moved_count: int
    _id: str

    def __init__(self) -> None:
        self._moved_count = 0
        self._id = uuid4().hex

    @property
    def id(self) -> str:
        return self._id

    @property
    def moved_count(self) -> int:
        return self._moved_count

    def move(self, width: int) -> None:
        self._moved_count += 1

        if self._moved_count % self.move_count == 0:
            self._move(width)

    @abstractmethod
    def _move(self, width: int) -> None:
        ...


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

from uuid import uuid4
from abc import ABC, abstractmethod


from typing import Literal

from src.type.constants import GameState, PLAYER_ACTIONS


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


class BasePlayerStrategy(ABC):
    description: str

    def __init__(self) -> None:
        pass

    @abstractmethod
    def decide_action(self, game_state: "GameState") -> PLAYER_ACTIONS:
        raise NotImplementedError

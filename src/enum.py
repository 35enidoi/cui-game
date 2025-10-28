from typing import Literal


PLAYER_ACTIONS = Literal["left", "right", "shoot", "none"]


class BaseEnemy:
    hitpoint: int
    position: tuple[int, int]
    move_direction: Literal["left", "right", "down"]
    move_distance: int
    move_count: int
    base_score: int
    current_count: int

    def move(self, width: int) -> None:
        raise NotImplementedError

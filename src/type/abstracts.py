from uuid import uuid4
from abc import ABC, abstractmethod


from typing import Literal

from src.type.constants import GameState, PLAYER_ACTIONS, StageState


class BaseEnemy(ABC):
    hitpoint: int
    position: tuple[int, int]
    move_direction: Literal["left", "right", "down"]
    move_distance: int
    move_count: int
    base_score: int
    char: str

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
    name: str
    description: str

    def __init__(self) -> None:
        pass

    @abstractmethod
    def decide_action(self, game_state: "GameState") -> PLAYER_ACTIONS:
        raise NotImplementedError

    def reset(self) -> None:
        pass


class BaseGameStage(ABC):
    name: str
    description: str

    def __init__(self, screen_size: tuple[int, int]) -> None:
        deadline = 10 if screen_size[1] >= 20 else 7
        self.stage_state: StageState = {
            "screen_size": screen_size,
            "deadline": deadline,
            "enemies": [],
            "scores": [],
            "max_score": 0,
            "bullets": []
        }
        self.stage_reset()

    @property
    def is_game_over(self) -> bool:
        if not self.stage_state["enemies"]:
            return True
        elif any(enemy.position[1] <= self.stage_state["deadline"] for enemy in self.stage_state["enemies"]):
            return True
        else:
            return False

    def stage_reset(self) -> None:
        self.stage_state["enemies"] = self.enemy_initialization()
        self.stage_state["bullets"].clear()
        self.stage_state["max_score"] = max(self.stage_state["max_score"], sum(self.stage_state["scores"]))
        self.stage_state["scores"].clear()

    def bullet_add(self, position: tuple[int, int]) -> None:
        self.stage_state["bullets"].append(position)

    def emuration_step(self) -> list[tuple[BaseEnemy, int]]:
        destoroyed_enemys: list[tuple[BaseEnemy, int]] = []

        # 敵の移動
        for enemy in self.stage_state["enemies"]:
            enemy.move(self.stage_state["screen_size"][0])

        # 弾の移動と敵への命中判定
        new_bullets = []
        for bullet in self.stage_state["bullets"]:
            new_bullet_y = bullet[1] + 1

            if new_bullet_y >= self.stage_state["screen_size"][1] + 1:
                # 画面外に出た弾は削除
                continue

            for enemy_index, enemy in enumerate(self.stage_state["enemies"]):
                if enemy.position == (bullet[0], new_bullet_y):
                    # 命中した場合、敵の体力を減少させて消す
                    enemy.hitpoint -= 10

                    if enemy.hitpoint <= 0:
                        self.stage_state["enemies"].pop(enemy_index)

                        score = self.emuration_calculate_score(enemy)

                        self.stage_state["scores"].append(score)

                        destoroyed_enemys.append((enemy, score))

                    break
            else:
                # 命中しなかった弾は次の位置に移動
                new_bullets.append((bullet[0], new_bullet_y))

        self.stage_state["bullets"] = new_bullets

        return destoroyed_enemys

    def emuration_calculate_score(self, enemy: BaseEnemy) -> int:
        if enemy.base_score >= 50 and enemy.moved_count <= 150:
            bonus_score = (enemy.base_score // 50) * (150 - enemy.moved_count)
        else:
            bonus_score = 0

        return enemy.base_score + bonus_score

    @abstractmethod
    def enemy_initialization(self) -> list[BaseEnemy]:
        raise NotImplementedError

from typing import Callable, Optional
from random import shuffle

from src.type.constants import PLAYER_ACTIONS, GameState
from src.type.abstracts import BaseEnemy
from src.enemy import InvaderEnemy


class GameModel:
    def __init__(
            self,
            screen_height: int,
            screen_width: int) -> None:
        self.initialize_game((screen_width, screen_height))

    def initialize_game(self, screen_size: tuple[int, int], enemy_count: Optional[int] = None) -> None:
        self.gamestate: GameState = {
            "screen_size": screen_size,
            "deadline": 10,
            "player": {
                "position": (screen_size[0] // 2, 6),
                "bullet_cooldown": 0
            },
            "enemies": self._enemy_initialization(screen_size, enemy_count),
            "bullets": [],
            "scores": []
        }

    def _enemy_initialization(self, screen_size: tuple[int, int], enemy_count: Optional[int] = None) -> list[BaseEnemy]:
        screen_width, screen_height = screen_size

        if enemy_count is None:
            enemy_count = screen_height * (screen_height // 4) // 5

        screen_positions: list[tuple[int, int]] = []
        for y in range(10 if screen_height > 20 else screen_height // 4):
            for x in range(screen_width):
                screen_positions.append((x, screen_height - y))

        shuffle(screen_positions)

        if enemy_count > len(screen_positions):
            enemy_count = len(screen_positions)

        enemys = []

        for _ in range(enemy_count):
            x, y = screen_positions.pop()
            enemys.append(InvaderEnemy(x, y))

        return enemys

    @property
    def is_game_over(self) -> bool:
        if not self.gamestate["enemies"]:
            return True
        elif any(enemy.position[1] <= self.gamestate["deadline"] for enemy in self.gamestate["enemies"]):
            return True
        else:
            return False

    def emuration_step(self, player_strategy: Callable[[GameState], PLAYER_ACTIONS]) -> list[tuple[BaseEnemy, int]]:
        # プレイヤーの行動決定と実行
        destoroyed_enemys: list[tuple[BaseEnemy, int]] = []
        player_action = player_strategy(self.gamestate)

        match player_action:
            case "left":
                if self.gamestate["player"]["position"][0] > 0:
                    self.gamestate["player"]["position"] = (
                        self.gamestate["player"]["position"][0] - 1,
                        self.gamestate["player"]["position"][1]
                    )
            case "right":
                if self.gamestate["player"]["position"][0] < self.gamestate["screen_size"][0] - 1:
                    self.gamestate["player"]["position"] = (
                        self.gamestate["player"]["position"][0] + 1,
                        self.gamestate["player"]["position"][1]
                    )
            case "shoot":
                self.gamestate["bullets"].append(self.gamestate["player"]["position"])

        # 敵の移動
        for enemy in self.gamestate["enemies"]:
            enemy.move(self.gamestate["screen_size"][0])

        # 弾の移動と敵への命中判定
        new_bullets = []
        for bullet in self.gamestate["bullets"]:
            new_bullet_y = bullet[1] + 1

            if new_bullet_y >= self.gamestate["screen_size"][1] + 1:
                # 画面外に出た弾は削除
                continue

            for enemy_index, enemy in enumerate(self.gamestate["enemies"]):
                if enemy.position == (bullet[0], new_bullet_y):
                    # 命中した場合、敵の体力を減少させて消す
                    enemy.hitpoint -= 10
                    if enemy.hitpoint <= 0:
                        self.gamestate["enemies"].pop(enemy_index)

                        # スコア計算
                        if enemy.base_score >= 50 and enemy.moved_count <= 150:
                            bonus_score = (enemy.base_score // 50) * (150 - enemy.moved_count)
                        else:
                            bonus_score = 0

                        self.gamestate["scores"].append(enemy.base_score + bonus_score)
                        destoroyed_enemys.append((enemy, enemy.base_score + bonus_score))
                    break
            else:
                # 命中しなかった弾は次の位置に移動
                new_bullets.append((bullet[0], new_bullet_y))

        self.gamestate["bullets"] = new_bullets

        return destoroyed_enemys

    @staticmethod
    def screen_reverser(screen_y: int, position: tuple[int, int]) -> tuple[int, int]:
        """スクリーンのy座標が逆なのでそれを反映するやつ"""
        return position[0], abs(screen_y - position[1])

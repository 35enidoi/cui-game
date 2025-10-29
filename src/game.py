from typing import Callable
from time import sleep
from random import shuffle

from asciimatics.screen import Screen
from asciimatics.constants import COLOUR_WHITE

from src.enum import PLAYER_ACTIONS, BaseEnemy, GameState
from src.enemy import InvaderEnemy
from src.player import player_strategys


class GameModel:
    def __init__(
            self,
            screen_height: int,
            screen_width: int) -> None:
        self.initialize_game((screen_width, screen_height))

    def initialize_game(self, screen_size: tuple[int, int], enemy_count=10) -> None:
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

    def _enemy_initialization(self, screen_size: tuple[int, int], enemy_count: int) -> list[BaseEnemy]:
        screen_width, screen_height = screen_size
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

            if new_bullet_y >= self.gamestate["screen_size"][1]:
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


def screen_reverser(screen_y: int, position: tuple[int, int]) -> tuple[int, int]:
    """スクリーンのy座標が逆なのでそれを反映するやつ"""
    return position[0], abs(screen_y - position[1])


def main(screen: Screen, sleep_time: float) -> None:
    game = GameModel(screen.height, screen.width)
    max_score = 0
    destoroy_enemy_messages: list[tuple[int, str, tuple[int, int]]] = []

    while True:
        game.initialize_game(game.gamestate["screen_size"], enemy_count=40)
        destoroy_enemy_messages.clear()
        while not game.is_game_over:
            for i in reversed(range(len(destoroy_enemy_messages))):
                count, message, position = destoroy_enemy_messages[i]
                if count <= 0:
                    destoroy_enemy_messages.pop(i)
                else:
                    destoroy_enemy_messages[i] = (count - 1, message, position)

            screen.clear_buffer(COLOUR_WHITE, 0, 0)

            player = player_strategys["midareuti"]
            destroyed_enemies = game.emuration_step(player.decide_action)

            for enemy, score in destroyed_enemies:
                destoroy_enemy_messages.append((20, f"+{score}", screen_reverser(screen.height, enemy.position)))

            # スコア表示
            screen.print_at(f"Score: {sum(game.gamestate['scores'])}", 2, 0)
            screen.print_at(f"Max Score: {max_score}", 20, 0)

            # ゲームの表示
            screen.print_at("A", *screen_reverser(screen.height, game.gamestate["player"]["position"]))
            for enemy in game.gamestate["enemies"]:
                screen.print_at("M", *screen_reverser(screen.height, enemy.position))
            for bullet in game.gamestate["bullets"]:
                screen.print_at("|", *screen_reverser(screen.height, bullet))

            # 敵破壊メッセージの表示
            for _, message, position in destoroy_enemy_messages:
                screen.print_at(message, position[0], position[1])

            screen.refresh()

            sleep(sleep_time)

        max_score = sum(game.gamestate["scores"]) if sum(game.gamestate["scores"]) > max_score else max_score

    screen.close()

    print("Game Over! Your score:", sum(game.gamestate["scores"]))

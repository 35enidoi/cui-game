from typing import Callable
from time import sleep

from asciimatics.screen import Screen
from asciimatics.constants import COLOUR_WHITE

from src.enum import PLAYER_ACTIONS, GameState
from src.enemy import InvaderEnemy
from src.player import player


class GameModel:
    def __init__(
            self,
            screen_height: int,
            screen_width: int) -> None:
        self.initialize_game((screen_width, screen_height))

    def initialize_game(self, screen_size: tuple[int, int]) -> None:
        self.gamestate: GameState = {
            "screen_size": screen_size,
            "deadline": 10,
            "player": {
                "position": (screen_size[0] // 2, 6),
                "bullet_cooldown": 0
            },
            "enemies": [
                InvaderEnemy(x_position, screen_size[1] - 2)
                for x_position in range(2, screen_size[0] - 2, 4)
            ],
            "bullets": [],
            "scores": []
        }

    @property
    def is_game_over(self) -> bool:
        if not self.gamestate["enemies"]:
            return True
        elif any(enemy.position[1] <= self.gamestate["deadline"] for enemy in self.gamestate["enemies"]):
            return True
        else:
            return False

    def emuration_step(self, player_strategy: Callable[[GameState], PLAYER_ACTIONS]) -> None:
        # プレイヤーの行動決定と実行
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
                        self.gamestate["scores"].append(enemy.base_score + 10 * (new_bullet_y - self.gamestate["deadline"]))
                    break
            else:
                # 命中しなかった弾は次の位置に移動
                new_bullets.append((bullet[0], new_bullet_y))

        self.gamestate["bullets"] = new_bullets


def screen_reverser(screen_y: int, position: tuple[int, int]) -> tuple[int, int]:
    """スクリーンのy座標が逆なのでそれを反映するやつ"""
    return position[0], abs(screen_y - position[1])


def main(screen: Screen, sleep_time: float) -> None:
    game = GameModel(screen.height, screen.width)
    game.initialize_game((screen.width, screen.height))
    while not game.is_game_over:
        screen.clear_buffer(COLOUR_WHITE, 0, 0)

        game.emuration_step(player)

        screen.print_at(
            f"Score: {sum(game.gamestate['scores'])}",
            2,
            0
        )

        screen.print_at("A", *screen_reverser(screen.height, game.gamestate["player"]["position"]))
        for enemy in game.gamestate["enemies"]:
            screen.print_at("M", *screen_reverser(screen.height, enemy.position))
        for bullet in game.gamestate["bullets"]:
            screen.print_at("|", *screen_reverser(screen.height, bullet))

        screen.refresh()

        sleep(sleep_time)

    screen.close()

    print("Game Over! Your score:", sum(game.gamestate["scores"]))


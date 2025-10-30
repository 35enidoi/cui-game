from typing import Callable

from src.type.constants import PLAYER_ACTIONS, GameState
from src.type.abstracts import BaseEnemy, BaseGameStage


class GameModel:
    def __init__(self, stage: BaseGameStage) -> None:
        self.stage = stage
        self.initialize_game()

    @property
    def is_game_over(self) -> bool:
        return self.stage.is_game_over

    def initialize_game(self) -> None:
        self.stage.stage_reset()
        self.gamestate: GameState = {
            "player": {
                "position": (self.stage.stage_state["screen_size"][0] // 2, 6),
                "bullet_cooldown": 0
            },
            "stage": self.stage.stage_state,
        }

    def change_stage(self, stage: BaseGameStage) -> None:
        self.stage = stage
        self.initialize_game()

    def emuration_step(self, player_strategy: Callable[[GameState], PLAYER_ACTIONS]) -> list[tuple[BaseEnemy, int]]:
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
                if self.gamestate["player"]["position"][0] < self.gamestate["stage"]["screen_size"][0] - 1:
                    self.gamestate["player"]["position"] = (
                        self.gamestate["player"]["position"][0] + 1,
                        self.gamestate["player"]["position"][1]
                    )
            case "shoot":
                self.stage.bullet_add(self.gamestate["player"]["position"])

        # ステージのエミュレーションステップ実行
        destoroyed_enemys = self.stage.emuration_step()

        return destoroyed_enemys

    @staticmethod
    def screen_reverser(screen_y: int, position: tuple[int, int]) -> tuple[int, int]:
        """スクリーンのy座標が逆なのでそれを反映するやつ"""
        return position[0], abs(screen_y - position[1])

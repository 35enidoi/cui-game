from random import shuffle

from src.type.abstracts import BaseEnemy, BaseGameStage
from src.enemy import InvaderEnemy


class InvaderStage(BaseGameStage):
    name = "Invader Stage"
    description = "A stage where invader-type enemies appear."

    def enemy_initialization(self) -> list[BaseEnemy]:
        screen_width, screen_height = self.stage_state["screen_size"]

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

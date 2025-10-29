from random import randint

from src.enum import BasePlayerStrategy, BaseEnemy


class TekitouStrategy(BasePlayerStrategy):
    def decide_action(self, game_state):
        enemies = game_state["enemies"]
        position = game_state["player"]["position"]

        if not enemies:
            return "none"

        enemy_x_positions = {enemy.position[0] for enemy in enemies}
        front_enemies: list[BaseEnemy] = []
        for x in enemy_x_positions:
            front_enemies.append(
                min(
                    (e for e in enemies if e.position[0] == x),
                    key=lambda z: z.position[1]
                )
            )

        most_near_enemy = min(front_enemies, key=lambda e: abs(e.position[1] - position[1]))

        # 敵の動きを予測して移動または攻撃を決定
        move_count, move_distance = most_near_enemy.move_count, most_near_enemy.move_distance
        predict_hit_time = abs(most_near_enemy.position[1] - position[1])

        predict_bullet_shoot_pos = most_near_enemy.position[0]
        match most_near_enemy.move_direction:
            case "left":
                predict_bullet_shoot_pos -= (predict_hit_time // (move_count)) * move_distance
            case "right":
                predict_bullet_shoot_pos += (predict_hit_time // (move_count)) * move_distance

        predict_bullet_shoot_pos += randint(-most_near_enemy.move_count, most_near_enemy.move_count)  # 少しランダム要素を加える

        if predict_bullet_shoot_pos < 0 or predict_bullet_shoot_pos >= game_state["screen_size"][0]:
            if position[0] == 0 or position[0] == game_state["screen_size"][0] - 1:
                return "shoot"

        if predict_bullet_shoot_pos < position[0]:
            return "left"
        elif predict_bullet_shoot_pos > position[0]:
            return "right"
        else:
            return "shoot"


class MidareutiStrategy(BasePlayerStrategy):
    def __init__(self) -> None:
        self.directions = ("left", "right")
        self.count = 0
        self.direction_count = 0

    def decide_action(self, game_state):
        self.count += 1
        if self.count % 2:
            return "shoot"

        if game_state["player"]["position"][0] == 0 or game_state["player"]["position"][0] == game_state["screen_size"][0] - 1:
            self.direction_count += 1

        return self.directions[self.direction_count % 2]


player_strategys: dict[str, BasePlayerStrategy] = {
    "tekitou": TekitouStrategy(),
    "midareuti": MidareutiStrategy()
}

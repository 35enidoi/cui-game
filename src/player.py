from src.enum import PLAYER_ACTIONS, GameState

from random import randint


def nearest_shot(game_state: GameState) -> PLAYER_ACTIONS:
    enemies = game_state["enemies"]
    position = game_state["player"]["position"]

    if not enemies:
        return "none"

    enemy_x_positions = {enemy.position[0] for enemy in enemies}
    nearest_enemies = [min(enemies, key=lambda z: 0 if z.position[0] != x else abs(z.position[1] - position[1])) for x
                       in enemy_x_positions]

    most_near_enemy = min(nearest_enemies, key=lambda e: abs(e.position[1] - position[1]))

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


player = nearest_shot

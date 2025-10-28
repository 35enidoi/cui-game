from typing import Literal, Callable, Sequence
from time import sleep

from asciimatics.screen import Screen
from asciimatics.constants import COLOUR_WHITE


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


class InvaderEnemy(BaseEnemy):
    move_count = 3

    def __init__(self, x_position: int, y_position: int) -> None:
        self.hitpoint = 10
        self.position = (x_position, y_position)
        self.move_direction = "down"
        self.move_distance = 1
        self.current_count = self.move_count
        self.base_score = 100

    def move(self, width: int) -> None:
        if self.current_count < 0:
            self.current_count = self.move_count
            x, y = self.position
            match self.move_direction:
                case "left":
                    if x > 0:
                        self.position = (x - 1, y)
                    else:
                        self.move_direction = "down"
                case "right":
                    if x < width - 1:
                        self.position = (x + 1, y)
                    else:
                        self.move_direction = "down"
                case "down":
                    self.position = (x, y - 1)
                    self.move_direction = "left" if x > width // 2 else "right"
        else:
            self.current_count -= 1


def player(screen_size: tuple[int, int], position: tuple[int, int], enemies: Sequence[BaseEnemy]) -> PLAYER_ACTIONS:
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

    if predict_bullet_shoot_pos < 0 or predict_bullet_shoot_pos >= screen_size[0]:
        if position[0] == 0 or position[0] == screen_size[0] - 1:
            return "shoot"

    if predict_bullet_shoot_pos < position[0]:
        return "left"
    elif predict_bullet_shoot_pos > position[0]:
        return "right"
    else:
        return "shoot"


class GameModel:
    def __init__(self,
                 screen_height: int,
                 screen_width: int,
                 player_strategy: Callable[[tuple[int, int], tuple[int, int], Sequence[BaseEnemy]], PLAYER_ACTIONS]) -> None:
        self.enemy_list: list[BaseEnemy] = []
        self.player_position = (screen_width // 2, 6)
        self.player_strategy = player_strategy
        self.scores: list[int] = []
        self.bullets: list[tuple[int, int]] = []
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.deadline = 10

    @property
    def is_game_over(self) -> bool:
        if not self.enemy_list:
            return True
        elif any(enemy.position[1] <= self.deadline for enemy in self.enemy_list):
            return True
        else:
            return False

    def initialize_game(self) -> None:
        self.enemy_list = [InvaderEnemy(x, self.screen_height - 1 - y) for y in range(3) for x in range(5)]

    def emuration_step(self) -> None:
        # プレイヤーの行動決定と実行
        player_action = self.player_strategy((self.screen_width, self.screen_height), self.player_position, self.enemy_list)
        match player_action:
            case "left":
                if self.player_position[0] > 0:
                    self.player_position = (self.player_position[0] - 1, self.player_position[1])
            case "right":
                if self.player_position[0] < self.screen_width - 1:
                    self.player_position = (self.player_position[0] + 1, self.player_position[1])
            case "shoot":
                self.bullets.append((self.player_position[0], self.player_position[1] + 1))

        # 敵の移動
        for enemy in self.enemy_list:
            enemy.move(self.screen_width)

        # 弾の移動と敵への命中判定
        new_bullets = []
        for bullet in self.bullets:
            new_bullet_y = bullet[1] + 1

            if new_bullet_y >= self.screen_height:
                # 画面外に出た弾は削除
                continue

            for enemy_index, enemy in enumerate(self.enemy_list):
                if enemy.position == (bullet[0], new_bullet_y):
                    # 命中した場合、敵の体力を減少させて消す
                    enemy.hitpoint -= 10
                    if enemy.hitpoint <= 0:
                        self.enemy_list.pop(enemy_index)
                        self.scores.append(enemy.base_score + 10 * (new_bullet_y - self.deadline))
                    break
            else:
                # 命中しなかった弾は次の位置に移動
                new_bullets.append((bullet[0], new_bullet_y))

        self.bullets = new_bullets


def main(screen: Screen, sleep_time: float) -> None:
    game = GameModel(screen.height, screen.width, player)
    game.initialize_game()
    while not game.is_game_over:
        screen.clear_buffer(COLOUR_WHITE, 0, 0)

        game.emuration_step()
        screen.print_at("A", *game.player_position)
        for enemy in game.enemy_list:
            screen.print_at("M", *enemy.position)
        for bullet in game.bullets:
            screen.print_at("|", *bullet)

        screen.refresh()

        sleep(sleep_time)

    screen.close()


if __name__ == "__main__":
    Screen.wrapper(main, arguments=[0])

from collections import defaultdict

from src.type.abstracts import BasePlayerStrategy, BaseEnemy


class PredictStrategy(BasePlayerStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.target_enemy_id: str | None = None
        self.shooted_enemys: list[tuple[int, str]] = []

    name = "Predict"

    def target_enemy(self, enemies: list[BaseEnemy], player_position: tuple[int, int]) -> BaseEnemy | None:
        for enemy in enemies:
            if enemy.id == self.target_enemy_id:
                return enemy
        else:
            enemy_key_x = defaultdict(list)
            for e in enemies:
                if e.id not in [se[1] for se in self.shooted_enemys]:
                    enemy_key_x[e.position[0]].append(e)

            if not enemy_key_x:
                return None

            near_x = min(enemy_key_x.keys(), key=lambda x: abs(x - player_position[0]))

            most_near_enemy = min(enemy_key_x[near_x], key=lambda e: abs(e.position[1] - player_position[1]))

            self.target_enemy_id = most_near_enemy.id

            return most_near_enemy

    def _predict_intersection_x(self, enemy: BaseEnemy, player_y: int, screen_size: tuple[int, int]) -> tuple[int, int]:
        """弾がplayer_yから上昇し、敵と同じyに到達する時点の敵xをシミュレーションで求める。
        GameModelの更新順序(敵move→弾move→当たり判定)に合わせて進める。
        返り値は予測される敵のx座標と当たるまでのフレーム数。
        """
        width, height = screen_size
        ex, ey = enemy.position
        direction = enemy.move_direction
        moved = enemy.moved_count
        move_count = enemy.move_count

        bullet_y = player_y

        # 最大でも画面高分だけ進めば十分
        for _ in range(height + 2):
            # 敵の更新(このフレームで移動するか判定)
            moved += 1
            if move_count > 0 and moved % move_count == 0:
                match direction:
                    case "left":
                        if ex > 0:
                            ex -= 1
                        else:
                            direction = "down"
                    case "right":
                        if ex < width - 1:
                            ex += 1
                        else:
                            direction = "down"
                    case "down":
                        ey -= 1
                        direction = "left" if ex > width // 2 else "right"

            # 弾の更新
            bullet_y += 1

            # 当たり判定(同じyに到達した時点で交差を想定)
            if bullet_y == ey:
                return ex, bullet_y

        # フォールバック: シミュレーションしきれない場合は現在位置
        return ex, bullet_y

    def decide_action(self, game_state):
        player_position = game_state["player"]["position"]
        screen_size = game_state["screen_size"]

        for index, (bullet_y, enemy_id) in enumerate(self.shooted_enemys):
            if bullet_y - player_position[1] <= 0:
                self.shooted_enemys.pop(index)
            else:
                self.shooted_enemys[index] = (bullet_y - 1, enemy_id)

        enemy = self.target_enemy(game_state["enemies"], game_state["player"]["position"])

        if enemy is None:
            return "none"

        target_x, bullet_y = self._predict_intersection_x(enemy, player_position[1], screen_size)

        # 端での挙動(画面外予測はしないが、端に張り付いた時は撃つ)
        if player_position[0] in (0, screen_size[0] - 1):
            if player_position[0] == target_x:
                return "shoot"

        if target_x < player_position[0]:
            return "left"
        elif target_x > player_position[0]:
            return "right"
        else:
            self.shooted_enemys.append((bullet_y, enemy.id))
            self.target_enemy_id = None
            return "shoot"


class MidareutiStrategy(BasePlayerStrategy):
    name = "Midareuti"

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


player_strategys: tuple[BasePlayerStrategy, ...] = (
    PredictStrategy(),
    MidareutiStrategy(),
)

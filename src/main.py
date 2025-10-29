from time import sleep

from asciimatics.screen import Screen
from asciimatics.constants import COLOUR_WHITE

from src.player import player_strategys
from src.game import GameModel


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
                destoroy_enemy_messages.append((20, f"+{score}", GameModel.screen_reverser(screen.height, enemy.position)))

            # スコア表示
            screen.print_at(f"Score: {sum(game.gamestate['scores'])}", 2, 0)
            screen.print_at(f"Max Score: {max_score}", 20, 0)

            # ゲームの表示
            screen.print_at("A", *GameModel.screen_reverser(screen.height, game.gamestate["player"]["position"]))
            for enemy in game.gamestate["enemies"]:
                screen.print_at("M", *GameModel.screen_reverser(screen.height, enemy.position))
            for bullet in game.gamestate["bullets"]:
                screen.print_at("|", *GameModel.screen_reverser(screen.height, bullet))

            # 敵破壊メッセージの表示
            for _, message, position in destoroy_enemy_messages:
                screen.print_at(message, position[0], position[1])

            screen.refresh()

            sleep(sleep_time)

        max_score = sum(game.gamestate["scores"]) if sum(game.gamestate["scores"]) > max_score else max_score

    screen.close()

    print("Game Over! Your score:", sum(game.gamestate["scores"]))

from time import sleep
from typing import cast

from asciimatics.screen import Screen
from asciimatics.constants import COLOUR_WHITE
from asciimatics.event import KeyboardEvent

from src.player import player_strategys
from src.type.constants import KEY_Q, KEY_LOWQ
from src.game import GameModel


def main(screen: Screen) -> None:
    def draw():
        # 画面クリア
        screen.clear_buffer(COLOUR_WHITE, 0, 0)

        # デッドラインの表示
        screen.move(*GameModel.screen_reverser(screen.height, (0, game.gamestate["deadline"])))
        screen.draw(*GameModel.screen_reverser(screen.height, (screen.width, game.gamestate["deadline"])), char="-", colour=1)

        # ゲームの表示
        screen.print_at("A", *GameModel.screen_reverser(screen.height, game.gamestate["player"]["position"]))
        for enemy in game.gamestate["enemies"]:
            screen.print_at("M", *GameModel.screen_reverser(screen.height, enemy.position))
        for bullet in game.gamestate["bullets"]:
            screen.print_at("|", *GameModel.screen_reverser(screen.height, bullet))

        # 敵破壊メッセージの表示
        for _, message, position in destoroy_enemy_messages:
            screen.print_at(message, position[0], position[1])

        # ゲーム情報関係の表示
        screen.print_at(f"Score: {sum(game.gamestate['scores'])}", 2, screen.height - 2)
        screen.print_at(f"Max Score: {max_score}", 2, screen.height - 3)
        screen.print_at(f"Enemies: {len(game.gamestate['enemies'])}", 20, screen.height - 2)
        screen.print_at(f"Clock Time: {clock_time * 0.01}", 20, screen.height - 3)
        screen.print_at(f"Strategy: {player_strategys[strategy].name}", 40, screen.height - 2)
        screen.print_at("Press Q to quit.", screen.width - 20, screen.height - 2)

        screen.refresh()

    game = GameModel(screen.height, screen.width)
    max_score = 0
    destoroy_enemy_messages: list[tuple[int, str, tuple[int, int]]] = []
    max_sleep_time = 50
    minimum_sleep_time = 1
    strategy = 0
    clock_time = 1
    clock = 0

    while True:
        game.initialize_game(game.gamestate["screen_size"], enemy_count=40)
        destoroy_enemy_messages.clear()
        while not game.is_game_over:
            clock += 1
            # 描画の時間までは描画とか処理をスキップ
            if clock >= clock_time:
                # 描画及び実行関数
                clock = 0

                # 敵破壊メッセージのカウントダウン
                for i in reversed(range(len(destoroy_enemy_messages))):
                    count, message, position = destoroy_enemy_messages[i]
                    if count <= 0:
                        destoroy_enemy_messages.pop(i)
                    else:
                        destoroy_enemy_messages[i] = (count - 1, message, position)

                # ストラテジーを選択
                player = player_strategys[strategy]
                # 演算
                destroyed_enemies = game.emuration_step(player.decide_action)

                # スコアの計算
                for enemy, score in destroyed_enemies:
                    destoroy_enemy_messages.append((20, f"+{score}", GameModel.screen_reverser(screen.height, enemy.position)))

                draw()

            # キーボード入力処理
            event = cast(KeyboardEvent | None, screen.get_event())
            if isinstance(event, KeyboardEvent):
                if event.key_code in (KEY_Q, KEY_LOWQ):
                    screen.close()
                    print("Game Over! Your max score:", max_score)
                    return
                elif event.key_code == Screen.KEY_UP:
                    clock_time = min(max_sleep_time, clock_time + 1)
                    draw()
                elif event.key_code == Screen.KEY_DOWN:
                    clock_time = max(minimum_sleep_time, clock_time - 1)
                    draw()
                elif event.key_code == Screen.KEY_RIGHT:
                    strategy = (strategy + 1) % len(player_strategys)
                    draw()
                elif event.key_code == Screen.KEY_LEFT:
                    strategy = (strategy - 1) % len(player_strategys)
                    draw()

            sleep(1 / 100)  # 1 clock = 10ms

        max_score = sum(game.gamestate["scores"]) if sum(game.gamestate["scores"]) > max_score else max_score

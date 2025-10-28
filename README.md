# cui-game

CUI(コンソール)上で動作するインベーダー風ゲーム(シミュレーション)。
描画には `asciimatics` を使用し、プレイヤーは自動戦略(AI)で操作されます。

- 自機: `A`
- 敵: `M`
- 弾: `|`

## デモのイメージ
ターミナル上で、敵 `M` が左右移動と降下を繰り返し、自機 `A` が最短交差予測で移動/射撃して撃破します。

---

## 必要環境
- Python 3.11+ を推奨 (開発時のバージョン: CPython 3.11)
- OS: Windows / macOS / Linux
  - Windows は PowerShell/Windows Terminal 推奨
- 依存: `asciimatics`

## セットアップ (Windows PowerShell)
1) 仮想環境を作成・有効化

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) 依存関係をインストール

```pwsh
pip install -r requirements.txt
```

## 実行

```pwsh
python run.py
```

- 実行速度は `run.py` の `Screen.wrapper(main, arguments=[0.01])` の値(秒)で調整可能です。
- 画面サイズに応じてレイアウトが変わります。小さすぎる場合はターミナルを広げてください。

---

## ゲームのルール/仕様
- 初期配置
  - 敵は 5×3 体を生成します。
  - 自機は画面下から6行目に表示されます。(座標系は下が `y=0`、上に行くほど `y` が増える想定)
- 敵の移動
  - 一定カウントごとに左右へ1マス移動し、端に達すると1マス降下してから左右方向を切り替えます。
  - 敵クラス: `InvaderEnemy` (`src/enemy.py`)
  - 主なパラメータ: `move_count=3`, `move_distance=1`, `hitpoint=10`
- 自機の行動(自動)
  - `src/player.py` の戦略 `nearest_shot` が最短交差位置を予測し、`left`/`right`/`shoot` を選択します。
  - キーボード操作は不要です(ユーザー入力は受け付けません)。
- 弾
  - 自機の真上方向へ毎ステップ1マス進みます。
  - 敵の座標に一致すると命中。`hitpoint` を 10 減らし、0 以下で撃破します(本実装では1発で撃破)。
- スコア
  - 撃破時に `base_score(100) + 10 * (命中した弾のY座標 - デッドライン)` を加算。
- ゲーム終了
  - 敵を全滅させるとクリア(終了)。
  - いずれかの敵がデッドライン `y <= 10` に到達するとゲームオーバー。

---

## 主なパラメータ(調整箇所)
- `src/game.py`
  - `GameModel.deadline = 10` … 敵がここまで降りると終了。
  - `initialize_game()` … 生成数(5×3)などの初期配置。
- `src/enemy.py`
  - `InvaderEnemy.move_count`, `move_distance`, `hitpoint`, `base_score` … 敵の挙動/耐久/得点。
- `run.py`
  - `arguments=[0.01]` … 1ステップのスリープ(速度)。

---

## フォルダ/ファイル構成
```
LICENSE
README.md
requirements.txt
run.py
src/
  enemy.py      # 敵の実装(移動ロジック/耐久/スコア)
  enum.py       # 型エイリアスとベースクラス定義
  game.py       # ゲーム進行(状態、描画、当たり判定、スコア計算)
  player.py     # プレイヤー戦略(AI)の実装とエイリアス `player`
```

---

## プレイヤー戦略を差し替える
`src/player.py` の関数シグネチャに従う関数を用意し、
末尾の `player = nearest_shot` を差し替えるだけで戦略を変更できます。

```python
# シグネチャ例
Callable[[tuple[int, int], tuple[int, int], Sequence[BaseEnemy]], Literal["left","right","shoot","none"]]
```

- 返り値は `left` / `right` / `shoot` / `none` のいずれか。
- 画面サイズ・自機座標・敵リストを基に行動を決めます。

---

## ライセンス
BSD 2-Clause License. 詳細は `LICENSE` を参照してください。

## 謝辞
- [asciimatics](https://github.com/peterbrittain/asciimatics)

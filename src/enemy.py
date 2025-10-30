from random import choice

from src.type.abstracts import BaseEnemy


class InvaderEnemy(BaseEnemy):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()
        self.move_count = 3
        self.hitpoint = 10
        self.position = (x_position, y_position)
        self.move_direction = choice(("left", "right"))
        self.move_distance = 1
        self.base_score = 100

    def _move(self, width: int) -> None:
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

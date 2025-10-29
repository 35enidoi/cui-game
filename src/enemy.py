from src.enum import BaseEnemy


class InvaderEnemy(BaseEnemy):
    move_count = 3

    def __init__(self, x_position: int, y_position: int) -> None:
        self.hitpoint = 10
        self.position = (x_position, y_position)
        self.move_direction = "down"
        self.move_distance = 1
        self.current_count = self.move_count
        self.base_score = 100
        self.moved_count = 0

    def move(self, width: int) -> None:
        self.moved_count += 1

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

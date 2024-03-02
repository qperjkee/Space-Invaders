import random
from .utils import collide
from .entities import Enemy

class Level:
    def __init__(self):
        self.level = 0
        self.wave_length = 5

    def increase_level(self):
        self.level += 1
        self.wave_length += 3

    def add_score(self, score):
        if self.level >= 2:
            score += 1000
        return score

    def create_enemies(self, enemies, WIDTH):
        for _ in range(self.wave_length):
            enemy = None
            if self.level < 2:
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), "red")
            elif self.level < 3:
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue"]))
            else:
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-2000, -100), random.choice(["red", "blue", "green"]))

            if enemy.x <= 100:
                if enemy.color == "red":
                    enemy.x += 200
                else:
                    enemy.x += 100
            elif enemy.x >= WIDTH - 100:
                if enemy.color == "red":
                    enemy.x -= 200
                else:
                    enemy.x -= 100

            for other_enemy in enemies:
                if collide(enemy, other_enemy):
                    enemy.y -= 100

            enemies.append(enemy)

        return enemies
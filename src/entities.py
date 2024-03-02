import pygame
from .constants import HEIGHT, YELLOW_LASER, YELLOW_SPACE_SHIP, RED_LASER, GREEN_LASER, RED_SPACE_SHIP, BLUE_LASER, GREEN_SPACE_SHIP, BLUE_SPACE_SHIP, WIN
from .laser import Laser

class Ship:
    COOLDOWN = 20
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.max_health = 100

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN :
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if obj.color == "blue":
                            obj.health -= 50
                            if obj.health <= 0:
                                objs.remove(obj)
                        else:
                            objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    

    def draw(self, window):
        self.healthbar(window)
        super().draw(window)
        

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+15, self.y+10, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def add_hp(self):
        self.health += 20
        while self.health > self.max_health:
            self.health -= 10

    def healthbar(self, window):
        main_font = pygame.font.SysFont("comicsans", 20)
        hp_label = main_font.render(f"HP: ", 1, (255,255,255))
        WIN.blit(hp_label, (10, HEIGHT-35))
        pygame.draw.rect(window, (255,0,0), (45, HEIGHT-24, 80, 10))
        pygame.draw.rect(window, (0,255,0), (45, HEIGHT-24, 80 * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.color = color
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            if self.ship_img == RED_SPACE_SHIP:
                laser = Laser(self.x+50, self.y+45, self.laser_img)
            else:
                laser = Laser(self.x-15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def draw_health(self, window):
        if self.color == "blue":
            pygame.draw.rect(window, (255,0,0), (self.x + 13, self.y, self.ship_img.get_width() - 22, 5))
            pygame.draw.rect(window, (0,255,0), (self.x + 13, self.y, (self.ship_img.get_width() - 22) * (self.health/self.max_health), 5))

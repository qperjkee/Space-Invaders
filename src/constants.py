import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Ships
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red_inv.png")), (195, 140))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_inv.png")), (70, 50))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue_inv.png")), (70, 50))
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "invader.png")), (130, 90))

# Sound and Pause
SOUND_OFF_ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sound_off.png")), (100, 100))
SOUND_ON_ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sound_on.png")), (100, 100))
PAUSE_ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pause2.png")), (200, 200))

# Extra img
ALIEN = pygame.image.load(os.path.join("assets", "alien.png"))
SCENE = pygame.image.load(os.path.join("assets", "scene.png"))
ROCKET = pygame.image.load(os.path.join("assets", "rocket.png"))
AWARD = pygame.transform.scale(pygame.image.load(os.path.join("assets", "award.png")), (50, 40))
PLANET = pygame.image.load(os.path.join("assets", "planet.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# sounds
game_music = pygame.mixer.Sound("sfx/game_sound.mp3")

import pygame, sys, random, json
from .constants import WIDTH, HEIGHT, SOUND_ON_ICON, SOUND_OFF_ICON, RED_SPACE_SHIP, BLUE_SPACE_SHIP, GREEN_SPACE_SHIP, ALIEN, SCENE, BG, AWARD, ROCKET, PLANET, WIN, game_music, PAUSE_ICON
from .button import Button
from .utils import collide
from .entities import Player, Enemy
from .level import Level
from .laser import Laser

class Menu:
    def __init__(self):
        pygame.mixer.init()
        self.game_music = pygame.mixer.Sound("sfx/game_sound.mp3")
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.info_font = pygame.font.Font('font/my_font.ttf', 30)
        self.end_font = pygame.font.Font('font/my_font.ttf', 110)
        self.top_font = pygame.font.Font('font/my_font.ttf', 65)
        self.result_font = pygame.font.Font('font/my_font.ttf', 75)
        self.end_font2 = pygame.font.Font('font/my_font.ttf', 110)
        self.info_font2 = pygame.font.SysFont('comicsans', 20)
        self.result_font2 = pygame.font.Font('font/my_font.ttf', 45)
        self.bg_y = 0

    def update_scores(self, score):
        with open('scores.txt', 'a') as file:
            file.write(str(score) + '\n')
        with open('scores.txt', 'r') as file:
            scores = [int(line.strip()) for line in file]
        scores.sort(reverse=True)
        with open('scores.txt', 'w') as file:
            for score in scores:
                file.write(str(score) + '\n')

    def read_top_scores(self):
        with open('scores.txt', 'r') as file:
            top_scores = []
            for _ in range(5):
                line = file.readline().strip()
                if line:
                    top_scores.append(int(line))
        return top_scores

    def find_score_row(self, score):
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if int(line.strip()) == score:
                    return i + 1

    def get_font(self, size): 
        return pygame.font.Font("font/font.ttf", size)

    def main_menu(self):
        pygame.mixer.Channel(0).set_volume(0.1)
        pygame.mixer.Channel(0).play(self.game_music)
        self.end_font = pygame.font.Font('font/my_font.ttf', 110)
        self.result_font2 = pygame.font.Font('font/my_font.ttf', 45)
        sound_icon_rect = SOUND_ON_ICON.get_rect()
        sound_icon_rect.topleft = (WIDTH - 100, HEIGHT - 100)
        sound_icon = SOUND_ON_ICON
        load_label = self.end_font.render("Load prev game", 1, (118,12,139))
        load_rect = load_label.get_rect(center = (WIDTH/2, 600))
        run = True
        while run:
            self.move_bg()
            PLAY_BUTTON = Button(pos=(600, 300), text_input="PLAY", font=self.get_font(75), base_color="White", hovering_color="Green")
            INFO_BUTTON = Button(pos=(WIDTH-150, 700), text_input="INFO", font=self.get_font(25), base_color="White", hovering_color="Green")
            for button in [PLAY_BUTTON, INFO_BUTTON]:
                button.changeColor(pygame.mouse.get_pos())
                button.update(self.WIN)
            self.WIN.blit(sound_icon, (WIDTH - 100, HEIGHT - 100))
            title_label = self.end_font.render("Space Invaders", 1, (118,12,139))
            result_label = self.result_font2.render("Top 5 Results: ", 1, (0,255,0))
            self.WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 10))
            self.WIN.blit(result_label, (10, HEIGHT-280))
            self.WIN.blit(load_label, load_rect)
            font = pygame.font.Font('font/my_font.ttf', 40)
            top_scores = self.read_top_scores()
            for i, score in enumerate(top_scores):
                text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
                self.WIN.blit(text, (20, 520 + i*40))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        pygame.mixer.Channel(0).stop()
                        game = Game()
                        game.run_game()
                    if load_rect.collidepoint(event.pos):
                        pygame.mixer.Channel(0).stop()
                        with open('game_phase.txt') as f:
                            data = json.load(f)
                        game = Game(data, True)
                        game.run_game()
                    if sound_icon_rect.collidepoint(event.pos):
                        if sound_icon == SOUND_ON_ICON:
                            sound_icon = SOUND_OFF_ICON
                            pygame.mixer.Channel(0).stop()
                        else:
                            sound_icon = SOUND_ON_ICON
                            pygame.mixer.Channel(0).play(self.game_music)
                    elif INFO_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.info_menu()
        pygame.quit()

    def info_menu(self):
        self.end_font2 = pygame.font.Font('font/my_font.ttf', 110)
        self.info_font2 = pygame.font.SysFont('comicsans', 20)
        run = True
        while run:
            self.move_bg()
            self.WIN.blit(RED_SPACE_SHIP, (-50, 100))
            self.WIN.blit(BLUE_SPACE_SHIP, (10, 200))
            self.WIN.blit(GREEN_SPACE_SHIP, (10, 255))
            self.WIN.blit(ALIEN, (800, HEIGHT-200))
            self.WIN.blit(SCENE, (950, 0))
            title_label = self.end_font2.render("About the game", 1, (255,255,255))
            info_label1 = self.info_font2.render("- HP: 1 hit to destroy, SPAWN: from 1 level, HIT PROBABILITY - 1 TO 4", 1, (255,0,0))
            info_label2 = self.info_font2.render("- HP: 2 hits to destroy, SPAWN: from 2 level, HIT PROBABILITY - 1 TO 3", 1, (0,0,255))
            info_label3 = self.info_font2.render("- HP: 1 hit to destroy, SPAWN: from 3 level, HIT PROBABILITY - 1 TO 2", 1, (0,255,0))
            score_label = self.info_font2.render("• Score - player erans 15 points to score each second and 1000 each lvl complete", 1, (255,255,255))
            lives_label = self.info_font2.render("• Lives - player lose one of 5 lives each time enemy gets to your base(bottom screen)", 1, (255,255,255))
            hp_label = self.info_font2.render("• HP - player has 100 hp total and loses 10 each time when players ship gets hit", 1, (255,255,255))
            game_label = self.info_font2.render("=> Defend your base from different waves of space invaders by shooting them(SPACE button) <= ", 1, (255,255,255))
            game2_label = self.info_font2.render("Avoid their lasers(w/a/s/d) unless your ship will be destroyed. Good luck!:) P.S ESC - Pause", 1, (255,255,255))
            leave_label = self.info_font2.render("Press ESC to return to main menu :)", 1, (128,128,128))
            self.WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 10))
            self.WIN.blit(leave_label, (WIDTH/2 - leave_label.get_width()/2 - 50, 710))
            self.WIN.blit(info_label1, (100, 160))
            self.WIN.blit(info_label2, (100, 210))
            self.WIN.blit(info_label3, (100, 265))
            self.WIN.blit(score_label, (10, 320))
            self.WIN.blit(lives_label, (10, 360))
            self.WIN.blit(hp_label, (10, 400))
            self.WIN.blit(game_label, (10, 460))
            self.WIN.blit(game2_label, (30, 500))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_music.stop()
                        self.main_menu()
        pygame.quit()

    def end_menu(self, score):
        player_score = score
        self.end_font = pygame.font.Font('font/my_font.ttf', 110)
        self.result_font = pygame.font.Font('font/my_font.ttf', 75)
        self.top_font = pygame.font.Font('font/my_font.ttf', 65)
        self.info_font = pygame.font.Font('font/my_font.ttf', 30)
        top_scores = self.read_top_scores()
        rank = self.find_score_row(score)
        run = True
        while run:
            self.WIN.blit((BG), (0,0))
            info_label = self.info_font.render("Press ENTER to play", 1, (128,128,128))
            info2_label = self.info_font.render("Press ESC to leave the game", 1, (128,128,128))
            title_label = self.end_font.render("Game Over", 1, (255,0,0))
            rank_label = self.top_font.render(f"Your rank: {rank}", 1, (0,255,0))
            result_label = self.result_font.render(f"Your Score: {player_score}", 1, (255,255,255))
            top_label = self.top_font.render(f"Top 5 scores: ", 1, (255,255,255))
            self.WIN.blit(info2_label, (WIDTH/2 - info_label.get_width()/2 - 50, 710))
            self.WIN.blit(info_label, (WIDTH/2 - info_label.get_width()/2, 680))
            self.WIN.blit(rank_label, (WIDTH/2 - rank_label.get_width()/2, 580))
            self.WIN.blit(top_label, (WIDTH/2 - top_label.get_width()/2, 240))
            self.WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 10))
            self.WIN.blit(result_label, (WIDTH/2 - result_label.get_width()/2, 170))
            self.WIN.blit(AWARD, (480,325))
            self.WIN.blit(PLANET, (50,130))
            self.WIN.blit(ROCKET, (WIDTH-300,HEIGHT-300))
            font = pygame.font.Font('font/my_font.ttf', 50)
            for i, score in enumerate(top_scores):
                text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
                self.WIN.blit(text, (WIDTH/2 - text.get_width()/2, 320 + i*50))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN: 
                        game = Game()
                        game.run_game()

    def move_bg(self):
        self.bg_y
        WIN.blit(BG, (0, self.bg_y))
        WIN.blit(BG, (0, self.bg_y - HEIGHT)) 

        self.bg_y += 0.25

        if self.bg_y >= HEIGHT:
            self.bg_y = 0

class Game:
    def __init__(self, data = {}, load = False):
        pygame.init()
        self.WIDTH = 1200
        self.HEIGHT = 750
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.run = True
        self.lives = 5
        self.score = 0
        self.bg_y = 0
        self.lost = False
        self.lost_count = 0
        self.data = data
        self.load = load

        self.main_font = pygame.font.SysFont("comicsans", 50)

        self.enemies = []
        self.enemy_vel = 0.75

        self.player_vel = 5
        self.laser_vel = 5

        self.player = Player(self.WIDTH / 2, 630)
        self.level = Level()

        self.init_game()
        self.menu = Menu()

        if self.load:
            self.load_game()
            self.redraw_window()
            self.pause_game()
    
    def load_game(self):
        self.level.level = self.data.get('level')
        self.lives = self.data.get('lives')
        self.score = self.data.get('score')
        self.player.x = self.data.get('player.x')
        self.player.y = self.data.get('player.y')
        self.player.health = self.data.get('player.health')

        for laser_pos in self.data.get('player.lasers', []):
            x, y = laser_pos
            laser = Laser(x, y, self.player.laser_img)
            self.player.lasers.append(laser)
        
        for enemy_data in self.data.get('enemies', []):
            enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['color'])
            enemy.health = enemy_data['health']
            enemy.lasers = [Laser(x, y, enemy.laser_img) for x, y in enemy_data['lasers']]
            self.enemies.append(enemy)

    def init_game(self):
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game")

    def pause_game(self):
        paused = True
        self.end_font = pygame.font.Font('font/my_font.ttf', 60)
        save_label = self.end_font.render("Save game", 1, (118,12,139))
        save_rect = save_label.get_rect(center = (WIDTH/2, 30))

        enemies_data = []
        for enemy in self.enemies:
            enemy_data = {
                'x': enemy.x,
                'y': enemy.y,
                'color': enemy.color,
                'health': enemy.health,
                'lasers': [(laser.x, laser.y) for laser in enemy.lasers]
            }
            enemies_data.append(enemy_data)

        self.data = {
            'level': self.level.level,
            'score': self.score,
            'lives': self.lives,
            'player.x': self.player.x,
            'player.y': self.player.y,
            'player.health': self.player.health,
            'player.lasers': [(laser.x, laser.y) for laser in self.player.lasers],
            'enemies': enemies_data
        }
        
        while paused:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if save_rect.collidepoint(event.pos):
                        with open('game_phase.txt', 'w') as f:
                            json.dump(self.data, f)
                        menu = Menu()
                        menu.main_menu()
            self.WIN.blit(save_label, save_rect)
            self.WIN.blit(PAUSE_ICON, (self.WIDTH / 2 - 100, self.HEIGHT / 2 - 100))
            pygame.display.update()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def redraw_window(self):
        self.WIN.blit(BG, (0, self.bg_y))
        self.WIN.blit(BG, (0, self.bg_y - self.HEIGHT))

        self.bg_y += 0.25

        if self.bg_y >= self.HEIGHT:
            self.bg_y = 0

        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level: {self.level.level}", 1, (255, 255, 255))

        self.WIN.blit(lives_label, (10, 10))
        self.WIN.blit(level_label, (self.WIDTH - level_label.get_width() - 10, 10))

        for enemy in self.enemies:
            enemy.draw(self.WIN)
            enemy.draw_health(self.WIN)

        self.player.draw(self.WIN)

        if self.lost:
            self.menu.update_scores(round(self.score))
            self.menu.end_menu(round(self.score))
        pygame.display.update()

    def run_game(self):
        while self.run:
            self.score += 0.25
            self.clock.tick(self.FPS)
            self.redraw_window()

            if self.lives <= 0 or self.player.health <= 0:
                self.lost = True
                self.run = False
                self.redraw_window()

            if len(self.enemies) == 0:
                self.level.increase_level()
                self.player.add_hp()
                self.score = self.level.add_score(self.score)
                self.enemies = self.level.create_enemies(self.enemies, self.WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.player.x > -30:  # left
                self.player.x -= self.player_vel
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.player.x + self.player_vel + self.player.get_width() < self.WIDTH + 30:  # right
                self.player.x += self.player_vel
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.player.y - self.player_vel > 0:  # up
                self.player.y -= self.player_vel
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.player.y + self.player_vel + self.player.get_height() + 15 < self.HEIGHT + 15:  # down
                self.player.y += self.player_vel
            if keys[pygame.K_SPACE]:
                self.player.shoot()

            for enemy in self.enemies[:]:
                enemy.move(self.enemy_vel)
                enemy.move_lasers(self.laser_vel, self.player)

                if enemy.color == "red":
                    if random.randrange(0, 3 * 60) == 1:
                        enemy.shoot()

                elif enemy.color == "blue":
                    if random.randrange(0, 2 * 60) == 1:
                        enemy.shoot()
                else:
                    if random.randrange(0, 1 * 60) == 1:
                        enemy.shoot()

                if collide(enemy, self.player):
                    self.player.health -= 10
                    self.enemies.remove(enemy)

                elif enemy.y + enemy.get_height() > self.HEIGHT + 30:
                    self.lives -= 1
                    self.enemies.remove(enemy)

            self.player.move_lasers(-self.laser_vel, self.enemies)
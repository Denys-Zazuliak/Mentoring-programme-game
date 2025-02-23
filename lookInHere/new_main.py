# IMPORTS
import pygame as py
import random
import math


# CONSTANTS
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 30
# assets
PLAYER_IMG = "player.png"
ENEMY_IMG = "enemy.png"
PROJECTILE_IMG = "projectile.png"
STRONGER_ENEMY_IMG = "stronger_enemy.png"
STRONGEST_ENEMY_IMG = "strongest_enemy.png"
IMAGE_SIZE = 64
# OceanBackground colours
TOP_COLOUR = (173, 216, 230)
BOTTOM_COLOUR = (0, 0, 128)
WAVE_COLOUR = (255, 255, 255, 90)
BEAM_COLOUR = (255, 255, 224, 40)
CORAL_COLOUR = (139, 69, 19)
BUBBLE_COLOUR = (224, 255, 255)
# difficulty
STRONGER_ENEMY_SPAWN_TIME = 10
ENEMY_SPAWN_TIME = 2
STRONGEST_ENEMY_SPAWN_TIME = 30
AMMO_REGEN_TIME = 1
INVULNERABILITY_TIME = 3
PLAYER_V = 5
PLAYER_HEALTH = 5
PLAYER_AMMO = 2
ENEMY_HEALTH = 2
ENEMY_V = 3
STRONGER_ENEMY_HEALTH = 5
STRONG_ENEMY_V = 4
STRONGEST_ENEMY_HEALTH = 10


# CLASSES
class Game:
    def __init__(self):
        # general setup
        py.init()
        self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.font = py.font.SysFont("Arial", 20)
        self.running = True
        self.high_score = 0
        self.background = OceanBackground(SCREEN_WIDTH, SCREEN_HEIGHT)
        # repeatable setup
        self.player = Player()
        self.sprites = []
        self.enemies = []
        self.projectiles = []
        self.sprites.append(self.player)
        self.count = 1
        self.score = 0

    def start_screen(self):
        # create text
        text = self.font.render("press enter to start", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # display text
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        py.display.flip()

        # loop for quiting game
        while self.running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.running = False
                    if event.key == py.K_RETURN:
                        self.main_screen()
        py.quit()

    def end_screen(self):
        self.running = True

        # scoring
        if self.score > self.high_score:
            self.high_score = self.score

        # creating text
        text1 = self.font.render("GAME OVER", True, (255, 255, 255))
        text1_rect = text1.get_rect()
        text1_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)

        text2 = self.font.render("press enter to restart", True, (255, 255, 255))
        text2_rect = text2.get_rect()
        text2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)

        text3 = self.font.render(f"score: {self.score}", True, (255, 255, 255))
        text3_rect = text3.get_rect()
        text3_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        text4 = self.font.render(f"high score: {self.high_score}", True, (255, 255, 255))
        text4_rect = text4.get_rect()
        text4_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

        # displaying text
        self.screen.fill((0, 0, 0))

        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        self.screen.blit(text3, text3_rect)
        self.screen.blit(text4, text4_rect)

        py.display.flip()

        # loop for either replaying or quiting game
        while self.running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.running = False
                    if event.key == py.K_RETURN:
                        for sprite in self.sprites:
                            del sprite
                        # repeatable setup
                        self.player = Player()
                        self.sprites = []
                        self.enemies = []
                        self.projectiles = []
                        self.sprites.append(self.player)
                        self.count = 1
                        self.score = 0
                        # replay
                        self.main_screen()
        py.quit()

    def main_screen(self):
        # game loop
        while self.running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                    if event.key == py.K_SPACE:
                        if self.player.get_ammo() > 0:
                            projectile = Projectile(self.player)
                            self.projectiles.append(projectile)
                            self.sprites.append(projectile)
                            self.player.minus_ammo()

            keys = py.key.get_pressed()

            # creating text
            text1 = self.font.render(f"health: {self.player.get_health()}", True, (255, 255, 255))
            text1_rect = text1.get_rect()
            text1_rect.center = (SCREEN_WIDTH // 2, 20)

            text2 = self.font.render(f"score: {self.score}", True, (255, 255, 255))
            text2_rect = text2.get_rect()
            text2_rect.center = (SCREEN_WIDTH // 2, 40)

            text3 = self.font.render(f"ammo: {self.player.get_ammo()}", True, (255, 255, 255))
            text3_rect = text3.get_rect()
            text3_rect.center = (SCREEN_WIDTH // 2, 60)

            # updating projectiles
            for i in range(len(self.projectiles) - 1, 0, -1):
                self.projectiles[i].move()
                # deleting extra projectile objects
                if self.projectiles[i].wall_collide():
                    self.sprites.remove(self.projectiles[i])
                    del self.projectiles[i]
                elif self.projectiles[i].enemy_collide(self.enemies):
                    self.sprites.remove(self.projectiles[i])
                    del self.projectiles[i]

            # spawning enemies
            if self.count % (STRONGEST_ENEMY_SPAWN_TIME * FPS) == 0:
                enemy1 = StrongestEnemy()
                enemy2 = StrongerEnemy()
                enemy3 = StrongerEnemy()
                self.enemies.append(enemy1)
                self.sprites.append(enemy1)
                self.enemies.append(enemy2)
                self.sprites.append(enemy2)
                self.enemies.append(enemy3)
                self.sprites.append(enemy3)
            elif self.count % (STRONGER_ENEMY_SPAWN_TIME * FPS) == 0:
                enemy = StrongerEnemy()
                self.enemies.append(enemy)
                self.sprites.append(enemy)
            elif self.count % (ENEMY_SPAWN_TIME * FPS) == 0:
                enemy = Enemy()
                self.enemies.append(enemy)
                self.sprites.append(enemy)

            # updating enemies
            for i in range(len(self.enemies) - 1, 0, -1):
                self.enemies[i].move_towards_player(self.player.get_pos())
                # deleting dead enemy objects
                if self.enemies[i].get_health() <= 0:
                    self.sprites.remove(self.enemies[i])
                    del self.enemies[i]

            # updating player
            self.player.move(keys)
            self.player.wall_collide()
            self.player.is_invulnerable()
            self.player.enemy_collide(self.enemies)
            if self.player.get_health() <= 0:
                self.running = False
            if self.count % (AMMO_REGEN_TIME * FPS) == 0:
                self.player.add_ammo()

            # drawing ocean background
            self.background.draw(self.screen)

            # drawing text
            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)
            self.screen.blit(text3, text3_rect)

            # displaying sprites
            for sprite in self.sprites:
                self.screen.blit(sprite.img, sprite.rect)

            # updating display and game
            py.display.flip()
            self.clock.tick(FPS)
            self.count += 1
            if self.count % FPS == 0:
                self.score += 1
        self.end_screen()

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = py.image.load(PLAYER_IMG).convert_alpha()
        self.rect = py.Rect(SCREEN_WIDTH // 2 - IMAGE_SIZE // 2, SCREEN_HEIGHT // 2 - IMAGE_SIZE // 2, IMAGE_SIZE, IMAGE_SIZE)
        self.v = PLAYER_V
        self.health = PLAYER_HEALTH
        self.invulnerable = False
        self.invulnerable_count = 0
        self.ammo = PLAYER_AMMO

    def move(self, keys):
        if keys[py.K_UP]:
            self.rect.move_ip(0, -self.v)
        if keys[py.K_DOWN]:
            self.rect.move_ip(0, self.v)
        if keys[py.K_LEFT]:
            self.rect.move_ip(-self.v, 0)
        if keys[py.K_RIGHT]:
            self.rect.move_ip(self.v, 0)

    def wall_collide(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def enemy_collide(self, enemies):
        count = 0
        while (not self.invulnerable) and (count < len(enemies)):
            if self.rect.colliderect(enemies[count]):
                self.health -= 1
                self.invulnerable = True
            count += 1

    def get_health(self):
        return self.health

    def get_pos(self):
        return [self.rect.centerx, self.rect.centery]

    def is_invulnerable(self):
        self.invulnerable_count += 1
        if self.invulnerable_count >= (INVULNERABILITY_TIME * FPS):
            self.invulnerable = False
            self.invulnerable_count = 0

    def add_ammo(self):
        self.ammo += 1

    def get_ammo(self):
        return self.ammo

    def minus_ammo(self):
        self.ammo -= 1

class Projectile(py.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.img = py.image.load(PROJECTILE_IMG).convert_alpha()
        self.rect = py.Rect(player.rect.right, player.rect.centery - 4, 8, 8)
        self.v = 7

    def move(self):
        self.rect.move_ip(self.v, 0)

    def wall_collide(self):
        if self.rect.left < 0:
            del self
            return 1
        if self.rect.right > SCREEN_WIDTH:
            del self
            return 1
        if self.rect.top <= 0:
            del self
            return 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            del self
            return 1
        return 0

    def enemy_collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                enemy.set_health(enemy.get_health() - 1)
                del self
                return 1
        return 0

class Enemy(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = py.image.load(ENEMY_IMG).convert_alpha()
        self.rect = py.Rect(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 50), IMAGE_SIZE, IMAGE_SIZE)
        self.v = ENEMY_V
        self.health = ENEMY_HEALTH

    def move_towards_player(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        dx, dy = dx / distance, dy / distance
        self.rect.move_ip(dx * self.v, dy * self.v)

    def set_health(self, health):
        self.health = health

    def get_health(self):
        return self.health

class StrongerEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = STRONGER_ENEMY_HEALTH
        self.v = STRONG_ENEMY_V
        self.img = py.image.load(STRONGER_ENEMY_IMG).convert_alpha()

class StrongestEnemy(StrongerEnemy):
    def __init__(self):
        super().__init__()
        self.health = STRONGEST_ENEMY_HEALTH
        self.img = py.image.load(STRONGEST_ENEMY_IMG).convert_alpha()

class OceanBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gradient_surface = create_gradient_surface(width, height, TOP_COLOUR, BOTTOM_COLOUR)
        self.wave_phase = 0
        self.wave_speed = 0.05
        self.wave_amplitude = 10
        self.wave_frequency = 0.02
        self.bubbles = self.create_bubbles(15)

    def create_bubbles(self, count):
        bubbles = []
        for _ in range(count):
            bubble = {
                'x': random.randint(50, self.width - 50),
                'y': random.randint(self.height - 100, self.height - 10),
                'radius': random.randint(3, 8),
                'speed': random.uniform(0.5, 1.5)
            }
            bubbles.append(bubble)
        return bubbles

    def update_bubbles(self):
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] + bubble['radius'] < 0:
                bubble['x'] = random.randint(50, self.width - 50)
                bubble['y'] = self.height + random.randint(5, 50)
                bubble['radius'] = random.randint(3, 8)
                bubble['speed'] = random.uniform(0.5, 1.5)

    def draw(self, screen):
        screen.blit(self.gradient_surface, (0, 0))
        self.draw_light_beams(screen)
        self.draw_waves(screen)
        self.update_bubbles()
        self.draw_bubbles(screen)

    def draw_waves(self, screen):
        points = []
        for x in range(0, self.width, 5):
            y = int(50 + self.wave_amplitude * math.sin(self.wave_frequency * x + self.wave_phase))
            points.append((x, y))
        self.wave_phase += self.wave_speed
        wave_surface = py.Surface((self.width, 60), py.SRCALPHA)
        if len(points) > 1:
            py.draw.aalines(wave_surface, WAVE_COLOUR, False, points)
        screen.blit(wave_surface, (0, 0))

    def draw_light_beams(self, screen):
        beam_surface = py.Surface((self.width, self.height), py.SRCALPHA)
        beam_positions = [self.width * 0.2, self.width * 0.5, self.width * 0.8]
        for pos in beam_positions:
            beam_width = 100
            points = [
                (pos - beam_width * 0.5, 0),
                (pos + beam_width * 0.5, 0),
                (pos + beam_width * 1.5, self.height),
                (pos - beam_width * 1.5, self.height)
            ]
            py.draw.polygon(beam_surface, BEAM_COLOUR, points)
        screen.blit(beam_surface, (0, 0))

    def draw_bubbles(self, screen):
        for bubble in self.bubbles:
            py.draw.circle(screen, BUBBLE_COLOUR, (int(bubble['x']), int(bubble['y'])), bubble['radius'], 2)


# SUBPROGRAMS
# for OceanBackground
def create_gradient_surface(width, height, top_colour, bottom_colour):
    gradient = py.Surface((width, height))
    for y in range(height):
        factor = y / height
        red = int(top_colour[0] + factor * (bottom_colour[0] - top_colour[0]))
        green = int(top_colour[1] + factor * (bottom_colour[1] - top_colour[1]))
        blue = int(top_colour[2] + factor * (bottom_colour[2] - top_colour[2]))
        py.draw.line(gradient, (red, green, blue), (0, y), (width, y))
    return gradient


# MAIN
if __name__ == '__main__':
    game = Game()
    game.start_screen()


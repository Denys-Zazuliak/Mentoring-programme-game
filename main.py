# imports
import pygame
import math

# some constants
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# change to whatever 50x50 pixelart png you want with a transparent background
player_img = "fish.png"
enemy_img = "shark.png"
attack_img= "bubble.png"

# classes for the player and enemies and stuff will go here
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # loads image
        self.img = pygame.image.load(player_img).convert_alpha()
        # can change to smth other than 50x50 pixels if you want
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.health = 5
        self.invulnerable = False
        self.invuln_timer = 0

        # it moves
    def move(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -v)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, v)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-v, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(v, 0)

    # stops player wandering into the endless abyss off screen
    def wall_collide(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def enemy_collision(self, enemies):
        if self.invulnerable:
            self.invuln_timer -= 1
            if self.invuln_timer <= 0:
                self.invulnerable = False
        else:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.health -= 1
                    self.invulnerable = True
                    self.invuln_timer = FPS  # 1 second of invulnerability
                    break


# Enemy class that chases the player
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load(enemy_img).convert_alpha()
        self.rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 50, 50)  # Start at the bottom-right corner
        self.speed = 3  # Speed of the enemy

    def move_towards_player(self, player_position):
        # Calculate the direction vector to the player
        dx = player_position[0] - self.rect.centerx
        dy = player_position[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            return  # Guard against division by zero


        dx, dy = dx / distance, dy / distance
        self.rect.move_ip(dx * self.speed, dy * self.speed)

#maybe we should add a "tough enemy" class that will be identical to the enemy but just with more hp
# class ToughtEnemy(pygame.sprite.Sprite):
# pass


class Projectile(pygame.sprite.Sprite):
    def __init__(self, shooter):
        super().__init__()
        self.img = pygame.image.load(attack_img).convert_alpha()
        self.rect = pygame.Rect(shooter.rect.right, shooter.rect.centery, 10, 10)
        self.speed = 7

    def move(self):
        self.rect.move_ip(self.speed, 0)

    def wall_collision(self):
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > SCREEN_WIDTH:
            self.kill()
        if self.rect.top <= 0:
            self.kill()
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()

    def enemy_collision(self, enemy):
        if (self.rect.right >= enemy.rect.left and self.rect.left <= enemy.rect.right and self.rect.bottom >= enemy.rect.top and self.rect.top <= enemy.rect.bottom):
            self.kill()
            enemy.kill()


# quite important for pygame to work
pygame.init()

# screen stuff
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
shooting=False

# player velocity
v = 5

# instantiating player object
player = Player()

font=pygame.font.SysFont("Arial", 20)

bubble = Projectile(player)
enemies=[]
bubbles=[]

# creates a group of all sprites making it easier later to update them all
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# makes framerate constant across different machines
clock = pygame.time.Clock()
FPS = 30
count=0

# game loop
running = True
while running:

    # checks if the user wants to quit
    # idk why they would ever want to leave this masterpiece tho
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            if event.key == pygame.K_z:
                bubble = Projectile(player)
                bubbles.append(bubble)
                all_sprites.add(bubble)

    text = font.render(f'Health: {player.health}', True, (255, 255, 255), 0)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, 20)

    # gets dict of all keys pressed for moving player
    pressed_keys = pygame.key.get_pressed()

    # updating player stuff
    player.move(pressed_keys)
    player.wall_collide()

    if count%FPS==0:
        enemy=Enemy()
        all_sprites.add(enemy)
        enemies.append(enemy)

    for enemy in enemies:
        enemy.move_towards_player(player.rect.center)

    #there's this weird bug that makes the bubbles disappear but they still kill the sharks for some reason
    #also damage is taken even after the enemies are killed
    #i dont have a single idea on how to fix it
    for bubble in bubbles:
        bubble.move()
        bubble.wall_collision()
        for enemy in enemies:
            if bubble.enemy_collision(enemy):
                bubbles.remove(bubble)
                enemies.remove(enemy)
                bubble.kill()
                enemy.kill()
                break

    player.enemy_collision(enemies)

    screen.fill((0, 0, 0))
    screen.blit(text, textRect)

    # draw sprites to screen surface
    for entity in all_sprites:
        screen.blit(entity.img, entity.rect)

    # updates everything
    pygame.display.flip()
    # wait a bit
    clock.tick(FPS)
    count+=1

    if player.health <= 0:
        running = False

# goodbye
pygame.quit()

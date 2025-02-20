# imports
import pygame
import math
import random

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

def create_gradient_surface(width, height, top_colour, bottom_colour):
    """
    Create a surface with a vertical gradient from top_colour to bottom_colour.
    """
    gradient = pygame.Surface((width, height))
    for y in range(height):
        # Compute interpolation factor (0 at top; 1 at bottom)
        factor = y / height
        # Linearly interpolate each colour channel
        red = int(top_colour[0] + factor * (bottom_colour[0] - top_colour[0]))
        green = int(top_colour[1] + factor * (bottom_colour[1] - top_colour[1]))
        blue = int(top_colour[2] + factor * (bottom_colour[2] - top_colour[2]))
        pygame.draw.line(gradient, (red, green, blue), (0, y), (width, y))
    return gradient

class OceanBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create a precomputed gradient surface
        self.gradient_surface = create_gradient_surface(width, height, TOP_COLOUR, BOTTOM_COLOUR)

        # Variables for animated waves
        self.wave_phase = 0
        self.wave_speed = 0.05
        self.wave_amplitude = 10
        self.wave_frequency = 0.02

        # Create bubbles
        self.bubbles = self.create_bubbles(15)  # Number of bubbles to draw

    def create_bubbles(self, count):
        """
        Initialize a list of bubbles with random positions near the bottom.
        Each bubble is a dictionary containing x, y positions and a radius.
        """
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
        """
        Update bubble positions to simulate a rising effect.
        When a bubble moves off the top, reposition it near the bottom.
        """
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] + bubble['radius'] < 0:
                bubble['x'] = random.randint(50, self.width - 50)
                bubble['y'] = self.height + random.randint(5, 50)
                bubble['radius'] = random.randint(3, 8)
                bubble['speed'] = random.uniform(0.5, 1.5)

    def draw(self, screen):
        # Draw the static ocean gradient
        screen.blit(self.gradient_surface, (0, 0))

        # Draw animated light beams (soft beams are drawn first)
        self.draw_light_beams(screen)

        # Draw animated waves near the surface
        self.draw_waves(screen)

        # Draw faint silhouettes of marine details (e.g., coral)
        self.draw_coral(screen)

        # Update and draw bubbles
        self.update_bubbles()
        self.draw_bubbles(screen)

    def draw_waves(self, screen):
        """
        Draw animated sinusoidal waves across the top of the screen.
        """
        points = []
        # Compute wave points across the width of the screen
        for x in range(0, self.width, 5):
            y = int(50 + self.wave_amplitude * math.sin(self.wave_frequency * x + self.wave_phase))
            points.append((x, y))
        # Advance the phase for the next frame
        self.wave_phase += self.wave_speed

        # Create a transparent surface to draw waves
        wave_surface = pygame.Surface((self.width, 60), pygame.SRCALPHA)
        if len(points) > 1:
            # Draw the wave line
            pygame.draw.aalines(wave_surface, WAVE_COLOUR, False, points)
        # Blit the wave surface onto the screen (positioned near the top)
        screen.blit(wave_surface, (0, 0))

    def draw_light_beams(self, screen):
        """
        Draw soft beams of light filtering down from the surface.
        The beams are drawn using semi-transparent polygons.
        """
        # Create a surface with per-pixel alpha to handle transparency
        beam_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Define a few beam positions at the top for variety
        beam_positions = [self.width * 0.2, self.width * 0.5, self.width * 0.8]
        for pos in beam_positions:
            # Define a polygon that simulates a light beam
            beam_width = 100
            points = [
                (pos - beam_width * 0.5, 0),
                (pos + beam_width * 0.5, 0),
                (pos + beam_width * 1.5, self.height),
                (pos - beam_width * 1.5, self.height)
            ]
            pygame.draw.polygon(beam_surface, BEAM_COLOUR, points)
        # Overlay the beam surface onto the screen
        screen.blit(beam_surface, (0, 0))

    def draw_bubbles(self, screen):
        """
        Draw rising bubbles as circles on the screen.
        """
        for bubble in self.bubbles:
            pygame.draw.circle(screen, BUBBLE_COLOUR, (int(bubble['x']), int(bubble['y'])), bubble['radius'], 1)

    def draw_coral(self, screen):
        """
        Draw faint silhouettes of coral or distant marine life near the ocean floor.
        This is done by drawing low-opacity shapes near the bottom of the screen.
        """
        coral_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Coral 1
        coral1_points = [
            (100, self.height - 20),
            (120, self.height - 60),
            (140, self.height - 30)
        ]
        # Coral 2
        coral2_points = [
            (600, self.height - 20),
            (620, self.height - 70),
            (640, self.height - 40)
        ]
        pygame.draw.polygon(coral_surface, (*CORAL_COLOUR, 100), coral1_points)
        pygame.draw.polygon(coral_surface, (*CORAL_COLOUR, 100), coral2_points)
        screen.blit(coral_surface, (0, 0))

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

TOP_COLOUR = (173, 216, 230)  # Light, sunlit blue (water surface)
BOTTOM_COLOUR = (0, 0, 128)  # Deep navy blue (ocean depths)
WAVE_COLOUR = (255, 255, 255, 90)  # White semi-transparent for waves
BEAM_COLOUR = (255, 255, 224, 40)  # Light yellowish beams (RGBA)
CORAL_COLOUR = (139, 69, 19)  # Brownish colour for coral silhouettes
BUBBLE_COLOUR = (224, 255, 255)  # Light cyan for bubbles

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
shooting=False

# player velocity
v = 5

# instantiating player object
player = Player()

font=pygame.font.SysFont("Arial", 20)

bubble = Projectile(player)
background = OceanBackground(SCREEN_WIDTH, SCREEN_HEIGHT)
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

    background.draw(screen)

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
# imports
import pygame

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


# classes for the player and enemies and stuff will go here
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # loads image
        self.img = pygame.image.load(player_img).convert_alpha()
        # can change to smth other than 50x50 pixels if you want
        self.rect = pygame.Rect(0, 0, 50, 50)
    
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


# quite important for pygame to work
pygame.init()

# screen stuff
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# player velocity
v = 5

# instantiating player object
player = Player()

# creates a group of all sprites making it easier later to update them all
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# makes framerate constant across different machines
clock = pygame.time.Clock()
FPS = 30


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
    
    # gets dict of all keys pressed for moving player
    pressed_keys = pygame.key.get_pressed()
    
    # updating player stuff
    player.move(pressed_keys)
    player.wall_collide()
    
    screen.fill((0, 0, 0))
    
    # draw sprites to screen surface
    for entity in all_sprites:
        screen.blit(entity.img, entity.rect)
    
    # updates everything
    pygame.display.flip()
    # wait a bit
    clock.tick(FPS)
    

# goodbye
pygame.quit()

import pygame
import random
import os

# consts
WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialise assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# example sprite class
class Player(pygame.sprite.Sprite):
    # basic player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "test.png")).convert()
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

# initials
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MEW')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# main loop
running = True
while running:
    # keep loop speed in accordance with FPS
    clock.tick(FPS)
    # process input
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # updates
    all_sprites.update()

    screen.fill(BLUE)
    all_sprites.draw(screen)
    # flip always last
    pygame.display.flip()

pygame.quit()

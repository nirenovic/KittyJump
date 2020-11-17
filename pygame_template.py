import pygame
import random

# consts
WIDTH = 360
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initials
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MEW')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
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

    screen.fill(BLACK)
    all_sprites.draw(screen)
    # flip always last
    pygame.display.flip()

pygame.quit()

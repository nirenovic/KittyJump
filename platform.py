import pygame
from settings import *
from powerup import *
Vector = pygame.math.Vector2

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.image.fill(WHITE)
        self.rect.y = y
        self.reached = False

    def update(self):
        #self.rect.x += 5
        #pass
        #color_modifier = abs(self.rect.y - (HEIGHT / 2)) // abs(HEIGHT / 2)
        try:
            color_modifier = (self.rect.y - (HEIGHT / 2)) / (HEIGHT / 2)
            updated_shade = 255 * (1 - (color_modifier * 0.05))
            updated_color = (updated_shade, updated_shade, updated_shade)
            self.image.fill(updated_color)
        except:
            self.image.fill(WHITE)

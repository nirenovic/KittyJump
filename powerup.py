import pygame
from random import choice
from os import path

class Powerup(pygame.sprite.Sprite):
    def __init__(self, game, platform):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.platform = platform
        self.type = choice(['boost'])

import pygame
from settings import *
from game import *
from os import path

class Background:
    def __init__(self, game):
        self.game = game
        self.clouds = pygame.sprite.Group()
        self.init_clouds()

    def update(self):
        self.clouds.update()

    def draw(self, screen):
        self.clouds.draw(screen)

    def init_clouds(self):
        cloud1 = Cloud(self, (WIDTH / 2, HEIGHT))
        cloud2 = Cloud(self, ((WIDTH / 2) - WIDTH, HEIGHT))
        self.clouds.add(cloud1)
        self.clouds.add(cloud2)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, background, midbottom):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.reset_pos = ((WIDTH / 2) - WIDTH + 1, HEIGHT)
        self.image = pygame.image.load(path.join(self.background.game.img_dir, "clouds.png")).convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (WIDTH, int(self.rect.height * (WIDTH / self.rect.width))))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom
        self.last_update = 0
        self.update_interval = 70

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.update_interval:
            self.last_update = current_time
            self.rect.x += 1
        if self.rect.x > WIDTH:
            self.rect.midbottom = self.reset_pos

import pygame
from settings import *

Vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.facing_left = True
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        #self.image = pygame.Surface((20, 30))
        #self.image.fill(PALE_PINK)
        self.image = self.game.player_spritesheet.get_image(0, 0, 416, 454)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

    def load_images(self):
        self.idle_frames_right = [
            self.game.player_spritesheet.get_image(0, 0, 416, 454),
            self.game.player_spritesheet.get_image(416, 0, 416, 454),
            self.game.player_spritesheet.get_image(832, 0, 416, 454),
            self.game.player_spritesheet.get_image(1248, 0, 416, 454),
            self.game.player_spritesheet.get_image(0, 454, 416, 454),
            self.game.player_spritesheet.get_image(416, 454, 416, 454),
            self.game.player_spritesheet.get_image(832, 454, 416, 454),
            self.game.player_spritesheet.get_image(1248, 454, 416, 454),
            self.game.player_spritesheet.get_image(0, 908, 416, 454),
            self.game.player_spritesheet.get_image(416, 908, 416, 454),
            self.game.player_spritesheet.get_image(832, 908, 416, 454),
            self.game.player_spritesheet.get_image(1248, 908, 416, 454),
            self.game.player_spritesheet.get_image(0, 1362, 416, 454),
            self.game.player_spritesheet.get_image(416, 1362, 416, 454),
            self.game.player_spritesheet.get_image(832, 1362, 416, 454),
            self.game.player_spritesheet.get_image(1248, 1362, 416, 454)
        ]

        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame, True, False))

        self.jumping_frames_right = [
            self.game.player_spritesheet.get_image(0, 1816, 416, 454),
            self.game.player_spritesheet.get_image(416, 1816, 416, 454),
            self.game.player_spritesheet.get_image(832, 1816, 416, 454),
            self.game.player_spritesheet.get_image(1248, 1816, 416, 454),
            self.game.player_spritesheet.get_image(0, 2270, 416, 454),
            self.game.player_spritesheet.get_image(416, 2270, 416, 454),
            self.game.player_spritesheet.get_image(832, 2270, 416, 454),
            self.game.player_spritesheet.get_image(1248, 2270, 416, 454),
            self.game.player_spritesheet.get_image(0, 2724, 416, 454),
            self.game.player_spritesheet.get_image(416, 2724, 416, 454),
            self.game.player_spritesheet.get_image(832, 2724, 416, 454),
            self.game.player_spritesheet.get_image(1248, 2724, 416, 454),
            self.game.player_spritesheet.get_image(0, 3178, 416, 454),
            self.game.player_spritesheet.get_image(416, 3178, 416, 454),
            self.game.player_spritesheet.get_image(832, 3178, 416, 454),
            self.game.player_spritesheet.get_image(1248, 3178, 416, 454),
            self.game.player_spritesheet.get_image(0, 3632, 416, 454),
            self.game.player_spritesheet.get_image(416, 3632, 416, 454),
            self.game.player_spritesheet.get_image(832, 3632, 416, 454),
            self.game.player_spritesheet.get_image(1248, 3632, 416, 454),
            self.game.player_spritesheet.get_image(0, 4086, 416, 454),
            self.game.player_spritesheet.get_image(416, 4086, 416, 454),
            self.game.player_spritesheet.get_image(832, 4086, 416, 454),
            self.game.player_spritesheet.get_image(1248, 4086, 416, 454),
            self.game.player_spritesheet.get_image(0, 4540, 416, 454),
            self.game.player_spritesheet.get_image(416, 4540, 416, 454),
            self.game.player_spritesheet.get_image(832, 4540, 416, 454),
            self.game.player_spritesheet.get_image(1248, 4540, 416, 454),
            self.game.player_spritesheet.get_image(0, 4994, 416, 454),
            self.game.player_spritesheet.get_image(416, 4994, 416, 454)
        ]

        self.jumping_frames_left = []
        for frame in self.jumping_frames_right:
            self.jumping_frames_left.append(pygame.transform.flip(frame, True, False))

    def update(self):
        self.animate()
        self.acc = Vector(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.facing_left = False

        # wrap around screen
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = WIDTH

        # apply frictional forces
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # add current acceleration to current velocity
        self.vel += self.acc
        # position = current velocity + current acceleration / 2
        self.pos += self.vel + PLAYER_ACC * self.acc
        # set center of sprite to computed position value
        self.rect.midbottom = self.pos
        # check if jumping, walking
        if self.vel.y == 0:
            self.jumping = False

    def animate(self):
        current_time = pygame.time.get_ticks()
        if not self.walking and not self.jumping:
            if self.facing_left:
                frames = self.idle_frames_left
            else:
                frames = self.idle_frames_right
            update_interval = 70
        elif self.jumping == True:
            if self.facing_left:
                frames = self.jumping_frames_left
            else:
                frames = self.jumping_frames_right
            update_interval = 120

        if current_time - self.last_update > update_interval:
            self.last_update = current_time
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]
            self.image.set_colorkey(BLACK)

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -1 * PLAYER_JUMP_HEIGHT
        self.jumping = True

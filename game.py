import pygame
import random
from settings import *
from player import Player
from platform import Platform
from spritesheet import Spritesheet
from background import *
from os import path

Vector = pygame.math.Vector2

class Game(object):
    def __init__(self):
        # initials
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.load_data()
        self.running = True
        self.background = Background(self)

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.font_dir = path.join(self.dir, 'fonts')
        self.sound_dir = path.join(self.dir, 'sound')

        try:
            with open(path.join(self.dir, HIGH_SCORE_FILE), 'r+') as file:
                self.highscore = int(file.read())
        except:
            self.highscore = 0
        # load Spritesheet
        self.player_spritesheet = Spritesheet(path.join(self.img_dir, PLAYER_SPRITESHEET))
        # load sounds
        self.music = pygame.mixer.music.load(path.join(self.sound_dir, BACKGROUND_MUSIC))


    def new(self):
        self.score = -10
        self.playing = True
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.max_platforms = 8
        self.platforms = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        base_platform = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.all_sprites.add(base_platform)
        self.platforms.add(base_platform)
        self.player.pos = self.platforms.sprites()[0].rect.midtop + Vector(0, 1)
        self.all_sprites.add(self.player)
        self.entities.add(self.player)
        self.generate_platforms(self.max_platforms)
        self.run()

    def run(self):
        pygame.mixer.music.play(loops = -1)
        while self.playing:
            self.clock.tick(FPS)
            self.process_events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(2000)

    def update(self):
        self.all_sprites.update()
        self.background.update()
        # check collisions if player velocity is downwards
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #self.score += 10
                #self.score_text = self.font.render(str(self.score), False, (0, 0, 0))
                self.player.rect.y -= self.player.vel.y
                if self.player.rect.colliderect(hits[0].rect) != True:
                    if self.player.pos.x > hits[0].rect.left and \
                    self.player.pos.x < hits[0].rect.right:
                        self.player.pos.y = hits[0].rect.top + 1
                        self.player.vel.y = 0
                if hits[0].reached == False:
                    hits[0].reached = True
                    self.add_score(10)

        #self.test_text = self.font.render(str(self.player.vel.y), False, (0, 0, 0))

        # move camera upwards
        if self.player.rect.top  <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for p in self.platforms:
                p.rect.y += abs(self.player.vel.y)
        # remove platforms that go below bottom of screen
        platform_count = 0
        for p in self.platforms:
            platform_count += 1
            if p.rect.top >= HEIGHT:
                p.kill()
                self.spawn_new_platform()

        # PLAYER DEATH
        # move platforms if player falls
        if self.player.rect.bottom > HEIGHT:
            for s in self.all_sprites:
                s.rect.y -= max(self.player.vel.y, 10)
                if s.rect.bottom < 0:
                    s.kill()

        if len(self.platforms) == 0 and self.player.rect.y > HEIGHT + 1000:
            self.playing = False

        #self.test_text = self.font.render(str(self.player_max_vel), False, (0, 0, 0))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        self.background.draw(self.screen)
        self.platforms.draw(self.screen)
        self.entities.draw(self.screen)
        self.draw_text(str(self.score), SCORE_FONT, 30, PALE_YELLOW, 30, 10)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(SKY_BLUE)
        self.draw_text('Jump to Heaven', GAME_FONT, 40, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press the arrow keys to move", GAME_FONT, 18, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("spacebar to jump", GAME_FONT, 18, WHITE, WIDTH / 2, HEIGHT / 2 + 30)
        self.draw_text("Press any key to play", GAME_FONT, 24, WHITE, WIDTH / 2, HEIGHT * 0.75)
        self.draw_text("High Score " + str(self.highscore), GAME_FONT, 24, WHITE, WIDTH / 2, 25)
        pygame.display.flip()
        self.wait_for_any_key()

    def show_end_screen(self):
        if not self.running:
            return
        self.screen.fill(BITTERSWEET)
        self.draw_text("Game over", GAME_FONT, 40, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to play again", GAME_FONT, 24, WHITE, WIDTH / 2, HEIGHT * 0.75)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New high score " + str(self.score) + "!", SCORE_FONT, 30, WHITE, WIDTH / 2, HEIGHT / 2)
            with open(path.join(self.dir, HIGH_SCORE_FILE), 'w') as file:
                file.write(str(self.score))
        else:
            self.draw_text("Score " + str(self.score), SCORE_FONT, 30, WHITE, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_any_key()

    def wait_for_any_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def generate_platforms(self, num):
        start_ypos = self.platforms.sprites()[0].rect.y - PLATFORM_HEIGHT
        ypos = random.randint(start_ypos - 100, start_ypos - self.player.rect.height)
        for n in range(0, num):
            platform = Platform(random.randint(0, WIDTH - 50), ypos, random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH), PLATFORM_HEIGHT)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            ypos -= random.randint(80, 120)

    def spawn_new_platform(self):
        platform = Platform(random.randint(0, WIDTH - 50),
                            self.platforms.sprites()[len(self.platforms.sprites())-1].rect.y - random.randint(80, 120),
                            random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH), PLATFORM_HEIGHT)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

    def add_score(self, score):
        self.score += score

    def draw_text(self, text, font, size, color, x, y):
        try:
            self.font = pygame.font.Font(path.join(self.font_dir, font), size)
        except:
            self.font = pygame.font.SysFont('arial', size)

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

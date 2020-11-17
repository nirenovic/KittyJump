import pygame
import random
import os
from settings import *
from game import Game

game = Game()

game.show_start_screen()

while game.running:
    game.new()
    game.show_end_screen()

pygame.quit()

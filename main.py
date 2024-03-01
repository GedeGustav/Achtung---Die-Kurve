import pygame
from snake import Snake
from game_elev import Game
import constants

pygame.init()

game = Game()

while game.running:

    game.run()
    

pygame.quit()
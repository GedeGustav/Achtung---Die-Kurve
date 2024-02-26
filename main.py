import pygame
from snake import Snake
from game_elev import Game
import constants

pygame.init()

clock = pygame.time.Clock()
game = Game()

while game.running:

    game.run()
    
    clock.tick(constants.FPS)

pygame.quit()
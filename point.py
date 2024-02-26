import pygame
import random
from constants import *

class Point(pygame.sprite.Sprite):
    def __init__(self, screen, color):
        super().__init__()
        self.screen = screen
        self.color = color
        self.image = pygame.Surface((TILE_WIDTH, TILE_WIDTH))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.random_position()
        self.eaten = False
        
    def random_position(self):
        return (random.randint(0,BOARD[0]))*TILE_WIDTH,(random.randint(0,BOARD[1])*TILE_WIDTH)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)    


       
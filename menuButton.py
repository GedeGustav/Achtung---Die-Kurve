import pygame
import random
from constants import *

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, screen, text, coords):
        super().__init__()
        self.screen = screen
        self.color = (232, 204, 125)
        self.image = pygame.Surface((300, 70))
        self.image.fill(self.color)
        
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = coords[0]-self.rect.width/2, coords[1]

        self.text = text
            
    def draw(self, surface):
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.text), 1, WHITE)
        
        surface.blit(self.image, self.rect)
        surface.blit(text, self.rect)
    
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return [True, self.text]
        else:
            return [False, "Not an menu item"]

   
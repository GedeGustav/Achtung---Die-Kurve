import pygame
import random
from constants import *

class Snake(pygame.sprite.Sprite):
    def __init__(self, screen, color, mode):
        super().__init__()
        self.screen = screen
        self.color = color
        self.image = pygame.Surface((TILE_WIDTH, TILE_WIDTH))
        self.image.fill(color)
        self.speed = 1
        self.mode = mode
        
        self.snake_head = (12, 12)
        self.snake_body = [(12,11), (12,10)]
        self.score_count = 0
        
        self.move = "down" #The snake will move this direction, other possible values are "up", "left" and "right"
        self.dead = False
        self.rects=[] #List for storing the body parts of the snake

        self.rect = self.image.get_rect()

        self.rect.x = self.snake_head[0]*TILE_WIDTH
        self.rect.y = self.snake_head[1]*TILE_WIDTH

        for body_part in self.snake_body:
            self.rects.append(pygame.Rect(body_part[0]*TILE_WIDTH, body_part[1]*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH))
    
    def score(self):
        self.score_count += 1
        self.snake_body.append(self.snake_head)

    def draw(self, surface):
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.score_count), 1, WHITE)
        surface.blit(text, ((surface.get_rect().width/2)-text.get_width()/2, 50))
        for rect in self.rects:
            surface.blit(self.image, rect)
        surface.blit(self.image, self.rect)    

    def update(self):
    
        self.snake_body.insert(0, self.snake_head)
        self.snake_body.pop()

        (x, y) = self.snake_head

        if self.move == "up":
            if (x, y-self.speed) not in self.snake_body:
                self.snake_head = (x, y-self.speed)
            else:
                self.snake_head = (x, y+self.speed)
            if y == 0:
                self.dead = True
                self.kill()
        elif self.move == "left":
            if (x-self.speed, y) not in self.snake_body:
                self.snake_head = (x-self.speed, y)
            else:
                self.snake_head = (x+self.speed, y)
            if x == 0:
                self.dead = True
                self.kill()
        elif self.move == "down":
            if (x, y+self.speed) not in self.snake_body:
                self.snake_head = (x, y+self.speed)
            else:
                self.snake_head = (x, y-self.speed)
            if y >= BOARD[1]:
                self.dead = True
                self.kill()
                
        elif self.move == "right":
            if (x+self.speed, y) not in self.snake_body:
                self.snake_head = (x+self.speed, y)
            else:
                self.snake_head = (x-self.speed, y)
            if x >= BOARD[0]:
                self.dead = True
                self.kill()
        if self.snake_head in self.snake_body:
            self.dead = True
            self.kill()
        
        self.rect.x = self.snake_head[0]*TILE_WIDTH
        self.rect.y = self.snake_head[1]*TILE_WIDTH

        self.rects=[]

        for body_part in self.snake_body:
            self.rects.append(pygame.Rect(body_part[0]*TILE_WIDTH, body_part[1]*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH))
        
        print(f"X: {self.snake_head[0]} Y: {self.snake_head[1]}")
        
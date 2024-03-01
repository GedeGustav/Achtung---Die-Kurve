import pygame
import random
import time


pygame.init()

size = WIDTH, HEIGHT = 800, 600


screen = pygame.display.set_mode((800, 600))
screen.fill((255, 0, 255))


power_modes = ["normal", "speed", "slow", "big", "90_turn"]


class Player:
    def __init__(self, color):
        self.color = color
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 2
        self.rotation = 90
        self.direction = pygame.Vector2(0, 1)
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.rects = []
        self.invisible_time = 15
        self.mode = power_modes[0]


    def update(self):
        """keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.rotate_ip(-self.rotation)
        if keys[pygame.K_d]:
            self.direction.rotate_ip(self.rotation)"""

        """for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.direction.rotate_ip(-self.rotation)
                if event.key == pygame.K_d:
                    self.direction.rotate_ip(self.rotation)"""


        self.movement()
        self.rect = pygame.Rect(self.x, self.y, 5, 5)

        if self.invisible_time <= 0:
            self.draw()
            self.rects.append(self.rect)
        self.invisible_time -= 1

        if self.invisible_time <= -200:
            self.invisible_time = 15

        if len(self.rects) > 10:
            self.collision()

    def movement(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self):
        #pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
        pygame.draw.rect(screen, self.color, self.rect)

    def collision(self):
        for rect in self.rects[0: len(self.rects) - 10]:
            if self.rect.colliderect(rect):
                print("Game Over")
                pygame.quit()
                exit()

player1 = Player((255, 255, 255)) 

while True:
    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player1.direction.rotate_ip(-player1.rotation)
            if event.key == pygame.K_a:
                player1.direction.rotate_ip(-player1.rotation)

    player1.update()
    print(player1.direction)

    pygame.display.flip()
    pygame.time.Clock().tick(60)



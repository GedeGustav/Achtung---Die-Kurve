import pygame
import random
import time


pygame.init()

size = WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

power_modes = ["normal", "speed", "slow", "big", "90_turn"]


class Player:
    def __init__(self, color, left, right):
        self.color = color
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 2
        self.rotation = 3
        self.direction = pygame.Vector2(0, 1)
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.rects = []
        self.invisible_time = 15
        self.mode = power_modes[0]
        self.left = left
        self.right = right


    def update(self):
        if self.mode == power_modes[0]:
            self.rotation = 3
            keys = pygame.key.get_pressed()
            if keys[self.left]:
                self.direction.rotate_ip(-self.rotation)
            if keys[self.right]:
                self.direction.rotate_ip(self.rotation)


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
                pygame.quit()
                exit()

players = [
            Player((255, 0, 0), pygame.K_a, pygame.K_d),
            Player((0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT),
            Player((0, 0, 255), pygame.K_o, pygame.K_p)
          ]

while True:
    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            for player in players:
                """if player.mode == power_modes[4]:
                    player.rotation = 90
                    if event.key == pygame.K_a:
                        player.direction.rotate_ip(-player.rotation)
                    if event.key == pygame.K_d:
                        player.direction.rotate_ip(player.rotation)"""
    for player in players:       
        player.update()
   
    pygame.display.flip()
    pygame.time.Clock().tick(60)



import pygame
import random
import time


pygame.init()

size = WIDTH, HEIGHT = 1000, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((200, 200, 200))

power_modes = ["normal", "speed", "slow", "big", "90_turn"]

powerup_images = [pygame.image.load("Images/speed.jpg"), pygame.image.load("Images/slow.jpg"), pygame.image.load("Images/size.jpg"), pygame.image.load("Images/90_turn.jpg")]

class Powerup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mode = power_modes[random.randint(1, 4)]
        self.image = powerup_images[power_modes.index(self.mode) - 1]
        self.rect = self.image.get_rect()
        self.color = (0, 0, 0)

    def draw(self):
        self.rect.center = (self.x, self.y)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        screen.blit(self.image, self.rect)

    def update(self):
        self.draw()



class Player:
    def __init__(self, color, left, right):
        self.color = color
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 2
        self.direction = pygame.Vector2(0, 1)
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.rect.center = (self.x, self.y)
        self.rects = []
        self.invisible_time = 15
        self.mode = power_modes[0]
        self.left = left
        self.right = right


    def update(self):
        if self.mode == power_modes[0]:
            self.power_0()

        if self.mode == power_modes[1]:
            self.power_1()

        if self.mode == power_modes[2]:
            self.power_2()

        if self.mode == power_modes[3]:
            self.power_3()

        if self.mode == power_modes[4]:
            self.power_0()

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

        self.powerup_collision()

    def power_0(self):
        self.speed = 2
        self.rotation = 4
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)

    def power_1(self):
        self.speed = 4
        self.rotation = 4
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)

    def power_2(self):
        self.speed = 1
        self.rotation = 4
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)

    def power_3(self):
        self.speed = 2
        self.rotation = 4
        self.rect.width = 3
        self.rect.height = 3
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)

    def power_4(self):
        pass

    def movement(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def collision(self):
        for rect in self.rects[0: len(self.rects) - 10]:
            if self.rect.colliderect(rect):
                pygame.quit()
                exit()

    def powerup_collision(self):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.mode = powerup.mode
                powerups.remove(powerup)

players = [
            Player((255, 0, 0), pygame.K_a, pygame.K_d),
            #Player((0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT),
            #Player((0, 0, 255), pygame.K_o, pygame.K_p)
          ]

powerups = [Powerup(100, 100)]

while True:
    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        """if event.type == pygame.KEYDOWN:
            for player in players:
                if player.mode == power_modes[4]:
                    player.rotation = 90
                    if event.key == pygame.K_a:
                        player.direction.rotate_ip(-player.rotation)
                    if event.key == pygame.K_d:
                        player.direction.rotate_ip(player.rotation)"""
    for player in players:       
        player.update()
        print(player.mode)

    for powerup in powerups:
        powerup.update()
   


    pygame.display.flip()
    pygame.time.Clock().tick(60)



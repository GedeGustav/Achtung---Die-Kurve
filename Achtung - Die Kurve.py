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
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.color = (0, 0, 0)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.draw()
        self.collision()

    def collision(self):
        for player in players:
            for rect in player.rects:
                if self.rect.colliderect(rect):
                    pygame.draw.rect(screen, (200, 200, 200), 
                                    (self.x - self.image.get_width()/2, 
                                     self.y- self.image.get_height()/2, 
                                     self.image.get_width() + 1, self.image.get_height() + 1))
                    
                    powerups.remove(self)
                    pygame.draw.rect(screen, (player.color), rect)
                    pygame.display.flip()
                    

class Player:
    def __init__(self, color, left, right, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.direction = (pygame.Vector2(WIDTH/2, HEIGHT/2) - pygame.Vector2(x, y)).normalize()
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.rect.center = (self.x, self.y)
        self.rects = []
        self.invisible_time = 15
        self.mode = power_modes[0]
        self.power_time = 300
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
            self.power_4()

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
        self.outOfBounds()

    def power_0(self):
        self.power_time = 300
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
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = 300

    def power_2(self):
        self.speed = 1
        self.rotation = 4
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = 300

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
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = 300

    def power_4(self):
        self.speed = 2
        self.rotation = 4

        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = 300


    def movement(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def outOfBounds(self):
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            pygame.quit()
            exit()

    def collision(self):
        for rect in self.rects[0: len(self.rects) - 10]:
            if self.rect.colliderect(rect):
                pygame.quit()
                exit()
        for player in players:
            if player != self:
                for rect in player.rects:
                    if self.rect.colliderect(rect):
                        pygame.quit()
                        exit()

    def powerup_collision(self):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.mode = powerup.mode

players = [
            Player((255, 0, 0), pygame.K_a, pygame.K_d, WIDTH/10, HEIGHT/10),
            #Player((0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT, WIDTH - WIDTH/10, HEIGHT/10),
            #Player((0, 0, 255), pygame.K_o, pygame.K_p, WIDTH/10, HEIGHT - HEIGHT/10),
            #Player((255, 255, 0), pygame.K_v, pygame.K_b, WIDTH - WIDTH/10, HEIGHT - HEIGHT/10)
          ]

powerups = [Powerup(500, 500)]

power_up_spawn_time = 600


class button:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self):  
        self.draw()
        self.collision()

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))

    def collision(self):
        if pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[0] < self.x + self.width and pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1] < self.y + self.height:
            if pygame.mouse.get_pressed()[0]:
                print("bing")
 

def game(timer):
    button1 = button(100, 100, 100, 100)
    button1.update()
    timer -= 1
    if timer <= 0:
        powerups.append(Powerup(random.randint(25, WIDTH - 25), random.randint(25, HEIGHT - 25)))
        timer = 600
    
    for player in players:       
        player.update()

    for powerup in powerups:
        powerup.update()


    pygame.display.flip()


while True:
    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            for player in players:
                if player.mode == power_modes[4]:
                    player.rotation = 90
                    if event.key == player.left:
                        player.direction.rotate_ip(-player.rotation)
                    if event.key == player.right:
                        player.direction.rotate_ip(player.rotation)
    
  
    pygame.time.Clock().tick(60)
    game(power_up_spawn_time)



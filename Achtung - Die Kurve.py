import pygame
import random
from Variables import *

pygame.init()

size = WIDTH, HEIGHT = screen_width, screen_height

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((200, 200, 200))

pygame.display.set_caption("Achtung - Die Kurve")

power_modes = ["normal", "speed", "slow", "big", "90_turn"]

powerup_images = [pygame.image.load("Images/speed.jpg"), 
                  pygame.image.load("Images/slow.jpg"), 
                  pygame.image.load("Images/size.jpg"), 
                  pygame.image.load("Images/90_turn.jpg")]

class Powerup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mode = power_modes[random.randint(1, 4)]
        self.image = powerup_images[power_modes.index(self.mode) - 1]
        self.image = pygame.transform.scale(self.image, powerup_size)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.color = (0, 0, 0)
        for player in players:
            for rect in player.rects:
                if self.rect.colliderect(rect):
                    print("collided")
                    self.x = random.randint(25, WIDTH - 25)
                    self.y = random.randint(25, HEIGHT - 25)
                    self.rect.center = (self.x, self.y)

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
        self.width = player_size[0]
        self.height = player_size[1]
        self.direction = (pygame.Vector2(WIDTH/2 - game_stats_bar_width/2, HEIGHT/2) - pygame.Vector2(x, y)).normalize()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.rects = []
        self.invisible_time = 15
        self.mode = power_modes[0]
        self.power_time = powerup_duration
        self.left = left
        self.right = right
        self.alive = True

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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.invisible_time <= 0:
            self.draw()
            self.rects.append(self.rect)
        self.invisible_time -= 1

        if self.invisible_time <= -180:
            self.invisible_time = player_hole_duration

        if len(self.rects) > 30:
            self.collision()

        self.powerup_collision()
        self.outOfBounds()

    def normal_input(self):
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.direction.rotate_ip(-self.rotation)
        if keys[self.right]:
            self.direction.rotate_ip(self.rotation)
        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = powerup_duration


    def power_0(self): #normal
        self.power_time = powerup_duration
        self.speed = player_speed
        self.rotation = player_rotation_speed
        self.width = player_size[0]
        self.height = player_size[1]
        self.normal_input()

    def power_1(self): #speed
        self.speed = player_speed * 2
        self.rotation = player_rotation_speed
        self.width = player_size[0]
        self.height = player_size[1]
        self.normal_input()

    def power_2(self): #slow
        self.speed = player_speed / 2
        self.rotation = player_rotation_speed
        self.width = player_size[0]
        self.height = player_size[1]
        self.normal_input()

    def power_3(self): #big
        self.speed = player_speed
        self.rotation = player_rotation_speed
        self.width = player_size[0] * 3
        self.height = player_size[1] * 3
        self.normal_input()

    def power_4(self): #90_turn
        self.speed = player_speed
        self.width = player_size[0]
        self.height = player_size[1]

        self.power_time -= 1
        if self.power_time <= 0:
            self.mode = power_modes[0]
            self.power_time = powerup_duration

    def movement(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def outOfBounds(self):
        if self.x < 0 or self.x > WIDTH - game_stats_bar_width or self.y < 0 or self.y > HEIGHT:
            self.alive = False

    def collision(self):
        for rect in self.rects[0: len(self.rects) - 30]:
            if self.rect.colliderect(rect):
                print("you killed yourself :(")
                self.alive = False

        for player in players:
            if player != self:
                for rect in player.rects:
                    if self.rect.colliderect(rect):
                        self.alive = False

    def powerup_collision(self):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.mode = powerup.mode

players = []

powerups = [Powerup(WIDTH/2 - game_stats_bar_width/2, HEIGHT/2)]

power_up_spawn_time = powerup_spawn_rate

class Button:
    def __init__(self, x, y, width, height, text, text_size) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.text = text
        self.text_size = text_size

    def update(self, playerCount):  
        self.draw()
        self.collision(playerCount)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text = font.render(self.text, True, (255, 255, 255))
        textRect = text.get_rect()
        screen.blit(text, (self.x - textRect.width/2, self.y - textRect.height/2))
    
    def collision(self, playerCount):
        if (pygame.mouse.get_pos()[0] > self.x - self.width/2 and 
            pygame.mouse.get_pos()[0] < self.x + self.width/2 and 
            pygame.mouse.get_pos()[1] > self.y - self.height/2 and 
            pygame.mouse.get_pos()[1] < self.y + self.height/2):
            
            if pygame.mouse.get_pressed()[0]:
                if self.text == "START":
                    game(power_up_spawn_time)

                if self.text == "2":
                    playerCount = 2
                    print(playerCount)

                if self.text == "3":
                    playerCount = 3
                    print(playerCount)

                if self.text == "4":
                    playerCount = 4 
                    print(playerCount)

                if self.text == "Menu":
                    menu()

                if self.text == "Restart":
                    game(power_up_spawn_time)

        return playerCount

def game(timer):
    global players
    players = [
            Player((255, 0, 0), pygame.K_a, pygame.K_d, WIDTH/10, HEIGHT/10),
            Player((0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT, WIDTH - WIDTH/10 - game_stats_bar_width, HEIGHT/10),
            Player((0, 0, 255), pygame.K_o, pygame.K_p, WIDTH/10, HEIGHT - HEIGHT/10),
            Player((255, 0, 255), pygame.K_v, pygame.K_b, WIDTH - WIDTH/10 - game_stats_bar_width, HEIGHT - HEIGHT/10)
          ]
    
    global powerups
    powerups = [Powerup(WIDTH/2 - game_stats_bar_width/2, HEIGHT/2)]
    
    screen.fill((200, 200, 200))

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
    
        clock.tick(60)

        timer -= 1
        if timer <= 0:
            powerups.append(Powerup(random.randint(25, WIDTH - 25), random.randint(25, HEIGHT - 25)))
            timer = power_up_spawn_time
        
        for player in players: 
            if players.index(player) <= playerCount - 1 and player.alive:
                player.update()      

        for powerup in powerups:
            powerup.update()

        # game stats bar
        pygame.draw.rect(screen, game_stats_bar_color, (WIDTH - game_stats_bar_width, 0, game_stats_bar_width, HEIGHT))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = (font.render("Score:", True, (255, 255, 255)))
        screen.blit(text, (WIDTH - game_stats_bar_width/2 - text.get_rect().width/2, 10))

        DeadPlayers = 0

        for player in players:
            if players.index(player) <= playerCount - 1:
                text = (font.render(str(round(len(player.rects) / 60)), True, (255, 255, 255)))
                screen.blit(text, (WIDTH - game_stats_bar_width/2 - text.get_rect().width/2, 100 + players.index(player) * 100))

            if player.alive == False:
                DeadPlayers += 1


        gameButtons = [
                    Button(WIDTH - game_stats_bar_width/2, HEIGHT-100, 240, 50, "Menu", 32),
                    Button(WIDTH - game_stats_bar_width/2, HEIGHT-200, 240, 50, "Restart", 32)
                    ]

        for button in gameButtons:
            button.update(playerCount)

        pygame.display.flip()

def menu():
    global playerCount
    playerCount = Player_default_count

    menuButtons = [
                Button(WIDTH/2, 200, 500, 200, "START", 100), 
                Button(WIDTH/2 - 150, 500, 50, 50, "2", 32),
                Button(WIDTH/2, 500, 50, 50, "3", 32),
                Button(WIDTH/2 + 150, 500, 50, 50, "4", 32)
              ]
    
    player_banners = [pygame.image.load("Images\Player 1.png"), pygame.image.load("Images\Player 2.png"), pygame.image.load("Images\Player 3.png"), pygame.image.load("Images\Player 4.png")]                                 

    while True:
        screen.fill((220, 220, 220))
        for button in menuButtons:
            button.update(playerCount)
            playerCount = button.collision(playerCount)
        
        for x in range(playerCount):
            playerBanner = player_banners[x]
            playerBanner = pygame.transform.scale(playerBanner, (350, 50))
            screen.blit(playerBanner, (WIDTH/2 - playerBanner.get_size()[0] / 2, 545 + x * 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

menu()
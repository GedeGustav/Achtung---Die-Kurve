import pygame


pygame.init()

size = WIDTH, HEIGHT = 800, 600


screen = pygame.display.set_mode((800, 600))
screen.fill((255, 0, 255))

rot = 1  
rot_speed = 1

# define a surface (RECTANGLE)  
image = pygame.Surface((100 , 100))  
# for making transparent background while rotating an image  
image.set_colorkey((0,0,0))  
# fill the rectangle / surface with green color  
image.fill((0,255,0))   
# define rect for placing the rectangle at the desired position  
rect = image.get_rect()  
rect.center = (WIDTH // 2 , HEIGHT // 2)  






class Player:
    def __init__(self, color):
        self.color = color
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        self.draw()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)


player1 = Player((255, 255, 255)) 


while True:
    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    #player1.update()


    # making a copy of the old center of the rectangle  
    old_center = rect.center 
    # defining angle of the rotation  
    rot = (rot + rot_speed) % 360
    # rotating the orignal image  
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        new_image = pygame.transform.rotate(image , rot)
    elif keys[pygame.K_d]:
        new_image = pygame.transform.rotate(image , -rot)
    else:
        new_image = image
    
    rect = new_image.get_rect()  
    # set the rotated rectangle to the old center  
    rect.center = old_center  
    # drawing the rotated rectangle to the screen  
    screen.blit(new_image , rect)

    pygame.display.update()
    pygame.time.Clock().tick(60)



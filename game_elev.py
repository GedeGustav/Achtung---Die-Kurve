import pygame
from snake import Snake
from point import Point
from menuButton import MenuButton
import constants



clock = pygame.time.Clock()

class Game():
    def __init__(self):

        self.state = "menu"
        self.running = True
        self.size = (500, 500)
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(constants.BLACK)

        self.menu_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.menu_surface.fill((255,255,255,100))

        self.menu_items = {"Play":"game", "Settings":"settings"}
        self.settings = ["Back", "Easy", "Medium", "Hard"]

        self.isSingleplayer = True
        self.mode = "Easy"
        self.players = []
        self.point = None
        
        self.all_sprites = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()
        self.settings_sprites = pygame.sprite.Group()

        self.create_menu()
        self.create_settings()
        pygame.display.set_caption("Snake")

    

    def create_menu(self):
        offset = 30
        for iter, key in enumerate(self.menu_items.keys()):
            button = MenuButton(self.screen, key, [(self.screen.get_width()/2), iter*100+offset])
            self.menu_sprites.add(button)
    
    def create_settings(self):
        offset = 30
        for iter, key in enumerate(self.settings):
            button = MenuButton(self.screen, key, [(self.screen.get_width()/2), iter*100+offset])
            self.settings_sprites.add(button)
    
    def control_game(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.running = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                    self.state = "menu"

        if self.isSingleplayer == True:            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.players[0].move = "up"
            if keys[pygame.K_s]:
                self.players[0].move = "down"
            if keys[pygame.K_a]:
                self.players[0].move = "left"
            if keys[pygame.K_d]:
                self.players[0].move = "right"
            
    def control_menu(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.running = False # Flag that we are done so we exit this loop

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                    self.state = "game"
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                for menu_item in self.menu_sprites:
                    if menu_item.check_click(event.pos)[0]:
                        if menu_item.check_click(event.pos)[1] in self.menu_items.keys():
                            self.state = self.menu_items[menu_item.check_click(event.pos)[1]]

    def control_settings(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.running = False # Flag that we are done so we exit this loop

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                    self.state = "game"
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                for setting_item in self.settings_sprites:
                    if setting_item.check_click(event.pos)[0]:
                        if setting_item.check_click(event.pos)[1] == "Back":
                            self.state = "menu"
                        if setting_item.check_click(event.pos)[1] == "Easy":
                            self.mode = "Easy"
                        if setting_item.check_click(event.pos)[1] == "Medium":
                            self.mode = "Medium"
                        if setting_item.check_click(event.pos)[1] == "Hard":
                            self.mode = "Hard"
       
    def start_game(self, isSingleplayer = True):
        self.isSingleplayer = isSingleplayer
        snake = Snake(self.screen, constants.WHITE, self.mode)
        
        self.players.append(snake)
        self.point = Point(self.screen, constants.RED)
        self.all_sprites.add(snake)  
        self.all_sprites.add(self.point)

    def reset_game(self):
        self.players = []
        self.point = None
        self.all_sprites = pygame.sprite.Group()
        self.start_game()  

    def checkState(self):
        if self.state == "game":
            if self.players == []:
                self.start_game()
            else:
                pass

    def update(self):
        self.checkState()
        
        for player in self.players:
            if player.rect.colliderect(self.point):
                player.score()
                self.point.kill()  
                self.point = Point(self.screen, constants.RED)
                self.all_sprites.add(self.point)

            if player.dead:
                self.reset_game()

        self.all_sprites.update()

    def draw(self):
        
        self.screen.fill(constants.BLACK)
        if self.state == "game":
            
            for sprite in self.all_sprites:
                sprite.draw(self.screen)

        if self.state == "menu" or self.state == "menuStart":
            for sprite in self.all_sprites:
                sprite.draw(self.screen)
            
            self.screen.blit(self.menu_surface, self.menu_surface.get_rect())

            for sprite in self.menu_sprites:
                sprite.draw(self.screen)
        
        if self.state == "settings":
            
            for sprite in self.settings_sprites:
                sprite.draw(self.screen)
            
            self.screen.blit(self.menu_surface, self.menu_surface.get_rect())
            
                       
        pygame.display.flip()

    def run(self):

        clock.tick(constants.FPS)


        if self.state == "game":
            self.update()
            self.control_game()

        if self.state == "menu":
            self.control_menu()
        
        if self.state == "settings":
            self.control_settings()

        self.draw()


    
    

 
    
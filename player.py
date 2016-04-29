from color import *
from config import *
import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, skin):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        ## Skin choice
        if skin == "male" :
            ## Import textures
            self.bunny_stand = pygame.image.load("PNG/Players/bunny1_stand.png").convert()
            self.bunny_walk1_r = pygame.image.load("PNG/Players/bunny1_walk1_r.png").convert()
            self.bunny_walk2_r = pygame.image.load("PNG/Players/bunny1_walk2_r.png").convert()
            self.bunny_walk1_l = pygame.image.load("PNG/Players/bunny1_walk1_l.png").convert()
            self.bunny_walk2_l = pygame.image.load("PNG/Players/bunny1_walk2_l.png").convert()

            ## Set texture background to transparent
            self.bunny_stand.set_colorkey(Color.BLACK)
            self.bunny_walk1_r.set_colorkey(Color.BLACK)
            self.bunny_walk2_r.set_colorkey(Color.BLACK)
            self.bunny_walk1_l.set_colorkey(Color.BLACK)
            self.bunny_walk2_l.set_colorkey(Color.BLACK)

            ## Set texture
            self.image = self.bunny_stand

        elif skin == "femal" :
            ## Import textures
            self.bunny_stand = pygame.image.load("PNG/Players/bunny2_stand.png").convert()
            self.bunny_walk1_r = pygame.image.load("PNG/Players/bunny2_walk1_r.png").convert()
            self.bunny_walk2_r = pygame.image.load("PNG/Players/bunny2_walk2_r.png").convert()
            self.bunny_walk1_l = pygame.image.load("PNG/Players/bunny2_walk1_l.png").convert()
            self.bunny_walk2_l = pygame.image.load("PNG/Players/bunny2_walk2_l.png").convert()

            ## Set texture background to transparent
            self.bunny_stand.set_colorkey(Color.BLACK)
            self.bunny_walk1_r.set_colorkey(Color.BLACK)
            self.bunny_walk2_r.set_colorkey(Color.BLACK)
            self.bunny_walk1_l.set_colorkey(Color.BLACK)
            self.bunny_walk2_l.set_colorkey(Color.BLACK)

            ## Set texture
            self.image = self.bunny_stand
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #self.height_diff = 0
        ## Set diferents variables
        self.jump = 0
        self.speed_base = 5
        self.speed = 0
        self.run_time = 0
        ## Set player default position
        self.rect.y = Config.height - 32 - 94 - self.height
        self.rect.x = 32

    def update(self, run) :
        ## Import diferents classes
    
        ## Player animation
        if run == "right" :
            ## Each images alternate every 20 frames
            if self.run_time < 20: 
                self.image = self.bunny_walk1_r
                self.run_time += 1
            elif self.run_time < 40 :
                self.run_time += 1
                self.image = self.bunny_walk2_r
            else :
                self.run_time = 0
        elif run == "stand" :
            self.image = self.bunny_stand
            self.run_time = 0
        elif run == "left" :
            ## Each images alternate every 20 frames
            if self.run_time < 20: 
                self.image = self.bunny_walk1_l
                self.run_time += 1
            elif self.run_time < 40 :
                self.run_time += 1
                self.image = self.bunny_walk2_l
            else :
                self.run_time = 0


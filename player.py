from color import *
from config import *
import pygame

class Player(pygame.sprite.Sprite):

########## INIT PROCESS ##########

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
        
        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)

        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        ## Set beeing in jump value
        self.in_jump = False
        
        ## Set last y value before jump
        self.last_y = self.rect.y

        ## Set beeing on ground value
        self.on_ground = False

        ## Set value for calculating jump
        self.c_base = -109
        self.c = self.c_base

        ## Set player speed base
        self.speed_base = 5
        self.speed = 0

        ## Set time to incremant animation
        self.animation_time = 0
        
        ## Set player default position
        self.rect.y = Config.height - 32 - 94 - self.height
        self.rect.x = 32

########### RESET PROCESS ##########

    def reset(self, stat) :
        if stat == "after_jump" :
            self.in_jump = False
            self.c = self.c_base
            self.on_ground = False
            self.rect.y += 9
        elif stat == "on_ground" :
            self.in_jump = False
            self.c = self.c_base
            self.on_ground = True

########### JUMP PROCESS ##########

    def jump(self) :
        ## Player jump process
        if self.in_jump == True :
            if (self.c < -(self.c_base)) :
                self.rect.y = (self.last_y - (-(self.c/10)**2+120))
                self.c += 3
                self.on_ground = False
            else :
                ## Reset values
                self.reset("after_jump")

########## ANIMATION AND POSITION UPDATE PROCESS ##########

    def update(self, run) :

        ## Player animation
        if run == "right" :
            ## Each images alternate every 20 frames
            if self.animation_time < 20: 
                self.image = self.bunny_walk1_r
                self.animation_time += 1
            elif self.animation_time < 40 :
                self.animation_time += 1
                self.image = self.bunny_walk2_r
            else :
                self.animation_time = 0

        elif run == "stand" :
            self.image = self.bunny_stand
            self.animation_time = 0

        elif run == "left" :
            ## Each images alternate every 20 frames
            if self.animation_time < 20: 
                self.image = self.bunny_walk1_l
                self.animation_time += 1
            elif self.animation_time < 40 :
                self.animation_time += 1
                self.image = self.bunny_walk2_l
            else :
                self.animation_time = 0

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)

        ## Update player position
        self.rect.x += self.speed


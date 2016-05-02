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

########## PLAYER AND BLOCK COLISION DETECTION ##########

    def colide_block(self, block_list, movable_list, all_game_sprites_list) :

        ## Detect rect colisions between player and ground block
        block_player_list = pygame.sprite.spritecollide(self, block_list, True)
        ## If a rect colision is detected
        if block_player_list != [] :
            ## For each blocks in colision
            for block in block_player_list :
                ## If a bitmap colision is detected
                if pygame.sprite.collide_mask(self, block) != None :
                    ## If the player is enter into the block by the top
                    if (self.rect.y + self.height) <= (block.rect.y + 3) :
                        ## Set ground value to true
                        self.reset("on_ground")
                        ## Set player pos to the top of the block
                        self.rect.y -= 3
                        ## Set the block to last block
                        self.last_block_colide = block
                    ## If the player is enter into the block by the bottom
                    elif (self.rect.y) >= (block.rect.y + block.height - 30) :
                        ## Move the player out of the block
                        self.rect.y += 1 #(block.rect.y + block.height )
                        ## Reset player variables
                        self.reset("after_jump")
                        ## Set block to the last block
                        self.last_block_colide = block
                        ## Gravity
                        self.rect.y += 3
                    ## If the player is enter into the block by the right side
                    elif (self.rect.x + self.width) > (block.rect.x) and (self.rect.x + self.width) < (block.rect.x + block.width) :
                        ## Move the player out of the block
                        self.rect.x -= (5 + self.speed)
                        ## Gravity
                        self.rect.y += 3
                    ## If the player is enter into the block by the left side
                    elif (self.rect.x) < (block.rect.x + block.width) and (self.rect.x) > (block.rect.x) :
                        ## Move the player out of the block
                        self.rect.x += (5 - self.speed)
                        ## Gravity
                        self.rect.y += 3
                
                ## If the player isn't on the block or down the block
                else :
                    ## Set groud val to 0
                    self.on_ground = False
                    ## Gravity
                    self.rect.y += 3
                ## Re-add block to default group
                movable_list.add(block)
                block_list.add(block)
                all_game_sprites_list.add(block)

        ## If the player isn't on the block or down the block
        elif (self.rect.x + self.width) <= (self.last_block_colide.rect.x) or (self.rect.x) >= (self.last_block_colide.rect.x + self.last_block_colide.width) or (self.rect.y) >= (self.last_block_colide.rect.y + self.last_block_colide.height) : 
            ## Set groud val to 0
            self.on_ground = False
            ## Gravity
            self.rect.y += 3

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


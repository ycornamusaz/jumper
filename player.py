from heart import *
from color import *
from config import *
import pygame
import math

class Player(pygame.sprite.Sprite):

########## INIT PROCESS ##########

    def __init__(self, skin):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Skin choice
        if skin == "male" :
            ## Import textures
            self.bunny_stand = pygame.image.load("PNG/Players/bunny1_stand.png").convert()
            self.bunny_walk1_r = pygame.image.load("PNG/Players/bunny1_walk1_r.png").convert()
            self.bunny_walk2_r = pygame.image.load("PNG/Players/bunny1_walk2_r.png").convert()
            self.bunny_walk1_l = pygame.image.load("PNG/Players/bunny1_walk1_l.png").convert()
            self.bunny_walk2_l = pygame.image.load("PNG/Players/bunny1_walk2_l.png").convert()

        elif skin == "femal" :
            ## Import textures
            self.bunny_stand = pygame.image.load("PNG/Players/bunny2_stand.png").convert()
            self.bunny_walk1_r = pygame.image.load("PNG/Players/bunny2_walk1_r.png").convert()
            self.bunny_walk2_r = pygame.image.load("PNG/Players/bunny2_walk2_r.png").convert()
            self.bunny_walk1_l = pygame.image.load("PNG/Players/bunny2_walk1_l.png").convert()
            self.bunny_walk2_l = pygame.image.load("PNG/Players/bunny2_walk2_l.png").convert()

        ## Resize images
        self.bunny_stand = pygame.transform.scale(self.bunny_stand, [int(self.bunny_stand.get_width()*self.conf.factor), int(self.bunny_stand.get_height()*self.conf.factor)])
        self.bunny_walk1_r = pygame.transform.scale(self.bunny_walk1_r, [int(self.bunny_walk1_r.get_width()*self.conf.factor), int(self.bunny_walk1_r.get_height()*self.conf.factor)])
        self.bunny_walk2_r = pygame.transform.scale(self.bunny_walk2_r, [int(self.bunny_walk2_r.get_width()*self.conf.factor), int(self.bunny_walk2_r.get_height()*self.conf.factor)])
        self.bunny_walk1_l = pygame.transform.scale(self.bunny_walk1_l, [int(self.bunny_walk1_l.get_width()*self.conf.factor), int(self.bunny_walk1_l.get_height()*self.conf.factor)])
        self.bunny_walk2_l = pygame.transform.scale(self.bunny_walk2_l, [int(self.bunny_walk2_l.get_width()*self.conf.factor), int(self.bunny_walk2_l.get_height()*self.conf.factor)])

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
        self.jump_height = 300
        self.jump_power = 4
        self.c_base = int(-(math.sqrt(self.jump_height)*10))
        self.c = self.c_base

        ## Set player speed base
        self.speed_base = 8*self.conf.xfactor
        self.speed = 0

        ## Set player's life
        self.life = 3

        ## Set the player immune
        self.imunne = False
        self.imunne_time = 0
        self.imunne_time_base = 200
        self.count = 0

        ## Set time to incremant animation
        self.animation_time = 0
        
        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32

########### RESET PROCESS ##########

    def reset(self, stat) :
        if stat == "after_jump" :
            self.in_jump = False
            self.c = self.c_base
            self.on_ground = False
            #self.rect.y += 9
        elif stat == "on_ground" :
            self.in_jump = False
            self.c = self.c_base
            self.on_ground = True

########## GRAVITY FUNCTION ##########

    def gravity(self, block_list, movable_list, all_game_sprites_list, power):
        #pdb.set_trace()
        self.rect.y += 1
        ## Detect rect colisions between player and ground blocks
        block_player_list = pygame.sprite.spritecollide(self, block_list, True)
        if block_player_list != [] :
            for block in block_player_list :
                ## Detect bitmap colisions between player and ground block
                if pygame.sprite.collide_mask(self, block) != None :
                    ## Set player state to "on ground"
                    self.reset("on_ground")
            
            ## Re-add block to default groups
            movable_list.add(block)
            block_list.add(block)
            all_game_sprites_list.add(block)

        else :
            ## Set plaxer state to "not on ground"
            self.on_ground = False

        self.rect.y -= 1
        
        ## If the player isn't on ground
        if self.on_ground == False :
            ## Apply gravity
            self.rect.y += power


########### JUMP PROCESS ##########

    def jump(self) :
        ## Player jump process
        if self.in_jump == True :
            if (self.c < -(self.c_base)) :
                self.rect.y = (self.last_y - (-(self.c/10)**2+self.jump_height)*self.conf.factor)
                self.c += self.jump_power
                self.on_ground = False
            else :
                self.c -= self.c*2
                self.rect.y -= (-(self.c/10)**2+self.jump_height)
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
                    if (self.rect.y + self.height) < (block.rect.y + 10 + (-(self.c/10)**2+self.jump_height)) :
                        ## Set ground value to true
                        self.reset("on_ground")
                        ## Set player pos to the top of the block
                        self.rect.y = block.rect.y - self.height
                        ## Set the block to last block
                        self.last_block_colide = block
                    ## If the player is enter into the block by the bottom
                    elif (self.rect.y) >= (block.rect.y + block.height - 30) :
                        ## Move the player out of the block
                        self.rect.y += 1
                        ## Reset player variables
                        self.reset("after_jump")
                        ## Set block to the last block
                        self.last_block_colide = block
                        ## Gravity
                        self.rect.y += 3
                    ## If the player is enter into the block by the right side
                    elif (self.rect.x + self.width) > (block.rect.x) and (self.rect.x + self.width) < (block.rect.x + block.width/2) :
                        ## Move the player out of the block
                        self.rect.x -= (5 + self.speed)
                        ## Gravity
                        self.gravity(block_list, movable_list, all_game_sprites_list, 3)
                    ## If the player is enter into the block by the left side
                    elif (self.rect.x) < (block.rect.x + block.width) and (self.rect.x) > (block.rect.x + block.width - block.width/2) :
                        ## Move the player out of the block
                        self.rect.x += (5 - self.speed)
                        ## Gravity
                        self.gravity(block_list, movable_list, all_game_sprites_list, 3)
                
                ## If the player isn't on the block or down the block
                elif self.on_ground == False :
                    self.gravity(block_list, movable_list, all_game_sprites_list, 3)

                ## Re-add block to default group
                movable_list.add(block)
                block_list.add(block)
                all_game_sprites_list.add(block)


########## ANIMATION AND POSITION UPDATE PROCESS ##########

    def update(self, all_game_sprites) :

        ## Player animation
        if self.speed > 0 :
            ## Each images alternate every 20 frames
            if self.animation_time < 20 :
                self.image = self.bunny_walk1_r 
                self.animation_time += 1
            elif self.animation_time < 40 :
                self.animation_time += 1
                self.image = self.bunny_walk2_r
            else :
                self.animation_time = 0

        elif self.speed == 0 :
            self.image = self.bunny_stand
            self.animation_time = 0

        elif self.speed < 0 :
            ## Each images alternate every 20 frames
            if self.animation_time < 20: 
                self.image = self.bunny_walk1_l
                self.animation_time += 1
            elif self.animation_time < 40 :
                self.animation_time += 1
                self.image = self.bunny_walk2_l
            else :
                self.animation_time = 0

        if self.imunne == True :
            if self.imunne_time < 5 :
                all_game_sprites.add(self)
            elif self.imunne_time < 10 :
                all_game_sprites.remove(self)
            elif self.imunne_time < 15 :
                all_game_sprites.add(self)
            else :
                self.imunne_time = 0
                self.count += 1
                if self.count*15 >= self.imunne_time_base :
                    self.imunne = False
                    self.count = 0
            self.imunne_time += 1

        ## Update player position
        self.rect.x += self.speed

########## DISPLAY PLAYER'S LIFE ##########

    def creat_life(self) :
        ## Create a new sprite group
        self.life_sprite = pygame.sprite.Group()
        
        ## Define heart's table sprite 
        self.heart = {}

        ## Add number of heart 
        for i in range(self.life) :
            i += 1
            self.heart[i] = Heart()
            self.heart[i].rect.y = 10
            self.heart[i].rect.x = 10*i + 50*(i - 1) 
        
            self.life_sprite.add(self.heart[i])

    def display_life(self, screen) :
        ## Display hearts
        self.creat_life()
        self.life_sprite.draw(screen)

    def lose_life(self) :
        if self.imunne != True :
            ## Remove a life ad calculate if the player is death
            self.life -= 1
            self.life_sprite.empty()
            self.imunne = True
        
        if self.life < 0 :
            return True
        else :
            return False


    def colide_enemie(self, enemie_list, groups) :
        
        value = False
        ## Detect rect colisions between player and ground block
        enemie_player_list = pygame.sprite.spritecollide(self, enemie_list, True)
        ## If a rect colision is detected
        if enemie_player_list != [] :
            ## For each enemies in colision
            for enemie in enemie_player_list :
                ## If a bitmap colision is detected
                if pygame.sprite.collide_mask(self, enemie) != None :

                    ## If the player is enter into the block by the right side
                    if (self.rect.x + self.width) > (enemie.rect.x) and (self.rect.x + self.width) < (enemie.rect.x + enemie.width/2) :
                        ## Move the player out of the block
                        self.rect.x -= (5 + self.speed)
                    
                    ## If the player is enter into the block by the left side
                    elif (self.rect.x) < (enemie.rect.x + enemie.width) and (self.rect.x) > (enemie.rect.x + enemie.width - enemie.width/2) :
                        ## Move the player out of the block
                        self.rect.x += (5 - self.speed)
                    
                    if enemie.enemie_type == "spikeman" :
                        if pygame.sprite.collide_mask(self, enemie.spike) != None :
                            value = self.lose_life()
                    elif enemie.enemie_type == "flyman" :
                        value = self.lose_life()

                enemie_list.add(enemie)
                for group in groups :
                    group.add(enemie)
        return(value)

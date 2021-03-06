import pygame
from config import *
import math

class SpikeMan(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Import textures
        self.spikeman_stand = pygame.image.load("PNG/Enemies/spikeMan_stand.png").convert()
        self.spikeman_walk1_r = pygame.image.load("PNG/Enemies/spikeMan_walk1_r.png").convert()
        self.spikeman_walk2_r = pygame.image.load("PNG/Enemies/spikeMan_walk2_r.png").convert()
        self.spikeman_walk1_l = pygame.image.load("PNG/Enemies/spikeMan_walk1_l.png").convert()
        self.spikeman_walk2_l = pygame.image.load("PNG/Enemies/spikeMan_walk2_l.png").convert()

        ## Resize images
        self.spikeman_stand = pygame.transform.scale(self.spikeman_stand, [int(self.spikeman_stand.get_width()*self.conf.factor), int(self.spikeman_stand.get_height()*self.conf.factor)])
        self.spikeman_walk1_r = pygame.transform.scale(self.spikeman_walk1_r, [int(self.spikeman_walk1_r.get_width()*self.conf.factor), int(self.spikeman_walk1_r.get_height()*self.conf.factor)])
        self.spikeman_walk2_r = pygame.transform.scale(self.spikeman_walk2_r, [int(self.spikeman_walk2_r.get_width()*self.conf.factor), int(self.spikeman_walk2_r.get_height()*self.conf.factor)])
        self.spikeman_walk1_l = pygame.transform.scale(self.spikeman_walk1_l, [int(self.spikeman_walk1_l.get_width()*self.conf.factor), int(self.spikeman_walk1_l.get_height()*self.conf.factor)])
        self.spikeman_walk2_l = pygame.transform.scale(self.spikeman_walk2_l, [int(self.spikeman_walk2_l.get_width()*self.conf.factor), int(self.spikeman_walk2_l.get_height()*self.conf.factor)])

        ## Set texture background to transparent
        self.spikeman_stand.set_colorkey(Color.BLACK)
        self.spikeman_walk1_r.set_colorkey(Color.BLACK)
        self.spikeman_walk2_r.set_colorkey(Color.BLACK)
        self.spikeman_walk1_l.set_colorkey(Color.BLACK)
        self.spikeman_walk2_l.set_colorkey(Color.BLACK)
       
        ## Set texture
        self.image = self.spikeman_stand

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        ## Set beeing on ground value
        self.on_ground = False

        ## Set player speed base
        self.speed_base = 3*self.conf.xfactor
        self.speed = 0

        ## Set the ennemie parkour
        self.start_from_base = 0
        self.end_to_base = 0
        self.start_from = self.start_from_base
        self.end_to = self.end_to_base

        self.enemie_type = "spikeman"
        
        ## Set time to incremant animation
        self.animation_time = 0
        
        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32

        self.spike = SpikeManSpike()
        self.spike.rect.x = self.rect.x
        self.spike.rect.y = self.rect.y

########## GRAVITY FUNCTION ##########

    def gravity(self, block_list, movable_list, all_game_sprites_list, power):
        self.rect.y += 1
        ## Detect rect colisions between player and ground blocks
        block_player_list = pygame.sprite.spritecollide(self, block_list, True)
        if block_player_list != [] :
            for block in block_player_list :
                ## Detect bitmap colisions between player and ground block
                if pygame.sprite.collide_mask(self, block) != None :
                    ## Set player state to "on ground"
                    self.on_ground = True
            
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
        else : 
            self.rect.y = block.rect.y - self.height


    def update(self) :
        
        ## Player animation
        if self.speed > 0 :
            ## Each images alternate every 20 frames
            if self.animation_time < 20 :
                self.image = self.spikeman_walk1_r 
                self.animation_time += 1
            elif self.animation_time < 40 :
                self.animation_time += 1
                self.image = self.spikeman_walk2_r
            else :
                self.animation_time = 0

        elif self.speed == 0 :
            self.image = self.spikeman_stand
            self.animation_time = 0

        elif self.speed < 0 :
            ## Each images alternate every 20 frames
            if self.animation_time < 20: 
                self.image = self.spikeman_walk1_l
                self.animation_time += 1
            elif self.animation_time < 40 :
                self.animation_time += 1
                self.image = self.spikeman_walk2_l
            else :
                self.animation_time = 0

        ## Update player position
        if (self.rect.x + self.width) >= self.end_to :

            self.speed = -(self.speed_base/2)
            self.rect.x = self.end_to - self.width

        elif self.rect.x <= self.start_from :

            self.speed = self.speed_base
            self.rect.x = self.start_from

        self.rect.x += self.speed
        


        self.spike.rect.x = self.rect.x
        self.spike.rect.y = self.rect.y
        
class SpikeManSpike(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Import textures
        self.spikeman_spike = pygame.image.load("PNG/Enemies/spikeMan_spike.png").convert()

        ## Resize images
        self.spikeman_spike = pygame.transform.scale(self.spikeman_spike, [int(self.spikeman_spike.get_width()*self.conf.factor), int(self.spikeman_spike.get_height()*self.conf.factor)])
        ## Set texture background to transparent
        self.spikeman_spike.set_colorkey(Color.BLACK)
       
        ## Set texture
        self.image = self.spikeman_spike

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        ## Set player speed base
        self.speed_base = 4*self.conf.xfactor
        self.speed = 0

        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32


class FlyMan(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Import textures
        self.flyman_stand = pygame.image.load("PNG/Enemies/flyMan_stand.png").convert()
        self.flyman_fly = pygame.image.load("PNG/Enemies/flyMan_fly.png").convert()
        self.flyman_jump = pygame.image.load("PNG/Enemies/flyMan_jump.png").convert()

        ## Resize images
        self.flyman_stand = pygame.transform.scale(self.flyman_stand, [int(self.flyman_stand.get_width()*self.conf.factor), int(self.flyman_stand.get_height()*self.conf.factor)])
        self.flyman_fly = pygame.transform.scale(self.flyman_fly, [int(self.flyman_fly.get_width()*self.conf.factor), int(self.flyman_fly.get_height()*self.conf.factor)])
        self.flyman_jump = pygame.transform.scale(self.flyman_jump, [int(self.flyman_jump.get_width()*self.conf.factor), int(self.flyman_jump.get_height()*self.conf.factor)])

        ## Set texture background to transparent
        self.flyman_stand.set_colorkey(Color.BLACK)
        self.flyman_fly.set_colorkey(Color.BLACK)
        self.flyman_jump.set_colorkey(Color.BLACK)
       
        ## Set texture
        self.image = self.flyman_stand

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        ## Set player speed base
        self.speed_base = 3*self.conf.xfactor
        self.speed = 0

        ## Set player amplitude
        self.amplitude = 100
        self.period = 100
        self.y_velocity = 0
        self.before = 0

        self.enemie_type = "flyman"

        ## Set the ennemie parkour
        self.start_from_base = 0
        self.end_to_base = 0
        self.start_from = self.start_from_base
        self.end_to = self.end_to_base

        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32

    def update(self) :
        
        ## Player animation
        if self.y_velocity < self.before :
            ## Each images alternate every 20 frames
            self.image = self.flyman_fly 

        elif self.y_velocity == self.before :
            self.image = self.flyman_stand

        elif self.y_velocity > self.before :
            self.image = self.flyman_jump

        i = self.rect.x - self.start_from
        self.before = self.y_velocity
        self.y_velocity = self.amplitude*math.sin(1/self.period*math.pi*i)

        try :
            self.rect.y = self.y_base + self.y_velocity
        except :
            self.y_base = self.rect.y

        ## Update player position
        if (self.rect.x + self.width) >= self.end_to :

            self.speed = -(self.speed_base/2)
            self.rect.x = self.end_to - self.width

        elif self.rect.x < self.start_from :

            self.speed = self.speed_base
            self.rect.x = self.start_from

        self.rect.x += self.speed
        
class Cloud(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Import textures
        self.cloud = pygame.image.load("PNG/Enemies/cloud.png").convert()

        ## Resize images
        self.cloud = pygame.transform.scale(self.cloud, [int(self.cloud.get_width()*self.conf.factor), int(self.cloud.get_height()*self.conf.factor)])

        ## Set texture background to transparent
        self.cloud.set_colorkey(Color.BLACK)
       
        ## Set texture
        self.image = self.cloud

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        ## Set beeing on ground value
        self.on_ground = False

        ## Set player speed base
        self.speed_base = 3*self.conf.xfactor
        self.speed = -(self.speed_base)

        self.spawntime = 1200
        self.spawncount = 0

        ## Set the ennemie parkour
        self.start_from_base = 0
        self.end_to_base = 0
        self.start_from = self.start_from_base
        self.end_to = self.end_to_base

        self.enemie_type = "cloud"
        
        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32

    def spawn(self, groups) :

        if self.spawncount == 0 :
            spikeball = SpikeBall()

            if self.end_to < self.rect.x - self.width/2 :
                spikeball.speed_base = -5*self.conf.xfactor
            elif self.end_to > self.rect.x - self.width/2 :
                spikeball.speed_base = 5*self.conf.xfactor

            spikeball.rect.x = self.rect.x + self.width/4
            spikeball.rect.y = self.rect.y + self.height/2

            for group in groups :
                group.add(spikeball)

        self.spawncount += 1

        if self.spawncount >= self.spawntime :
            self.spawncount = 0

class SpikeBall(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Import textures
        self.spikeball_1 = pygame.image.load("PNG/Enemies/spikeBall_1.png").convert()
        self.spikeball_2 = pygame.image.load("PNG/Enemies/spikeBall_2.png").convert()

        ## Resize images
        self.spikeball_1 = pygame.transform.scale(self.spikeball_1, [int(self.spikeball_1.get_width()*self.conf.factor), int(self.spikeball_1.get_height()*self.conf.factor)])
        self.spikeball_2 = pygame.transform.scale(self.spikeball_2, [int(self.spikeball_2.get_width()*self.conf.factor), int(self.spikeball_2.get_height()*self.conf.factor)])

        ## Set texture background to transparent
        self.spikeball_1.set_colorkey(Color.BLACK)
        self.spikeball_2.set_colorkey(Color.BLACK)
       
        ## Set texture
        self.image = self.spikeball_1

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        ## Set beeing on ground value
        self.on_ground = False

        ## Set player speed base
        self.speed_base = 5*self.conf.xfactor
        self.speed = 0

        ## Set the ennemie parkour
        self.start_from_base = 0
        self.end_to_base = 0
        self.start_from = self.start_from_base
        self.end_to = self.end_to_base

        self.enemie_type = "spikeball"
        
        ## Set time to incremant animation
        self.animation_time = 0
        
        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32

########## GRAVITY FUNCTION ##########

    def gravity(self, block_list, movable_list, all_game_sprites_list, power):
        self.rect.y += 1
        ## Detect rect colisions between player and ground blocks
        block_player_list = pygame.sprite.spritecollide(self, block_list, True)
        if block_player_list != [] :
            self.speed = self.speed_base/2
            for block in block_player_list :
                ## Detect bitmap colisions between player and ground block
                if pygame.sprite.collide_mask(self, block) != None :
                    ## Set player state to "on ground"
                    self.on_ground = True
            
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
        else : 
            self.rect.y = block.rect.y - self.height


    def update(self) :
        
        ## Player animation
        if self.speed != 0 :
            ## Each images alternate every 10 frames
            if self.animation_time < 10 :
                self.image = self.spikeball_1 
                self.animation_time += 1
            elif self.animation_time < 20 :
                self.animation_time += 1
                self.image = self.spikeball_2
            else :
                self.animation_time = 0

        elif self.speed == 0 :
            self.image = self.spikeball_1
            self.animation_time = 0

        ### Update player position
        #if (self.rect.x + self.width) >= self.end_to :

        #    self.speed = -(self.speed_base/2)
        #    self.rect.x = self.end_to - self.width

        #elif self.rect.x <= self.start_from :

        #    self.speed = self.speed_base
        #    self.rect.x = self.start_from

        self.rect.x += self.speed


class WingMan(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        self.conf = Config()

        ## Import textures
        self.wingman_1 = pygame.image.load("PNG/Enemies/wingMan1.png").convert()
        self.wingman_2 = pygame.image.load("PNG/Enemies/wingMan2.png").convert()
        self.wingman_3 = pygame.image.load("PNG/Enemies/wingMan3.png").convert()
        self.wingman_4 = pygame.image.load("PNG/Enemies/wingMan4.png").convert()
        self.wingman_5 = pygame.image.load("PNG/Enemies/wingMan5.png").convert()

        ## Resize images
        self.wingman_1 = pygame.transform.scale(self.wingman_1, [int(self.wingman_1.get_width()*self.conf.factor), int(self.wingman_1.get_height()*self.conf.factor)])
        self.wingman_2 = pygame.transform.scale(self.wingman_2, [int(self.wingman_2.get_width()*self.conf.factor), int(self.wingman_2.get_height()*self.conf.factor)])
        self.wingman_3 = pygame.transform.scale(self.wingman_3, [int(self.wingman_3.get_width()*self.conf.factor), int(self.wingman_3.get_height()*self.conf.factor)])
        self.wingman_4 = pygame.transform.scale(self.wingman_4, [int(self.wingman_4.get_width()*self.conf.factor), int(self.wingman_4.get_height()*self.conf.factor)])
        self.wingman_5 = pygame.transform.scale(self.wingman_5, [int(self.wingman_5.get_width()*self.conf.factor), int(self.wingman_5.get_height()*self.conf.factor)])

        ## Set texture background to transparent
        self.wingman_1.set_colorkey(Color.BLACK)
        self.wingman_2.set_colorkey(Color.BLACK)
        self.wingman_3.set_colorkey(Color.BLACK)
        self.wingman_4.set_colorkey(Color.BLACK)
        self.wingman_5.set_colorkey(Color.BLACK)
       
        ## Set texture
        self.image = self.wingman_1

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)
        
        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        ## Set player speed base
        self.speed_base = 3*self.conf.xfactor
        self.speed = 1

        ## Set the ennemie parkour
        self.start_from_base = 0
        self.end_to_base = 0
        self.start_from = self.start_from_base
        self.end_to = self.end_to_base

        self.enemie_type = "wingman"
        
        ## Set time to incremant animation
        self.animation_time = 0
        
        ## Set player default position
        self.rect.y = 1080 - 32 - 94 - self.height
        self.rect.x = 32

    def update(self) :
        
        ## Player animation
        if self.animation_time < 10 :
            self.image = self.wingman_2 
        elif self.animation_time < 20 :
            self.image = self.wingman_3
        elif self.animation_time < 30 :
            self.image = self.wingman_1
        elif self.animation_time < 40: 
            self.image = self.wingman_4
        elif self.animation_time < 50 :
            self.image = self.wingman_5
        else :
            self.animation_time = 0

        self.animation_time += 1

        ## Update player position
        if self.rect.y <= self.end_to :

            self.speed = self.speed_base
            #self.rect.y = self.end_to

        elif self.rect.y >= self.start_from :

            self.speed = -(self.speed_base/2)
            #self.rect.y = self.start_from

        self.rect.y += self.speed


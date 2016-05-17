from config import *
from color import *
import pygame

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, ground_type):
        ## Call the parent class (Sprite) constructor
        super().__init__()
        ## Load config file
        conf = Config()

        ## Import picture
        if ground_type == "grass" :
            self.image = pygame.image.load("PNG/Environment/ground_grass.png").convert()
        elif ground_type == "small_grass" :
            self.image = pygame.image.load("PNG/Environment/ground_grass_small.png").convert()
        elif ground_type == "broken_grass" :
            self.image = pygame.image.load("PNG/Environment/ground_grass_broken.png").convert()
        elif ground_type == "small_broken_grass" :
            self.image = pygame.image.load("PNG/Environment/ground_grass_small_broken.png").convert()
        elif ground_type == "stone" :
            self.image = pygame.image.load("PNG/Environment/ground_stone.png").convert()
        elif ground_type == "small_stone" :
            self.image = pygame.image.load("PNG/Environment/ground_stone_small.png").convert()
        elif ground_type == "broken_stone" :
            self.image = pygame.image.load("PNG/Environment/ground_stone_broken.png").convert()
        elif ground_type == "small_broken_stone" :
            self.image = pygame.image.load("PNG/Environment/ground_stone_small_broken.png").convert()
        elif ground_type == "cake" :
            self.image = pygame.image.load("PNG/Environment/ground_cake.png").convert()
        elif ground_type == "small_cake" :
            self.image = pygame.image.load("PNG/Environment/ground_cake_small.png").convert()
        elif ground_type == "broken_cake" :
            self.image = pygame.image.load("PNG/Environment/ground_cake_broken.png").convert()
        elif ground_type == "small_broken_cake" :
            self.image = pygame.image.load("PNG/Environment/ground_cake_small_broken.png").convert()
        elif ground_type == "snow" :
            self.image = pygame.image.load("PNG/Environment/ground_snow.png").convert()
        elif ground_type == "small_snow" :
            self.image = pygame.image.load("PNG/Environment/ground_snow_small.png").convert()
        elif ground_type == "broken_snow" :
            self.image = pygame.image.load("PNG/Environment/ground_snow_broken.png").convert()
        elif ground_type == "small_broken_snow" :
            self.image = pygame.image.load("PNG/Environment/ground_snow_small_broken.png").convert()
        elif ground_type == "sand" :
            self.image = pygame.image.load("PNG/Environment/ground_sand.png").convert()
        elif ground_type == "small_sand" :
            self.image = pygame.image.load("PNG/Environment/ground_sand_small.png").convert()
        elif ground_type == "broken_sand" :
            self.image = pygame.image.load("PNG/Environment/ground_sand_broken.png").convert()
        elif ground_type == "small_broken_sand" :
            self.image = pygame.image.load("PNG/Environment/ground_sand_small_broken.png").convert()
        elif ground_type == "wood" :
            self.image = pygame.image.load("PNG/Environment/ground_wood.png").convert()
        elif ground_type == "small_wood" :
            self.image = pygame.image.load("PNG/Environment/ground_wood_small.png").convert()
        elif ground_type == "broken_wood" :
            self.image = pygame.image.load("PNG/Environment/ground_wood_broken.png").convert()
        elif ground_type == "small_broken_wood" :
            self.image = pygame.image.load("PNG/Environment/ground_wood_small_broken.png").convert()
        else :
            print("Valid blocks types :\r\n    grass\r\n    small_grass\r\n    broken_grass\r\n    small_broken_grass\r\n    stone\r\n    small_stone\r\n    broken_stone")
            print("    small_broken_stone\r\n    cake\r\n    small_cake\r\n    broken_cake\r\n    small_broken_cake\r\n    snow\r\n    small_snow\r\n    broken_snow")
            print("    small_broken_snow\r\n    sand\r\n    small_sand\r\n    broken_sand\r\n    small_broken_sand\r\n    wood\r\n    small_wood\r\n    broken_wood")
            print("    small_broken_wood")

        self.image = pygame.transform.scale(self.image, [int(self.image.get_width()*conf.factor), int(self.image.get_height()*conf.factor)])

        ## Set the background to transparent
        self.image.set_colorkey(Color.BLACK)

        self.mask = pygame.mask.from_surface(self.image)

        ## Get sprite position
        self.rect = self.image.get_rect()
        
        ## Set ground type
        self.ground_type = ground_type

        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect.y = 1080 - 16 - 94
        self.rect.x = 32


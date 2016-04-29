from color import *
from config import *
import pygame

class Ground(pygame.sprite.Sprite):
    
    def __init__(self):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        ## Import picture
        self.image = pygame.image.load("PNG/Environment/ground_grass.png").convert()
        ## Set the background to transparent
        self.image.set_colorkey(Color.BLACK)

        self.mask = pygame.mask.from_surface(self.image)

        ## Get sprite position
        self.rect = self.image.get_rect()
        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.y = Config.height - 16 - 94
        self.rect.x = 32

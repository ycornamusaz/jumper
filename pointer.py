from color import *
from config import *
import pygame

class Pointer(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        ## Create a surface of 1x1 px
        self.image = pygame.image.load("PNG/cursor.png").convert()

        ## Set color to white
        self.image.set_colorkey(Color.WHITE)

        ## Define colide mask
        self.mask = pygame.mask.from_surface(self.image)

        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Set default sprite position
        self.rect.x = 0
        self.rect.y = 0

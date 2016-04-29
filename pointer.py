from color import *
from config import *
import pygame

class Pointer(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        ## Create a surface of 1x1 px
        self.image = pygame.Surface((1, 1))

        ## Set color to white
        self.image.fill(Color.WHITE)

        ## Get sprite position
        self.rect = self.image.get_rect()

        ## Set default sprite position
        self.rect.x = 1
        self.rect.y = 1
        self.mask = pygame.mask.from_surface(self.image)

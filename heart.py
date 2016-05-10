from color import *
import pygame


class Heart(pygame.sprite.Sprite) :
    def __init__(self) :
        super().__init__()
        
        ## Define sprite image
        self.image = pygame.image.load("PNG/heart.png").convert()

        ## Enable transparent
        self.image.set_colorkey(Color.WHITE)

        ## Get sprite position
        self.rect = self.image.get_rect()
        
        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()

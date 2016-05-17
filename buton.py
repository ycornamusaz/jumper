from color import *
from config import *
import pygame

class Buton(pygame.sprite.Sprite):

    def __init__(self, text, color_txt):
        ## Call the parent class (Sprite) constructor
        super().__init__()
        
        ## Load config file
        self.conf = Config()

        ## Import picture
        self.image_1 = pygame.image.load("PNG/Environment/ground_grass.png").convert()
        
        ## Resize imgage to fit with the screen resolution
        self.image_1 = pygame.transform.scale(self.image_1, [int(self.image_1.get_width()*self.conf.factor), int(self.image_1.get_height()*self.conf.factor)])
        self.image = pygame.Surface([self.image_1.get_width(),self.image_1.get_height()])

        ## Set the background to transparent
        self.image.set_colorkey(Color.BLACK)

        ## Get sprite position
        self.rect = self.image.get_rect()
        
        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = (self.conf.width/2 - self.width/2)
        self.rect.y = 32

        self.update(text, color_txt)

        ## Set mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, text, color_txt):

        ## Update text
        self.text = text
        ## Update text color
        self.color = color_txt
        ## Set font and font size
        self.font = pygame.font.SysFont("Ubuntu", int(25*self.conf.factor))
        ## Creat text object
        self.textSurf = self.font.render(self.text, 1, self.color)
        ## Get the text object width and height
        self.text_width = self.textSurf.get_width()
        self.text_height = self.textSurf.get_height()
        ## Fuse text object with the buton
        self.image.blit(self.image_1, [0,0])
        self.image.blit(self.textSurf, [(self.width/2 - self.text_width/2), (self.height/2 - self.text_height/2)])




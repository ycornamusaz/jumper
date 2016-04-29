from color import *
from config import *
import pygame

class Buton(pygame.sprite.Sprite):

    def __init__(self, text, color_txt):
        ## Call the parent class (Sprite) constructor
        super().__init__()

        ## Import picrure
        self.image_1 = pygame.image.load("PNG/Environment/ground_grass.png").convert()

        self.image = pygame.Surface([self.image_1.get_width(),self.image_1.get_height()])

        ## Set the background to transparent
        self.image.set_colorkey(Color.BLACK)

        ## Get sprite position
        self.rect = self.image.get_rect()
        
        ## Get sprite width and height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = (Config.width/2 - self.width/2)
        self.rect.y = 32

        ## Set text content
        self.text = text
        ## Set text color
        self.color = color_txt
        ## Set font and font size
        self.font = pygame.font.SysFont("Ubuntu", 25)
        ## Creat text object
        self.textSurf = self.font.render(self.text, 1, self.color)
        ## Get the text object width and height
        self.text_width = self.textSurf.get_width()
        self.text_height = self.textSurf.get_height()
        ## Fuse text object with the buton
        self.image.blit(self.image_1,[0,0])
        self.image.blit(self.textSurf, [(self.width/2 - self.text_width/2), (self.height/2 - self.text_height/2)])

    def update(self, text, color_txt):

        ## Update text
        self.text = text
        ## Update text color
        self.color = color_txt
        ## Set font and font size
        self.font = pygame.font.SysFont("Ubuntu", 25)
        ## Creat text object
        self.textSurf = self.font.render(self.text, 1, self.color)
        ## Get the text object width and height
        self.text_width = self.textSurf.get_width()
        self.text_height = self.textSurf.get_height()
        ## Fuse text object with the buton
        self.image.blit(self.image_1, [0,0])
        self.image.blit(self.textSurf, [(self.width/2 - self.text_width/2), (self.height/2 - self.text_height/2)])

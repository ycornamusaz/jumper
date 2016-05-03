from color import *
from config import *
import pygame

class Background() :
    def __init__(self) :

        ## Import background pictures (don't convert picture to pygame format to keep transarence)
        self.bg1_base = pygame.image.load("PNG/Background/bg_layer1.png")
        self.bg2_base = pygame.image.load("PNG/Background/bg_layer2.png")
        self.bg3_base = pygame.image.load("PNG/Background/bg_layer3.png")
        self.bg4_base = pygame.image.load("PNG/Background/bg_layer4.png")
        self.bg_game_over = pygame.image.load("PNG/Background/red.png")

        ## Creat background surface
        self.bg = pygame.Surface([Config.width, Config.height])

        ## Resize background picturesd
        self.bg1 = pygame.transform.scale(self.bg1_base, (Config.width, Config.height))
        self.bg2 = pygame.transform.scale(self.bg2_base, (Config.width, Config.height))
        self.bg3 = pygame.transform.scale(self.bg3_base, (Config.width, Config.height))
        self.bg4 = pygame.transform.scale(self.bg4_base, (Config.width, Config.height))
        self.bg_game_over = pygame.transform.scale(self.bg_game_over, (Config.width, Config.height))

        ## Fuse background onto background surface
        self.reset()

    def update(self, screen) :

        ## Print background on screen
        screen.blit(self.bg, [0, 0])

    def game_over(self) :
        
        ## Add red filter to background
        self.bg.blit(self.bg_game_over, [0, 0])

    def reset(self) :
        
        ## Fuse background onto background surface
        self.bg.blit(self.bg1, [0, 0])
        self.bg.blit(self.bg2, [0, 0])
        self.bg.blit(self.bg3, [0, 0])
        self.bg.blit(self.bg4, [0, 0])


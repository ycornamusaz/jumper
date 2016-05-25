import yaml
import pygame 
from player import *


class Config() :
    ## Define screen size
    width_base = 1800
    height_base = 1000

    def __init__(self) :
        
        ## Load config file
        with open("config.yaml") as config_data :
            self.config_data = yaml.load(config_data)
        
        ## Read and set width, height and amplification factor
        self.width = self.config_data["Config"]["Screen"]["width"]
        self.height = self.config_data["Config"]["Screen"]["height"]
        if self.config_data["Config"]["Screen"]["width"] < self.config_data["Config"]["Screen"]["height"] :
            self.factor = self.width/self.width_base
        else :
            self.factor = self.height/self.height_base
        self.xfactor = self.width/self.width_base

    ## Return config file var
    def get_config_data(self) :

        ## Load config file
        with open("config.yaml") as config_data :
            self.config_data = yaml.load(config_data)
        
        return self.config_data

########## GET SCREEN METHODE ##########

    def get_screen(self) :

        ## FULLSCREEN
        if self.config_data["Config"]["Screen"]["state"] == 'FULLSCREEN' :
            
            return pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        
        elif self.config_data["Config"]["Screen"]["state"] == 'WINDOWED' :

            return pygame.HWSURFACE | pygame.DOUBLEBUF

        ## If the entry is not reconise
        else :
            
            ## Return the value
            return eval(self.config_data["Config"]["Screen"]["state"])


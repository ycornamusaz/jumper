import yaml
import pygame 
from player import *


class Config() :
    ## Define screen size
    width_base = 1800
    height_base = 1000

    def __init__(self) :
        
        with open("config.yaml") as config_data :
            self.config_data = yaml.load(config_data)

        self.width = self.config_data["Config"]["Screen"]["width"]
        self.height = self.config_data["Config"]["Screen"]["height"]
        self.factor = self.width/self.width_base

    def get_config_data(self) :

        return self.config_data

    def get_screen(self) :

        if self.config_data["Config"]["Screen"]["state"] == 'FULLSCREEN' :
            
            return pygame.FULLSCREEN
        
        elif self.config_data["Config"]["Screen"]["state"] == 'OPENGL' :
            
            return pygame.OPENGL

        elif self.config_data["Config"]["Screen"]["state"] == 'HWSURFACE' :

            return pygame.HWSURFACE

        else :
            
            return eval(self.config_data["Config"]["Screen"]["state"])

    def conf_players(self, players, groups) :
        i = 0
        player = {}
        for i in range(self.config_data["Config"]["Players"]["number"]) :
            player[i] = Player(self.config_data["Config"]["Players"]["Sex"][i]["sex"])
            player[i].key_up = eval("pygame." + self.config_data["Config"]["Players"]["Keys"][i]["up"])
            player[i].key_right = eval("pygame." + self.config_data["Config"]["Players"]["Keys"][i]["right"])
            player[i].key_left = eval("pygame." + self.config_data["Config"]["Players"]["Keys"][i]["left"])
            players.add(player[i])
            player[i].creat_life()
            for group in groups :
                group.add(player[i])

        return player


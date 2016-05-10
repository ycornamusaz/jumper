import yaml
import pygame 
from player import *
from ground import Ground


class Config() :
    ## Define screen size
    width = 1200
    height = 1000

    def __init__(self, config_file) :
        
        with open(config_file) as config_data :
            self.config_data = yaml.load(config_data)

        with open(self.config_data["Config"]["Map"]["file"]) as map_data :
            self.map_data = yaml.load(map_data)

        self.shift = 0

    def gen_blocks(self, players, groups) :
        
        for ground_type in self.map_data["Levels"][0]["Blocks"] :
            i = 0
            for x, y in self.map_data["Levels"][0]["Blocks"][ground_type] :
                x = self.map_data["Levels"][0]["Blocks"][ground_type][i]["x"]
                y = self.map_data["Levels"][0]["Blocks"][ground_type][i]["y"]
                ground0 = Ground(ground_type)
                ground0.rect.x = x
                ground0.rect.y = y

                for player in players :
                    player.last_block_colide = ground0
                    player.rect.x = self.map_data["Levels"][0]["Player"]["x"]
                    player.rect.y = self.map_data["Levels"][0]["Player"]["y"]

                for group in groups :
                    group.add(ground0)
                i += 1

    def gen_players(self, players, groups) :
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

    def reset_level(self, player, liste) :
        for entity in liste :
            entity.rect.x -= self.shift
            player.rect.x = self.map_data["Levels"][0]["Player"]["x"]
            player.rect.y = self.map_data["Levels"][0]["Player"]["y"]
            player.on_ground = False

        self.shift = 0

    def move_map(self, player, liste) : 
        if (player.rect.x + player.width) > (Config.width - Config.width/3) :
            for entity in liste :
                entity.rect.x -= 5
            self.shift -= 5
        if player.rect.x < (Config.width/16) :
            for entity in liste :
                entity.rect.x += 5
            self.shift += 5


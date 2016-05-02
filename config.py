import yaml
from ground import *

class Config() :
    ## Define screen size
    width = 1200
    height = 1000

    def __init__(self, config_file) :
        
        with open(config_file) as config_data :
            self.config_data = yaml.load(config_data)

        with open(self.config_data["Config"]["Map"]["file"]) as map_data :
            self.map_data = yaml.load(map_data)

    def gen_map(self, players, groups) :
        
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

                for group in groups :
                    group.add(ground0)
                i += 1

from ground import *
from config import *
from pygame import *
from player import *
from buton import *
from heart import *
from pointer import *

class Engine() :

    def __init__(self) :

        self.conf = Config()

        ## Get the config var file
        self.config_data = self.conf.get_config_data()
        
        ## Open the map configuration file
        with open(self.config_data["Config"]["Map"]["file"]) as map_data :
            self.map_data = yaml.load(map_data)
        
        ## Set the shift of the map
        self.shift = 0

########## CREATE AND CONFIGURE PLAYERS ##########

    def conf_players(self, players, groups) :
        i = 0

        ## Define players table
        player = {}

        ## For the number of player
        for i in range(self.config_data["Config"]["Players"]["number"]) :
            
            ## Create player
            player[i] = Player(self.config_data["Config"]["Players"]["Sex"][i]["sex"])
            
            ## Set keyboard controls
            player[i].key_up = eval("pygame." + self.config_data["Config"]["Players"]["Keys"][i]["up"])
            player[i].key_right = eval("pygame." + self.config_data["Config"]["Players"]["Keys"][i]["right"])
            player[i].key_left = eval("pygame." + self.config_data["Config"]["Players"]["Keys"][i]["left"])
            
            ## Add player to players group
            players.add(player[i])

            ## Init player's life
            player[i].creat_life()

            ## Add player in each groups
            for group in groups :
                group.add(player[i])

        return player

########## CREATE, CONFIGURE BLOCKS AND DEFAULT PLAYER POSITION  ##########

    def gen_blocks(self, players, groups) :

        ## For each block types
        for ground_type in self.map_data["Levels"][0]["Blocks"] :
            i = 0

            ## For each blocks
            for x, y in self.map_data["Levels"][0]["Blocks"][ground_type] :

                ## Read x and y axes
                x = self.map_data["Levels"][0]["Blocks"][ground_type][i]["x"]*self.conf.factor
                y = (1000 - self.map_data["Levels"][0]["Blocks"][ground_type][i]["y"])*self.conf.factor
                
                ## Create block
                ground0 = Ground(ground_type)

                ## Set x and y position
                ground0.rect.x = x
                ground0.rect.y = y

                ## For each players
                for player in players :

                    ## Define the block to the player last touch block
                    player.last_block_colide = ground0

                    ## Set the player position
                    player.rect.x = self.map_data["Levels"][0]["Player"]["x"]*self.conf.factor
                    player.rect.y = (1000 - self.map_data["Levels"][0]["Player"]["y"])*self.conf.factor

                ## For each groups 
                for group in groups :
                    ## Add the block to the group
                    group.add(ground0)

                i += 1

########## RESET MAP PROCESS ##########

    def reset_level(self, player, liste) :

        ## For each entities who were shifed
        for entity in liste :

            ## Reset the entitie position
            entity.rect.x -= self.shift

            ## Reset the player position
            player.rect.x = self.map_data["Levels"][0]["Player"]["x"]*self.conf.factor
            player.rect.y = (1000 - self.map_data["Levels"][0]["Player"]["y"])*self.conf.factor

            ## Set the player state to "not on the ground"
            player.on_ground = False

        ## Reset shift
        self.shift = 0

########## MAP SHIFT ##########

    def move_map(self, player, liste) : 

        ## If the player is at 1/3 of je screen on the right side
        if (player.rect.x + player.width) > (self.conf.width - self.conf.width/3) :
            
            ## Shift all the entities to the left
            for entity in liste :
                entity.rect.x -= 5
            self.shift -= 5

        ## If the player is at 1/16 of je screen on the left side
        if player.rect.x < (self.conf.width/16) :

            ## Shift all the entities to the right
            for entity in liste :
                entity.rect.x += 5
            self.shift += 5


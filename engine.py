import pygame
import re
import ast
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

########## BUTON UPDATE ##########

    def update_selected_buton(self, buton_list, pointer, groups) :

        ## Detect rect colision between pointer and buton group
        buton_pointer_list = pygame.sprite.spritecollide(pointer, buton_list, True)
        
        ## If a rect colision is detected
        if buton_pointer_list != [] : 
            ## For each buton who are in colision with pointer
            for buton in buton_pointer_list :
                if pygame.sprite.collide_mask(pointer, buton) != None :
                    ## Update text Color to red
                    if buton.color != Color.RED :
                        buton.update(buton.text , Color.RED)
                else :
                    ## Update text Color to white
                    if buton.color != Color.WHITE :
                        buton.update(buton.text, Color.WHITE)

                ## Re-add buton to sprite list
                for group in groups :
                    group.add(buton)
        else :
            for buton in buton_list :
                ## Update text Color to white
                if buton.color != Color.WHITE :
                    buton.update(buton.text, Color.WHITE)


    def get_pressed_buton(self, buton_list, pointer, groups) :
        
        buton_pointer_list = pygame.sprite.spritecollide(pointer, buton_list, True)
        for buton in buton_pointer_list :
            if pygame.sprite.collide_mask(pointer, buton) != None :
                buton_text = buton.text
                for group in groups :
                    group.add(buton)
                return buton
            else :
                for group in groups :
                    group.add(buton)


    def set_ext_buton(self, buton, ext) :
        try :
            buton.ext = ext
            buton.text = buton.base_text + " " + buton.ext
            buton.update(buton.text, buton.color)
        
        except :
            buton.base_text = buton.text
            buton.ext = ext
            buton.text = buton.base_text + " " + buton.ext
            buton.update(buton.text, buton.color)

    def switch_resolution_buton(self, buton) :
        
        for i in range(len(self.config_data["Config"]["Screen"]["resolutions"])) :

            if buton.text.find(str(self.config_data["Config"]["Screen"]["resolutions"][i]["x"]) + "x" + str(self.config_data["Config"]["Screen"]["resolutions"][i]["y"])) != -1 :
                
                i += 1
                if i >= len(self.config_data["Config"]["Screen"]["resolutions"]) :
                    i = 0

                self.config_data["Config"]["Screen"]["width"] = self.config_data["Config"]["Screen"]["resolutions"][i]["x"]
                self.config_data["Config"]["Screen"]["height"] = self.config_data["Config"]["Screen"]["resolutions"][i]["y"]
                self.set_ext_buton(buton, (str(self.config_data["Config"]["Screen"]["width"]) + "x" + str(self.config_data["Config"]["Screen"]["height"])))
                break
        
        with open('config.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.config_data, default_flow_style=False))

    def switch_screen_format_buton(self, buton) :

        if self.config_data["Config"]["Screen"]["state"] == "FULLSCREEN" :
            self.set_ext_buton(buton, "WINDOWED")
            self.config_data["Config"]["Screen"]["state"] = "WINDOWED"
        elif self.config_data["Config"]["Screen"]["state"] == "WINDOWED" :
            self.set_ext_buton(buton, "FULLSCREEN")
            self.config_data["Config"]["Screen"]["state"] = "FULLSCREEN"

        with open('config.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.config_data, default_flow_style=False))

    def get_tick_speed(self) :
        if self.config_data["Config"]["dificulty"] == 0 :
            return 90
        elif self.config_data["Config"]["dificulty"] == 1 :
            return 120
        elif self.config_data["Config"]["dificulty"] == 2 :
            return 500

    def switch_dificulty_buton(self, buton) :

        if buton.text.find("Easy") != -1 :
            self.set_ext_buton(buton, "Medium")
            self.config_data["Config"]["dificulty"] = 1
        
        elif buton.text.find("Medium") != -1 :
            self.set_ext_buton(buton, "Hard")
            self.config_data["Config"]["dificulty"] = 2

        elif buton.text.find("Hard") != -1 :
            self.set_ext_buton(buton, "Easy")
            self.config_data["Config"]["dificulty"] = 0

        with open('config.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.config_data, default_flow_style=False))

    def get_dificulty(self) :

        if self.config_data["Config"]["dificulty"] == 0 :
            return "Easy"
        if self.config_data["Config"]["dificulty"] == 1 :
            return "Medium"
        if self.config_data["Config"]["dificulty"] == 2 :
            return "Hard"

    def switch_player_number_buton(self, buton) :

        if buton.text.find("1") != -1 :
            self.set_ext_buton(buton, "2")
            self.config_data["Config"]["Players"]["number"] = 2
        
        elif buton.text.find("2") != -1 :
            self.set_ext_buton(buton, "1")
            self.config_data["Config"]["Players"]["number"] = 1

        with open('config.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.config_data, default_flow_style=False))


    def switch_player_sex_buton(self, buton) :

        if buton.text.find("male") != -1 :
            self.config_data["Config"]["Players"]["Sex"][(self.config_data["Config"]["Players"]["number"] - 1)]["sex"] = "femal"
            self.set_ext_buton(buton, ( " " + str(self.config_data["Config"]["Players"]["number"]) + "'s sex " + self.config_data["Config"]["Players"]["Sex"][(self.config_data["Config"]["Players"]["number"] - 1)]["sex"] ))
        
        elif buton.text.find("femal") != -1 :
            self.config_data["Config"]["Players"]["Sex"][(self.config_data["Config"]["Players"]["number"] - 1)]["sex"] = "male"
            self.set_ext_buton(buton, ( " " + str(self.config_data["Config"]["Players"]["number"]) + "'s sex " + self.config_data["Config"]["Players"]["Sex"][(self.config_data["Config"]["Players"]["number"] - 1)]["sex"] ))

        with open('config.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.config_data, default_flow_style=False))

    def return_pressed_key(self, buton) :
        wait = True
        trace = re.compile('.*?(\\{.*?\\})')

        while wait :
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    string = trace.search(repr(event)).group(1)
                    key = ast.literal_eval(string)['unicode']
                    if key == '' :
                        if ast.literal_eval(string)['scancode'] == 113 :
                            out = "K_LEFT"
                        elif ast.literal_eval(string)['scancode'] == 114 :
                            out = "K_RIGHT"
                        elif ast.literal_eval(string)['scancode'] == 111 :
                            out = "K_UP"
                        elif ast.literal_eval(string)['scancode'] == 116 :
                            out = "K_DOWN"
                        elif ast.literal_eval(string)['scancode'] == 50 :
                            out = "K_LSHIFT"
                        elif ast.literal_eval(string)['scancode'] == 62 :
                            out = "K_RSHIFT"
                        elif ast.literal_eval(string)['scancode'] == 37 :
                            out = "K_LCTRL"
                        elif ast.literal_eval(string)['scancode'] == 105 :
                            out = "K_RCTRL"
                        elif ast.literal_eval(string)['scancode'] == 301 :
                            out = "K_CAPSLOCK"
                        else : 
                            out = None

                    elif key == '\t' :
                        out = "K_TAB"
                    elif key == ' ' :
                        out = "K_SPACE"
                    elif key == ',' :
                        out = "K_COMMA"
                    else :
                        out = "K_" + key

                    wait = False
        
        wait = True
        
        if buton.text.find("jump key") != -1 :
            self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["up"] = out
            self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " jump key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["up"])))
        elif buton.text.find("action key") != -1 :
            self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["action"] = out
            self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " action key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["action"])))
        elif buton.text.find("left key") != -1 :
            self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["left"] = out
            self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " left key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["left"])))
        
        elif buton.text.find("right key") != -1:
            self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["right"] = out
            self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " right key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["right"])))

        with open('config.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.config_data, default_flow_style=False))

    def update_player_menu(self, buton_list) :
        for buton in buton_list :
            if buton.text.find("Player") != -1 and buton.text.find("sex") != -1 :
                self.set_ext_buton(buton, ( " " + str(self.config_data["Config"]["Players"]["number"]) + "'s sex " + self.config_data["Config"]["Players"]["Sex"][(self.config_data["Config"]["Players"]["number"] - 1)]["sex"] ))

            elif buton.text.find("action key") != -1 :
                self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " action key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["action"])))

            elif buton.text.find("jump key") != -1 :
                self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " jump key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["up"])))

            elif buton.text.find("left key") != -1 :
                self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " left key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["left"])))

            elif buton.text.find("right key") != -1 :
                self.set_ext_buton(buton, (str(self.config_data["Config"]["Players"]["number"]) + " right key " + str(self.config_data["Config"]["Players"]["Keys"][(self.config_data["Config"]["Players"]["number"] - 1)]["right"])))

            else : 
                do = "nothing"

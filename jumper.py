#!/usr/bin/python3.4

import pygame
import yaml
import color
from player import *
from ground import *
from config import *
from buton import *
from pointer import *
from background import *
from engine import *

class Game :
    def menu():
        ## Init pygame
        pygame.init()
        ## Initialise external data configuration
        conf = Config()
        ## Create engine
        engine = Engine()
        ## Init screen
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen_mode())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!! - Menu")
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Init clock
        clock = pygame.time.Clock()
        ## Menu loop stat
        done_menu = False
        start_game = False
        start_options = False
        ## Set background
        background = Background()
        ## Create menu sprite group
        buton_list = pygame.sprite.Group()
        all_menu_sprites_list = pygame.sprite.Group()
        pointer_list = pygame.sprite.Group()
        ## Create pointer sprite
        pointer = Pointer()
        ## Add pointer to pointer's list
        pointer_list.add(pointer)
        ## Add pointer to menu sprite's group
        all_menu_sprites_list.add(pointer)
        ## Create butons
        buton1 = Buton("Play", Color.WHITE)
        buton2 = Buton("Options", Color.WHITE)
        buton3 = Buton("Quit", Color.WHITE)
        ## Set buton1 pos
        buton1.rect.x = (conf.width/2 - buton1.width/2)
        buton1.rect.y = (conf.height/2 - buton1.height/2 - 100)
        ## Set buton2 pos
        buton2.rect.x = (conf.width/3 - buton2.width/2)
        buton2.rect.y = (conf.height/2 - buton2.height/2 + 100)
        ## Set buton3 pos
        buton3.rect.x = (conf.width/3*2 - buton3.width/2)
        buton3.rect.y = (conf.height/2 - buton3.height/2 + 100)
        ## Add butons to buton list
        buton_list.add(buton1)
        buton_list.add(buton2)
        buton_list.add(buton3)
        ## Add butons to menu sprite's group
        all_menu_sprites_list.add(buton1)
        all_menu_sprites_list.add(buton2)
        all_menu_sprites_list.add(buton3)
    
        ## Start loop
        while not done_menu :
            
            ########## EVENT ZONE ##########
        
            ## For every events, filter event and refresh screen
            for event in pygame.event.get() :
        
                ## Filter events
                ## If the cross is pressed, quit game
                if event.type == pygame.QUIT :
                    done_menu = True
                ## If any mouse buton is pressed 
                if event.type == pygame.MOUSEBUTTONDOWN :
                    ## Detect if left mouse buton is pressed
                    if event.button == 1 :
                        
                        ## Detect and retourn the pressed buton
                        buton = engine.get_pressed_buton(buton_list, pointer, [all_menu_sprites_list, buton_list])
                        
                        ## If there's no buton pressed, do nothing
                        if buton == None :
                            do = "nothing"
                        
                        ## If play buton is pressed, launch the game
                        elif buton.text is "Play" :
                            start_game = True

                        ## If options buton is pressed, launch options menu
                        elif buton.text is "Options" :
                            start_options = True

                        ## If quit buton is pressed, quit the game
                        elif buton.text is "Quit" :
                            done_menu = True
                            
            ########## LOGIC CODE ZONE ##########
            
            ## Check for restarting the game
            while start_game == True :
                ## Launch game
                Game.game()
                ## One the player has gameover, launch gameover's screen
                start_game = Game.game_over()
            ## If the gameover menu return nothing, git the game
            if start_game == None :
                break
            ## If gameover menu return false, display main menu

            ## Check if option menu have to be launch
            if start_options == True :
                ## Launch option's menu
                restart = Game.options()

                ## Check if we have to restart the game
                if restart is True :
                    done_menu = True
                    return True
                
                ## Reset options menu start value
                start_options = False

            ## Update mouse pos
            pos = pygame.mouse.get_pos()
            pointer.rect.x = pos[0]
            pointer.rect.y = pos[1]

            ## Detect bitmap colision between butons and pointer
            engine.update_selected_buton(buton_list, pointer, [all_menu_sprites_list, buton_list])

            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the background
            background.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_menu_sprites_list.draw(screen)
            pointer_list.draw(screen)
        
            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game ticks (per second)
            clock.tick(60)
    
    def game() :
        ## Load config file
        conf = Config()
        ## Create engine
        engine = Engine()
        ## Init screen        
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen_mode())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!! - Level ##")
        tick_speed = engine.get_tick_speed()
        ## Init clock
        clock = pygame.time.Clock()
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Set background
        background = Background()
        
        ## Set game loop stat
        done_game = False

        ## Create game sprite groups
        player_list = pygame.sprite.Group()
        ground_list = pygame.sprite.Group()
        movable_list = pygame.sprite.Group()
        all_game_sprites_list = pygame.sprite.Group()

        ## Configurate players
        player = engine.conf_players(player_list, [movable_list, all_game_sprites_list])

        ## Generate map
        engine.gen_blocks(player_list, [ground_list, movable_list, all_game_sprites_list])

        ## Start game loop
        while not done_game :
                
            ########## EVENT ZONE ##########
        
            ## For every events, filter event and refresh screen
            for event in pygame.event.get() :
        
                ## Filter events
                ## If the cross is pressed, quit game
                if event.type == pygame.QUIT :
                    done_game = True

                for i in player :

                    ## If any key is pressed
                    if event.type == pygame.KEYDOWN :
                        
                        ## If right key is pressed
                        if event.key == player[i].key_right :
                            ## Move player to right
                            player[i].speed = player[i].speed_base
                            ## Change animation
    
                        ## If left key is pressed
                        elif event.key == player[i].key_left :
                            ## Move player to left
                            player[i].speed = -(player[i].speed_base)
                            ## Change animation
    
                        ## If key up is pressed
                        elif event.key == player[i].key_up :
                            ## Check if player in on the ground before jump
                            if player[i].on_ground == True :
                                player[i].last_y = player[i].rect.y
                                player[i].in_jump = True
                    
                    ## If key is release
                    elif event.type == pygame.KEYUP : 
                        
                        ## If key right or key left is release 
                        if (event.key == player[i].key_right) or (event.key == player[i].key_left) :
                            ## Set player speed to 0
                            player[i].speed = 0
                    
            ########## LOGIC CODE ZONE ##########
            
            for i in player :
                ## Quit game if player is out of screen
                if player[i].rect.y > conf.height :
                    engine.reset_level(player[i], movable_list)
                    player[i].reset("after_jump")
                    done_game = player[i].lose_life()
                
                ## Move the map
                engine.move_map(player[i], movable_list)

                ## Jump process
                player[i].jump()
    
                ## Detect and manage colisions between player and ground's blocks
                player[i].colide_block(ground_list, movable_list, all_game_sprites_list)
                
                ## Apply gravity to player
                player[i].gravity(ground_list, movable_list, all_game_sprites_list, 3)

                ## Update player animation and position
                player[i].update()
        
            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the entier screnn to white
            #screen.fill(Color.BLACK)
            background.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_game_sprites_list.draw(screen)
            for i in player :
                player[i].display_life(screen)

            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game tick (per second)
            clock.tick(tick_speed)

    def game_over() :
    
        ## Load config file
        conf = Config()
        ## Create engine
        engine = Engine()
        ## Init pygame
        pygame.init()
        ## Init screen
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen_mode())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!! - Game Over")
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Init clock
        clock = pygame.time.Clock()
        ## Menu loop stat
        done_game_over = False
        ## Set background
        background_red = Background()
        background_red.game_over()
        ## Create menu sprite group
        pointer_list = pygame.sprite.Group()
        buton_list = pygame.sprite.Group()
        all_game_over_sprites_list = pygame.sprite.Group()
        ## Create pointer sprite
        pointer = Pointer()
        ## Add pointer to pointer's list
        pointer_list.add(pointer)
        ## Add pointer to menu sprite's group
        all_game_over_sprites_list.add(pointer)
        ## Create butons
        buton1 = Buton("Restart", Color.WHITE)
        buton2 = Buton("Menu", Color.WHITE)
        buton3 = Buton("Quit", Color.WHITE)
        ## Set buton1 pos
        buton1.rect.x = (conf.width/2 - buton1.width/2)
        buton1.rect.y = (conf.height/2 - buton1.height/2 - 100)
        ## Set buton2 pos
        buton2.rect.x = (conf.width/3 - buton2.width/2)
        buton2.rect.y = (conf.height/2 - buton2.height/2 + 100)
        ## Set buton3 pos
        buton3.rect.x = (conf.width/3*2 - buton2.width/2)
        buton3.rect.y = (conf.height/2 - buton2.height/2 + 100)
        ## Add butons to buton list
        buton_list.add(buton1)
        buton_list.add(buton2)
        buton_list.add(buton3)
        ## Add butons to menu sprite's group
        all_game_over_sprites_list.add(buton1)
        all_game_over_sprites_list.add(buton2)
        all_game_over_sprites_list.add(buton3)
    
        ## Start loop
        while not done_game_over :
            
            ########## EVENT ZONE ##########
        
            ## For every events, filter event and refresh screen
            for event in pygame.event.get() :
        
                ## Filter events
                ## If the cross is pressed, quit game
                if event.type == pygame.QUIT :
                    done_game_over = True
                ## If any mouse buton is pressed 
                if event.type == pygame.MOUSEBUTTONDOWN :
                    ## If pointer is on buton1, start game
                    if event.button == 1 :
                        
                        ## Recover the pressed buton
                        buton = engine.get_pressed_buton(buton_list, pointer, [all_game_over_sprites_list, buton_list])

                        ## If no buton was pressed, do nothing
                        if buton == None :
                            do = "nothing"

                        ## Launch the game
                        elif buton.text is "Restart" :
                            return True
                            done_game_over = True

                        ## Quit the gameover screen
                        elif buton.text is "Menu" :
                            return False
                            done_game_over = True

                        ## Quit the game
                        elif buton.text is "Quit" :
                            done_game_over = True
                            return None

            ########## LOGIC CODE ZONE ##########
            
            ## Update mouse pos
            pos = pygame.mouse.get_pos()
            pointer.rect.x = pos[0]
            pointer.rect.y = pos[1]
            
            ## Detect bitmap colision between butons and pointer
            engine.update_selected_buton(buton_list, pointer, [all_game_over_sprites_list, buton_list])

            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the background
            background_red.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_game_over_sprites_list.draw(screen)
            pointer_list.draw(screen)

            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game ticks (per second)
            clock.tick(60)


    def options() :
    
        ## Load config file
        conf = Config()
        ## Read and stock conf_data
        conf_data = conf.get_config_data()
        ## Create engine
        engine = Engine()
        dificulty = engine.get_dificulty()
        ## Init pygame
        pygame.init()
        ## Init screen
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen_mode())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!! - Options")
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Init clock
        clock = pygame.time.Clock()
        ## Menu loop stat
        done_options = False
        ## Set background
        background = Background()
        ## Create menu sprite group
        pointer_list = pygame.sprite.Group()
        buton_list = pygame.sprite.Group()
        all_options_sprites_list = pygame.sprite.Group()
        ## Create pointer sprite
        pointer = Pointer()
        ## Add pointer to pointer's list
        pointer_list.add(pointer)
        ## Add pointer to menu sprite's group
        all_options_sprites_list.add(pointer)
        ## Create butons
        buton1 = Buton("Screen Resolution", Color.WHITE)
        engine.set_ext_buton(buton1, (str(conf_data["Config"]["Screen"]["width"]) + "x" + str(conf_data["Config"]["Screen"]["height"])))
        buton2 = Buton("Screen Format", Color.WHITE)
        engine.set_ext_buton(buton2, conf_data["Config"]["Screen"]["state"])
        buton3 = Buton("Player", Color.WHITE)
        buton4 = Buton("Dificulty", Color.WHITE)
        engine.set_ext_buton(buton4, dificulty)
        buton5 = Buton("Back", Color.WHITE)
        buton6 = Buton("Restart Game", Color.WHITE)
        ## Set buton1 pos
        buton1.rect.x = (conf.width/3 - buton1.width/2)
        buton1.rect.y = (conf.height/8*2)
        ## Set buton2 pos
        buton2.rect.x = (conf.width/3*2 - buton1.width/2)
        buton2.rect.y = (conf.height/8*2)
        ## Set buton3 pos
        buton3.rect.x = (conf.width/3 - buton1.width/2)
        buton3.rect.y = (conf.height/8*3)
        ## Set buton4 pos
        buton4.rect.x = (conf.width/3*2 - buton1.width/2)
        buton4.rect.y = (conf.height/8*3)
        ## Set buton5 pos
        buton5.rect.x = (conf.width/3 - buton1.width/2)
        buton5.rect.y = (conf.height/8*5)
        ## Set buton6 pos
        buton6.rect.x = (conf.width/3*2 - buton1.width/2)
        buton6.rect.y = (conf.height/8*5)

        ## Add butons to buton list
        buton_list.add(buton1)
        buton_list.add(buton2)
        buton_list.add(buton3)
        buton_list.add(buton4)
        buton_list.add(buton5)
        buton_list.add(buton6)
        ## Add butons to menu sprite's group
        all_options_sprites_list.add(buton1)
        all_options_sprites_list.add(buton2)
        all_options_sprites_list.add(buton3)
        all_options_sprites_list.add(buton4)
        all_options_sprites_list.add(buton5)
        all_options_sprites_list.add(buton6)
    
        ## Start loop
        while not done_options :
            
            ########## EVENT ZONE ##########
        
            ## For every events, filter event and refresh screen
            for event in pygame.event.get() :
        
                ## Filter events
                ## If the cross is pressed, quit game
                if event.type == pygame.QUIT :
                    done_options = True
                ## If any mouse buton is pressed 
                if event.type == pygame.MOUSEBUTTONDOWN :
                    ## If pointer is on buton1, start game
                    if event.button == 1 :
                        
                        ## Detect and recover the pressed buton
                        buton = engine.get_pressed_buton(buton_list, pointer, [all_options_sprites_list, buton_list])
                        
                        ## Nothig was pressed ? so do nothing
                        if buton == None :
                            
                            do = "nothing"

                        ## Change the screen resolution
                        elif buton.text.find("Screen Resolution") != -1 :
                        
                            engine.switch_resolution_buton(buton)

                        ## Change the screen format
                        elif buton.text.find("Screen Format") != -1 :
                        
                            engine.switch_screen_format_buton(buton)

                        ## Launch the player's options menu
                        elif buton.text is "Player" :
                        
                            Game.player()

                        ## Change the dificulty
                        elif buton.text.find("Dificulty") != -1 :

                            engine.switch_dificulty_buton(buton)
                        
                        ## Return to main menu
                        elif buton.text is "Back" :
                        
                            done_options = True

                        ## Restart the game
                        elif buton.text is "Restart Game" :
                        
                            done_options = True
                        
                            return True

        
            ########## LOGIC CODE ZONE ##########
            
            ## Update mouse pos
            pos = pygame.mouse.get_pos()
            pointer.rect.x = pos[0]
            pointer.rect.y = pos[1]
            
            ## Detect bitmap colision between butons and pointer
            engine.update_selected_buton(buton_list, pointer, [all_options_sprites_list, buton_list])

            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the background
            background.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_options_sprites_list.draw(screen)
            pointer_list.draw(screen)

            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game ticks (per second)
            clock.tick(60)

    def player() :
    
        ## Load config file
        conf = Config()
        ## Read and stock conf_data
        conf_data = conf.get_config_data()
        ## Create engine
        engine = Engine()
        ## Init pygame
        pygame.init()
        ## Init screen
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen_mode())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!! - Options")
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Init clock
        clock = pygame.time.Clock()
        ## Menu loop stat
        done_options = False
        ## Set background
        background = Background()
        ## Create menu sprite group
        pointer_list = pygame.sprite.Group()
        buton_list = pygame.sprite.Group()
        all_player_sprites_list = pygame.sprite.Group()
        ## Create pointer sprite
        pointer = Pointer()
        ## Add pointer to pointer's list
        pointer_list.add(pointer)
        ## Add pointer to menu sprite's group
        all_player_sprites_list.add(pointer)
        ## Create butons
        buton1 = Buton("Player number", Color.WHITE)
        engine.set_ext_buton(buton1, ( " " + str(conf_data["Config"]["Players"]["number"])))
        buton2 = Buton("Player", Color.WHITE)
        engine.set_ext_buton(buton2, ( " " + str(conf_data["Config"]["Players"]["number"]) + "'s sex " + conf_data["Config"]["Players"]["Sex"][(conf_data["Config"]["Players"]["number"] - 1)]["sex"] ))
        buton3 = Buton("Player", Color.WHITE)
        engine.set_ext_buton(buton3, (str(conf_data["Config"]["Players"]["number"]) + " action key " + str(conf_data["Config"]["Players"]["Keys"][(conf_data["Config"]["Players"]["number"] - 1)]["action"])))
        buton4 = Buton("Player", Color.WHITE)
        engine.set_ext_buton(buton4, (str(conf_data["Config"]["Players"]["number"]) + " jump key " + str(conf_data["Config"]["Players"]["Keys"][(conf_data["Config"]["Players"]["number"] - 1)]["up"])))
        buton5 = Buton("Player", Color.WHITE)
        engine.set_ext_buton(buton5, (str(conf_data["Config"]["Players"]["number"]) + " left key " + str(conf_data["Config"]["Players"]["Keys"][(conf_data["Config"]["Players"]["number"] - 1)]["left"])))
        buton6 = Buton("Player", Color.WHITE)
        engine.set_ext_buton(buton6, (str(conf_data["Config"]["Players"]["number"]) + " right key " + str(conf_data["Config"]["Players"]["Keys"][(conf_data["Config"]["Players"]["number"] - 1)]["right"])))
        buton7 = Buton("Back", Color.WHITE)
        buton8 = Buton("Restart Game", Color.WHITE)
        ## Set buton1 pos
        buton1.rect.x = (conf.width/3 - buton1.width/2)
        buton1.rect.y = (conf.height/9*2)
        ## Set buton2 pos
        buton2.rect.x = (conf.width/3*2 - buton1.width/2)
        buton2.rect.y = (conf.height/9*2)
        ## Set buton3 pos
        buton3.rect.x = (conf.width/3 - buton1.width/2)
        buton3.rect.y = (conf.height/9*3)
        ## Set buton4 pos
        buton4.rect.x = (conf.width/3*2 - buton1.width/2)
        buton4.rect.y = (conf.height/9*3)
        ## Set buton4 pos
        buton5.rect.x = (conf.width/3 - buton1.width/2)
        buton5.rect.y = (conf.height/9*4)
        ## Set buton4 pos
        buton6.rect.x = (conf.width/3*2 - buton1.width/2)
        buton6.rect.y = (conf.height/9*4)
        ## Set buton5 pos
        buton7.rect.x = (conf.width/2 - buton1.width/2)
        buton7.rect.y = (conf.height/9*6)

        ## Add butons to buton list
        buton_list.add(buton1)
        buton_list.add(buton2)
        buton_list.add(buton3)
        buton_list.add(buton4)
        buton_list.add(buton5)
        buton_list.add(buton6)
        buton_list.add(buton7)

        ## Add butons to menu sprite's group
        all_player_sprites_list.add(buton1)
        all_player_sprites_list.add(buton2)
        all_player_sprites_list.add(buton3)
        all_player_sprites_list.add(buton4)
        all_player_sprites_list.add(buton5)
        all_player_sprites_list.add(buton6)
        all_player_sprites_list.add(buton7)
    
        ## Start loop
        while not done_options :
            
            ########## EVENT ZONE ##########
        
            ## For every events, filter event and refresh screen
            for event in pygame.event.get() :
        
                ## Filter events
                ## If the cross is pressed, quit game
                if event.type == pygame.QUIT :
                    done_options = True
                ## If any mouse buton is pressed 
                if event.type == pygame.MOUSEBUTTONDOWN :
                    ## If pointer is on buton1, start game
                    if event.button == 1 :
                        
                        ## Recover the pressed buton
                        buton = engine.get_pressed_buton(buton_list, pointer, [all_player_sprites_list, buton_list])
                        
                        ## Nothing was pressed ? so do nothing
                        if buton == None :
                            
                            do = "nothing"

                        ## Change the nomber of player
                        elif buton.text.find("Player number") != -1 :
                        
                            engine.switch_player_number_buton(buton)
                            engine.update_player_menu(buton_list)

                        ## Change the sex of the player
                        elif buton.text.find("Player") != -1 and buton.text.find("sex") != -1 :
                        
                            engine.switch_player_sex_buton(buton)

                        ## Set the action key
                        elif buton.text.find("action key") != -1 :
                        
                            engine.return_pressed_key(buton)

                        ## Set the jump key
                        elif buton.text.find("jump key") != -1 :

                            engine.return_pressed_key(buton)
                        
                        ## Set the left key
                        elif buton.text.find("left key") != -1 :

                            engine.return_pressed_key(buton)
                        
                        ## Set the right key
                        elif buton.text.find("right key") != -1 :

                            engine.return_pressed_key(buton)
                        
                        ## Go back to the option's menu
                        elif buton.text is "Back" :
                        
                            done_options = True
                        
            ########## LOGIC CODE ZONE ##########
            
            ## Update mouse pos
            pos = pygame.mouse.get_pos()
            pointer.rect.x = pos[0]
            pointer.rect.y = pos[1]
            
            ## Detect bitmap colision between butons and pointer
            engine.update_selected_buton(buton_list, pointer, [all_player_sprites_list, buton_list])

            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the background
            background.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_player_sprites_list.draw(screen)
            pointer_list.draw(screen)

            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game ticks (per second)
            clock.tick(60)

## If the menu return true, restart the game
while Game.menu() is True :
    do = "nothing"

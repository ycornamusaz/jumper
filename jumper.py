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
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!!")
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Init clock
        clock = pygame.time.Clock()
        ## Menu loop stat
        done_menu = False
        start_game = False
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
        ## Set buton1 pos
        buton1.rect.x = (conf.width/2 - buton1.width/2)
        buton1.rect.y = (conf.height/2 - buton1.height/2 - 100)
        ## Set buton2 pos
        buton2.rect.x = (conf.width/2 - buton2.width/2)
        buton2.rect.y = (conf.height/2 - buton2.height/2 + 100)
        ## Add butons to buton list
        buton_list.add(buton1)
        buton_list.add(buton2)
        ## Add butons to menu sprite's group
        all_menu_sprites_list.add(buton1)
        all_menu_sprites_list.add(buton2)
    
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
                    ## If pointer is on buton1, start game
                    if event.button == 1 :
                        buton_pointer_list = pygame.sprite.spritecollide(pointer, buton_list, True)
                        for buton in buton_pointer_list :
                            if pygame.sprite.collide_mask(pointer, buton) != None :
                                if buton.text is "Play" :
                                    start_game = True

                                elif buton.text is "Options" :
                                    buton.text = "This is currently not implemented"
                                    buton.update("This is currently not implemented", Color.WHITE)

                            all_menu_sprites_list.add(buton)
                            buton_list.add(buton)
        
            ########## LOGIC CODE ZONE ##########
            
            while start_game == True :
                Game.game()
                start_game = Game.game_over()
            if start_game == None :
                break

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
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen())
        ## Init clock
        clock = pygame.time.Clock()
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Set background
        background = Background()
        
        ## Load config file
        #conf = Config("config.yaml")
        
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

                engine.move_map(player[i], movable_list)

                ## Jump process
                player[i].jump()
    
                ## Detect and manage colisions between player and ground's blocks
                player[i].colide_block(ground_list, movable_list, all_game_sprites_list)

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
            clock.tick(120)

    def game_over() :
    
        ## Load config file
        conf = Config()
        ## Create engine
        engine = Engine()
        ## Init pygame
        pygame.init()
        ## Init screen
        screen = pygame.display.set_mode([conf.width, conf.height], conf.get_screen())
        ## Init windows title
        pygame.display.set_caption("JUMPER !!!")
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
        buton2 = Buton("Quit", Color.WHITE)
        ## Set buton1 pos
        buton1.rect.x = (conf.width/2 - buton1.width/2)
        buton1.rect.y = (conf.height/2 - buton1.height/2 - 100)
        ## Set buton2 pos
        buton2.rect.x = (conf.width/2 - buton2.width/2)
        buton2.rect.y = (conf.height/2 - buton2.height/2 + 100)
        ## Add butons to buton list
        buton_list.add(buton1)
        buton_list.add(buton2)
        ## Add butons to menu sprite's group
        all_game_over_sprites_list.add(buton1)
        all_game_over_sprites_list.add(buton2)
    
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
                        buton_pointer_list = pygame.sprite.spritecollide(pointer, buton_list, True)
                        for buton in buton_pointer_list :
                            if pygame.sprite.collide_mask(pointer, buton) != None :
                                if buton.text is "Restart" :
                                    return True
                                    done_game_over = True
                                elif buton.text is "Quit" :
                                    done_game_over = True
                                    return None

                            all_game_over_sprites_list.add(buton)
                            buton_list.add(buton)
        
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

Game.menu()

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

class Game :
    def menu():
        ## Init pygame
        pygame.init()
        ## Init screen
        screen = pygame.display.set_mode([Config.width, Config.height])
        ## Init windows title
        pygame.display.set_caption("JUMPER !!!")
        ## Hide mouse cursor
        pygame.mouse.set_visible(False)
        ## Init clock
        clock = pygame.time.Clock()
        ## Menu loop stat
        done_menu = False
        ## Set background
        background = Background()
        ## Create menu sprite group
        buton_list = pygame.sprite.Group()
        all_menu_sprites_list = pygame.sprite.Group()
        ## Create pointer sprite
        pointer = Pointer()
        ## Add pointer to menu sprite's group
        all_menu_sprites_list.add(pointer)
        ## Create butons
        buton1 = Buton("Play", Color.WHITE)
        buton2 = Buton("Options", Color.WHITE)
        ## Set buton1 pos
        buton1.rect.x = (Config.width/2 - buton1.width/2)
        buton1.rect.y = (Config.height/2 - buton1.height/2 - 100)
        ## Set buton2 pos
        buton2.rect.x = (Config.width/2 - buton2.width/2)
        buton2.rect.y = (Config.height/2 - buton2.height/2 + 100)
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
                            if buton.text is "Play" :
                                #game_start = True
                                Game.game()
                            elif buton.text is "Options" :
                                buton.text = "This is currently not implemented"
                                buton.update("This is currently not implemented", Color.WHITE)

                            all_menu_sprites_list.add(buton)
                            buton_list.add(buton)
        
            ########## LOGIC CODE ZONE ##########
            
            ## Update mouse pos
            pos = pygame.mouse.get_pos()
            pointer.rect.x = pos[0]
            pointer.rect.y = pos[1]
            
            ## Detect rect colision between pointer and buton group
            buton_pointer_list = pygame.sprite.spritecollide(pointer, buton_list, True)
            
            ## If a rect colision is detected
            if buton_pointer_list != [] : 
                ## For each buton who are in colision with pointer
                for buton in buton_pointer_list :
                    ## Update text Color to red
                    if buton.color != Color.RED :
                        buton.update(buton.text , Color.RED)
                    ## Re-add buton to sprite list
                    buton_list.add(buton)
                    all_menu_sprites_list.add(buton)
            ## If not
            else :
                ## For all butons 
                for buton in buton_list :
                    ## Update text Color to white
                    if buton.color != Color.WHITE :
                        buton.update(buton.text, Color.WHITE)
            
            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the background
            background.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_menu_sprites_list.draw(screen)
        
            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game ticks (per second)
            clock.tick(60)
    
    def game() :
        ## Init screen        
        screen = pygame.display.set_mode([Config.width, Config.height])
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
        ## Create player and set player direction
        player = Player("male")
        direction = "stand"
        player_list.add(player)
        ## Add player to gamesprite's group
        movable_list.add(player)
        ## Add player to movable group
        all_game_sprites_list.add(player)

#        with open("map.yaml") as yaml_data :
#            map_data = yaml.load(yaml_data)
        conf = Config("config.yaml")
        
        ## Generate map
        conf.gen_map(player_list, [player_list, ground_list, movable_list, all_game_sprites_list])
#        for ground_type in map_data["Levels"][0]["Blocks"] :
#            i = 0
#            for x, y in map_data["Levels"][0]["Blocks"][ground_type] :
#                x = map_data["Levels"][0]["Blocks"][ground_type][i]["x"]
#                y = map_data["Levels"][0]["Blocks"][ground_type][i]["y"]
#                ground0 = Ground(ground_type)
#                ground0.rect.x = x
#                ground0.rect.y = y
#                player.last_block_colide = ground0
#                all_game_sprites_list.add(ground0)
#                ground_list.add(ground0)
#                movable_list.add(ground0)
#                i += 1

        ## Start game loop
        while not done_game :
                
            ########## EVENT ZONE ##########
        
            ## For every events, filter event and refresh screen
            for event in pygame.event.get() :
        
                ## Filter events
                ## If the cross is pressed, quit game
                if event.type == pygame.QUIT :
                    done_game = True

                ## If any key is pressed
                elif event.type == pygame.KEYDOWN :
                    
                    ## If right key is pressed
                    if event.key == pygame.K_RIGHT :
                        ## Move player to right
                        player.speed = player.speed_base
                        ## Change animation
                        direction = "right"

                    ## If left key is pressed
                    elif event.key == pygame.K_LEFT :
                        ## Move player to left
                        player.speed = -(player.speed_base)
                        ## Change animation
                        direction = "left"

                    ## If key up is pressed
                    elif event.key == pygame.K_UP :
                        ## Check if player in on the ground before jump
                        if player.on_ground == True :
                            player.last_y = player.rect.y
                            player.in_jump = True
                
                ## If key is release
                elif event.type == pygame.KEYUP : 
                    
                    ## If key right or key left is release 
                    if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_LEFT) :
                        ## Set player speed to 0
                        player.speed = 0
                        direction = "stand"
        
        
            ########## LOGIC CODE ZONE ##########
            
            ## Quit game if player is out of screen
            if player.rect.y > Config.height :
                done_game = True
            
            if (player.rect.x + player.width) > (Config.width - Config.width/3) :
                for test in movable_list :
                    test.rect.x -= 5
            if player.rect.x < (Config.width/16) :
                for test in movable_list :
                    test.rect.x += 5

            ## Jump process
            player.jump()

            ## Detect and manage colisions between player and ground's blocks
            player.colide_block(ground_list, movable_list, all_game_sprites_list)

            ## Update player animation and position
            player.update(direction)
        
            ########## CLEAR SCREEN ZONE ##########
        
            ## Set the entier screnn to white
            #screen.fill(Color.BLACK)
            background.update(screen)
        
            ########## DRAWING CODE ZONE ##########
            
            ## Draw all sprites to the screen
            all_game_sprites_list.draw(screen)
        
            ########## REFRESH SCREEN ZONE ##########
        
            ## Refresh screen
            pygame.display.flip()
        
            ## Set game tick (per second)
            clock.tick(120)

Game.menu()

#!/usr/bin/python3.4

import pygame
import json
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

        pygame.mouse.set_visible(True)
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
        ## Add player to gamesprite's group
        movable_list.add(player)
        ## Add player to movable group
        all_game_sprites_list.add(player)

        with open("map.json") as json_data :
            map_data = json.load(json_data)
        
        ## Generate map
        i = 0
        for blocks in map_data["Level_1"][0]["Block"] :
            x = map_data["Level_1"][0]["Block"][i]["x"]
            y = map_data["Level_1"][0]["Block"][i]["y"]
            ground0 = Ground()
            ground0.rect.x = x
            ground0.rect.y = y
            last_ground = ground0
            all_game_sprites_list.add(ground0)
            ground_list.add(ground0)
            movable_list.add(ground0)
            i += 1

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
            
            ## Detect rect colisions between player and ground block
            ground_player_list = pygame.sprite.spritecollide(player, ground_list, True)
            ## If a rect colision is detected
            if ground_player_list != [] :
                ## For each blocks in colision
                for ground in ground_player_list :
                    ## If a bitmap colision is detected
                    if pygame.sprite.collide_mask(player, ground) != None :
                        ## If the player is enter into the block by the top
                        if (player.rect.y + player.height) <= (ground.rect.y + 3) :
                            ## Set ground value to true
                            player.reset("on_ground")
                            ## Set player pos to the top of the block
                            player.rect.y -= 3
                            ## Set the block to last block
                            last_ground = ground
                        ## If the player is enter into the block by the bottom
                        elif (player.rect.y) >= (ground.rect.y + ground.height - 30) :
                            ## Move the player out of the block
                            player.rect.y += 1 #(ground.rect.y + ground.height )
                            ## Reset player variables
                            player.reset("after_jump")
                            ## Set block to the last block
                            last_ground = ground
                            ## Gravity
                            player.rect.y += 3
                        ## If the player is enter into the block by the right side
                        elif (player.rect.x + player.width) > (ground.rect.x) and (player.rect.x + player.width) < (ground.rect.x + ground.width) :
                            ## Move the player out of the block
                            player.rect.x -= (5 + player.speed)
                            ## Gravity
                            player.rect.y += 3
                        ## If the player is enter into the block by the left side
                        elif (player.rect.x) < (ground.rect.x + ground.width) and (player.rect.x) > (ground.rect.x) :
                            ## Move the player out of the block
                            player.rect.x += (5 - player.speed)
                            ## Gravity
                            player.rect.y += 3
                    ## If the player isn't on the block or down the block
                    #elif (player.rect.x + player.width) <= (last_ground.rect.x) or (player.rect.x) >= (last_ground.rect.x + last_ground.width) or (player.rect.y) >= (last_ground.rect.y + last_ground.height) : 
                    else :
                        ## Set groud val to 0
                        player.on_ground = False
                        ## Gravity
                        player.rect.y += 3
                    ## Re-add block to default group
                    movable_list.add(ground)
                    ground_list.add(ground)
                    all_game_sprites_list.add(ground)


            ## If the player isn't on the block or down the block
            elif (player.rect.x + player.width) <= (last_ground.rect.x) or (player.rect.x) >= (last_ground.rect.x + last_ground.width) or (player.rect.y) >= (last_ground.rect.y + last_ground.height) : 
                ## Set groud val to 0
                player.on_ground = False
                ## Gravity
                player.rect.y += 3

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

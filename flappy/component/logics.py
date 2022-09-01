import sys  #We will use sys.exit() to exit the game
import os
import random #for generating random numbers
import pygame #for game development
from pygame.locals import *  #Basic pygame imports
from flappy.logger.log import logging
from flappy.exception.exception_handler import AppException
from flappy.config.configuration import AppConfiguration


class Flappy:
    """
    Flappy is a class to play flappy game,
    It contains all the functionality needed to play the game 
    """

    def __init__(self, app_config = AppConfiguration()):
        """
        Initiate the Flappy class
        """
        try:
            self.templates_config = app_config.get_templates_config()
            self.root_game_config = app_config.get_root_game_config()

            self.FPS = self.root_game_config.fps
            self.SCREENWIDTH = self.root_game_config.screen_width
            self.SCREENHEIGHT = self.root_game_config.screen_height
            self.SCREEN = pygame.display.set_mode((self.SCREENWIDTH,self.SCREENHEIGHT))
            self.GROUND_Y = self.SCREENHEIGHT * 0.8
            self.PLAYER = self.root_game_config.player_name
            self.BACKGROUND = self.root_game_config.background_name
            self.PIPE = self.root_game_config.pipe_name
            self.FPS_CLOCK = pygame.time.Clock() 

            self.GAME_SPRITES = {}
            self.GAME_SOUNDS = {}


            #Keeping all png number images in this dictionary
            self.GAME_SPRITES['numbers'] = (
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"0.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"1.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"2.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"3.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"4.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"5.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"6.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"7.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"8.png")).convert_alpha(),
                pygame.image.load(os.path.join(self.templates_config.sprites_dir,"9.png")).convert_alpha()
            )


            #Keeping the message,base,background,player & pipe image in this dictionary
            self.GAME_SPRITES["message"] = pygame.image.load(os.path.join(self.templates_config.sprites_dir,"message.png")).convert_alpha()
            self.GAME_SPRITES["base"] = pygame.image.load(os.path.join(self.templates_config.sprites_dir,"base.png")).convert_alpha()
            self.GAME_SPRITES["background"] = pygame.image.load(os.path.join(self.templates_config.sprites_dir,self.BACKGROUND)).convert_alpha()
            self.GAME_SPRITES["player"] = pygame.image.load(os.path.join(self.templates_config.sprites_dir,self.PLAYER)).convert_alpha()
            self.GAME_SPRITES["pipe"] = (
                                        pygame.transform.rotate(pygame.image.load(os.path.join(self.templates_config.sprites_dir,self.PIPE)).convert_alpha(), 180),
                                        pygame.image.load(os.path.join(self.templates_config.sprites_dir,self.PIPE)).convert_alpha()
                                        )

            

            #Game sounds, Keeping all sounds  in this dictionary
            self.GAME_SOUNDS['die'] = pygame.mixer.Sound(os.path.join(self.templates_config.audios_dir,"die.wav"))
            self.GAME_SOUNDS['hit'] = pygame.mixer.Sound(os.path.join(self.templates_config.audios_dir,"hit.wav"))
            self.GAME_SOUNDS['point'] = pygame.mixer.Sound(os.path.join(self.templates_config.audios_dir,"point.wav"))
            self.GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(os.path.join(self.templates_config.audios_dir,"swoosh.wav"))
            self.GAME_SOUNDS['wing'] = pygame.mixer.Sound(os.path.join(self.templates_config.audios_dir,"wing.wav"))

            logging.info(f"Loaded all the game assets successfully!")
        
        except Exception as e:
            raise AppException(e, sys) from e

    


    def welcomeScreen(self):
        '''
        To shows welcome screen in front of the user
        '''
        try:
            #To get player X & Y value
            player_X = int(self.SCREENWIDTH/5)
            player_Y = int((self.SCREENHEIGHT - self.GAME_SPRITES['player'].get_height())/2) 
            
            #To get message X & Y value
            message_X = int((self.SCREENWIDTH - self.GAME_SPRITES['message'].get_width())/2) 
            message_Y = int(self.SCREENHEIGHT * 0.13) 
            
            #To get base X value
            base_X = 0

            while True:
                for event in pygame.event.get():
                    #If users click on the cross button the game will be exit
                    if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    #If the user presses space bar or up key button then the game will be start
                    elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                        return
                    
                    else:
                        self.SCREEN.blit(self.GAME_SPRITES['background'],(0,0))
                        self.SCREEN.blit(self.GAME_SPRITES['player'],(player_X , player_Y))
                        self.SCREEN.blit(self.GAME_SPRITES['message'],(message_X , message_Y))
                        self.SCREEN.blit(self.GAME_SPRITES['base'],(base_X , self.GROUND_Y))
                        pygame.display.update()
                        self.FPS_CLOCK.tick(self.FPS)
        
        except Exception as e:
            raise AppException(e, sys) from e

    

    def getRandomPipe(self):
        '''
        Generate position of two pipe (one bottom straight and one top rotate) for bliting on the screen
        '''
        try:

            pipHeight = self.GAME_SPRITES['pipe'][0].get_height()
            offset = self.SCREENHEIGHT/3
            y2 = offset + random.randrange(0, int(self.SCREENHEIGHT - self.GAME_SPRITES['base'].get_height()- 1.2 * offset))
            pipeX = self.SCREENWIDTH + 10
            y1 = pipHeight - y2 + offset
            pipe = [
                {'x':pipeX , 'y':-y1}, #upper pipe
                {'x':pipeX , 'y':y2} #lower pipe

            ]
            
            return pipe
        
        except Exception as e:
            raise AppException(e,sys) from e


    

    #Game over function
    def isCollide(self,player_X , player_Y , upperPipes , lowerPipes):
        try:
            if player_Y > self.GROUND_Y - 25 or player_Y<0:
                self.GAME_SOUNDS['hit'].play()
                return True
            
            for pipe in upperPipes:
                pipeHeight = self.GAME_SPRITES['pipe'][0].get_height()
                if(player_Y < pipeHeight + pipe['y'] and abs(player_X - pipe['x']) < self.GAME_SPRITES['pipe'][0].get_width()):
                    self.GAME_SOUNDS['hit'].play()
                    return True
            
            for pipe in lowerPipes:
                if(player_Y + self.GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_X - pipe['x']) < self.GAME_SPRITES['pipe'][0].get_width():
                    self.GAME_SOUNDS['hit'].play()
                    return True

            return False
        
        except Exception as e:
            raise AppException(e,sys) from e


    

    def mainGame(self):
        '''
        This is the main function of the game 
        '''
        try:
            score = 0
            player_X = int(self.SCREENWIDTH/5)
            player_Y = int(self.SCREENWIDTH/2)
            base_X = 0

            #create 2 pipes for bliting on the screen
            newPipe1 = self.getRandomPipe()
            newPipe2 = self.getRandomPipe()

            #My list of upper pipes
            upperPipes = [
                {'x': self.SCREENWIDTH + 200, 'y':newPipe1[0]['y']},
                {'x': self.SCREENWIDTH + 200 +(self.SCREENWIDTH/2), 'y':newPipe2[0]['y']}
            ]
            
            #My list of lower pipes
            lowerPipes = [
                {'x': self.SCREENWIDTH + 200, 'y':newPipe1[1]['y']},
                {'x': self.SCREENWIDTH + 200 +(self.SCREENWIDTH/2), 'y':newPipe2[1]['y']}
            ]

            
            pipeVelocity_X = -4
            
            playerVelocity_Y = -9
            playerMaxVelocity_Y = 10
            playerMinVelocity_Y = -8
            playerAccleration_Y = 1

            playerFlapAccv = -8 #Velocity while flapping
            playerFlapped = False #it is true only when the bird is flapping


            #Game loop
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                        if player_Y > 0:
                            playerVelocity_Y = playerFlapAccv
                            playerFlapped = True
                            self.GAME_SOUNDS['wing'].play()

                crashTest = self.isCollide(player_X , player_Y , upperPipes , lowerPipes) #This funtion will return true if you get crash
                if crashTest:
                    return

                #Check for score
                playerMidPos = player_X + self.GAME_SPRITES['player'].get_width()/2   #player middle position

                for pipe in upperPipes:
                    pipeMidPos = pipe['x'] + self.GAME_SPRITES['pipe'][0].get_width()/2     #pipe middle position
                    
                    if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                        score += 1
                        print(f"Your score is {score}")
                        self.GAME_SOUNDS['point'].play()


                #player move
                if playerVelocity_Y < playerMaxVelocity_Y and not playerFlapped:
                    playerVelocity_Y += playerAccleration_Y

                if playerFlapped:
                    playerFlapped = False

                playerHeight = self.GAME_SPRITES['player'].get_height()
                player_Y = player_Y + min(playerVelocity_Y, self.GROUND_Y - player_Y - playerHeight)

                #Moves pipes to the left
                for upperPipe , lowerPipe in zip(upperPipes , lowerPipes):

                    upperPipe['x'] += pipeVelocity_X
                    lowerPipe['x'] += pipeVelocity_X

                #Add a new pipe when the first pipe crosses left
                if 0<upperPipes[0]['x']<5:
                    
                    newPipe = self.getRandomPipe()
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])


                #If the pipe is out of the screen , remove it
                if upperPipes[0]['x'] < - self.GAME_SPRITES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

                #Lets blit our sprites now
                self.SCREEN.blit(self.GAME_SPRITES['background'],(0,0))
                for upperPipe,lowerPipe in zip(upperPipes,lowerPipes): 
                    self.SCREEN.blit(self.GAME_SPRITES['pipe'][0],(upperPipe['x'] , upperPipe['y']))
                    self.SCREEN.blit(self.GAME_SPRITES['pipe'][1],(lowerPipe['x'] , lowerPipe['y']))
                
                self.SCREEN.blit(self.GAME_SPRITES['base'],(base_X , self.GROUND_Y))
                self.SCREEN.blit(self.GAME_SPRITES['player'],(player_X , player_Y))
        

                #Score bliting
                myDigits = [int(x) for x in list(str(score))]
                width = 0
                for digit in myDigits:
                    width += self.GAME_SPRITES['numbers'][digit].get_width()
                
                xoffset = (self.SCREENWIDTH - width)/2

                for digit in myDigits:
                    self.SCREEN.blit(self.GAME_SPRITES['numbers'][digit],(xoffset, self.SCREENHEIGHT*0.12))
                    xoffset += self.GAME_SPRITES['numbers'][digit].get_width()
                pygame.display.update()
                self.FPS_CLOCK.tick(self.FPS)
        
        except Exception as e:
            raise AppException(e,sys) from e








        

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
        
        except Exception as e:
            raise AppException(e, sys) from e

        

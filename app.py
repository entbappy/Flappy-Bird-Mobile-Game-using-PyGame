import pygame 
from pygame.locals import *  
from flappy.logger.log import logging
from flappy.exception.exception_handler import AppException
from flappy.component.logics import Flappy


class GameEngine:
    def __init__(self):
        self.game_obj = Flappy()
        logging.info("Starting game engine")
    
    def start(self):
        self.game_obj.welcomeScreen()
        self.game_obj.mainGame()
        logging.info("Terminating game engine")


if __name__ == "__main__":

    #This will be the main point from where our game will start
    pygame.init() #Initialize pygame module
    pygame.display.set_caption('Flappy Bird')

    while True:
        obj = GameEngine()
        obj.start() 

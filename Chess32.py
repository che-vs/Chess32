#Chess32 State Manager
#Controls program flow between all modules

import os
import pygame
import sys
import numpy as np

from menu import first
from twoplayer import second
from lessonmenu import third
from botmenu import fourth
from baseplate import fifth
from credit import sixth
from baseplate2 import seventh

#State definitions
menu = 1
two_player = 2
lesson_menu = 3
bot_menu = 4
baseplate = 5
credit = 6
lessons = 7

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess32")
        
    current_state = menu
    running = True

    #Configuration values passed through all states
    config = {
        "lesson": 1,    #Current lesson number (1-8)
        "level": 1,     #Current bot level (1-8)
        "state": 1      #Current state
    }

    font = pygame.font.Font(None, 48)
    
    while running:
        
        #Run current state function
        if current_state == menu:
            result = first(screen, config)
        elif current_state == two_player:
            result = second(screen)
        elif current_state == lesson_menu:
            result = third(screen, config)
        elif current_state == bot_menu:
            result = fourth(screen, config)
        elif current_state == baseplate:
            result = fifth(screen, config)
        elif current_state == credit:
            result = sixth(screen)
        elif current_state == lessons:
            result = seventh(screen, config)
        else:
            result = menu
        
        #Handle result
        if result == "quit" or result == 0:
            running = False
        elif result in range(1, 8):
            current_state = result
        elif result is None:
            pass  #Stay in current state
        else:
            current_state = menu  #Invalid result = default to menu
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import pygame
import subprocess
import sys
import random
import time

from PIL import Image, ImageFilter
import numpy as np

from lessons.lesson1 import *
from lessons.lesson2 import *
from lessons.lesson3 import *
from lessons.lesson4 import *
from lessons.lesson5 import *
from lessons.lesson6 import *
from lessons.lesson7 import *
from lessons.lesson8 import *

def lessonfunction(lesson): #returns the correct function based on lesson selected
    if lesson == 1:
        return lesson1
    elif lesson == 2:
        return lesson2  
    elif lesson == 3:
        return lesson3
    elif lesson == 4:
        return lesson4
    elif lesson == 5:
        return lesson5
    elif lesson == 6:
        return lesson6
    elif lesson == 7:
        return lesson7
    elif lesson == 8:
        return lesson8
    else:
        return lesson1  

def seventh(screen, config):  #This is the main function for state 7 (baseplate for lessons)

    #Read which lesson to run
    lessonnum = config["lesson"]
    
    #Get the function for that lesson
    lessonfunc = lessonfunction(lessonnum)
    
    #Run the lesson function
    result = lessonfunc(screen)
    
    #Return the result to the state manager
    return result


if __name__ == "__main__":
    result = seventh()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

import pygame
import chess
import subprocess
import sys
import random
import time

from PIL import Image, ImageFilter
import numpy as np

def third(screen, config):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson Menu")

    board = pygame.image.load("images/board.png") 

    #colours
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    BLACK = (0, 0, 0)

    #fonts size
    fontlarge = pygame.font.Font(None, 48)  #names
    fontmedium = pygame.font.Font(None, 31)  #descriptions
    fontXL = pygame.font.Font(None, 64)  #title
    fontsmall = pygame.font.Font(None, 24)  #lesson labels

    #title
    title = fontXL.render("Lessons", True, WHITE)

    #lesson names
    name1 = fontsmall.render("Lesson 1", True, WHITE)
    name2 = fontsmall.render("Lesson 2", True, WHITE)
    name3 = fontsmall.render("Lesson 3", True, WHITE)
    name4 = fontsmall.render("Lesson 4", True, WHITE)
    name5 = fontsmall.render("Lesson 5", True, WHITE)
    name6 = fontsmall.render("Lesson 6", True, WHITE)
    name7 = fontsmall.render("Lesson 7", True, WHITE)
    name8 = fontsmall.render("Lesson 8", True, WHITE)

    def blur(): #Some AI assistance was used to implement screen state blurring
        #Get the current screen as a string
        screenArray = pygame.surfarray.array3d(screen)
        screenArray = np.transpose(screenArray, (1, 0, 2))  #Fix orientation
        
        #Convert to PIL Image
        pilImage = Image.fromarray(screenArray.astype("uint8"), "RGB")
        
        #Apply blur
        blurred = pilImage.filter(ImageFilter.GaussianBlur(radius=5))
        
        #Convert back to pygame surface
        blurredArray = np.array(blurred)
        blurredSurface = pygame.surfarray.make_surface(np.transpose(blurredArray, (1, 0, 2)))
        
        return blurredSurface
    
    running = True

    #load lesson profiles
    lesson1_img = pygame.transform.scale(pygame.image.load("lessons/images/openbook.png"), (120, 120))  
    lesson2_img = pygame.transform.scale(pygame.image.load("lessons/images/tactics.png"), (120, 120))
    lesson3_img = pygame.transform.scale(pygame.image.load("lessons/images/play.png"), (120, 120))  
    lesson4_img = pygame.transform.scale(pygame.image.load("lessons/images/captured.png"), (120, 120))   
    lesson5_img = pygame.transform.scale(pygame.image.load("lessons/images/swordking.png"), (170, 120))   
    lesson6_img = pygame.transform.scale(pygame.image.load("lessons/images/deadking.png"), (120, 120))
    lesson7_img = pygame.transform.scale(pygame.image.load("lessons/images/opening.png"), (120, 150))
    lesson8_img = pygame.transform.scale(pygame.image.load("lessons/images/better.png"), (120, 120))
    back_img = pygame.transform.scale(pygame.image.load("images/gameover/mainmenu.jpg"), (100, 100))   

    #Row 1: lessons 1-4 
    lesson1_rect = lesson1_img.get_rect(center=(160, 320))  
    lesson2_rect = lesson2_img.get_rect(center=(320, 320))  
    lesson3_rect = lesson3_img.get_rect(center=(480, 320))  
    lesson4_rect = lesson4_img.get_rect(center=(640, 320))  

    #Row 2: lessons 5-8 
    lesson5_rect = lesson5_img.get_rect(center=(160, 500))  
    lesson6_rect = lesson6_img.get_rect(center=(350, 500))  
    lesson7_rect = lesson7_img.get_rect(center=(480, 500))  
    lesson8_rect = lesson8_img.get_rect(center=(640, 500))  

    #back button in top left corner (takes you to main menu)
    back_rect = back_img.get_rect(center=(100, 60))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #esc to quit
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: #b to go back
                    return 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lesson1_rect.collidepoint(event.pos):
                    config["lesson"] = 1  #Set lesson in config dict
                    return 7
                elif lesson2_rect.collidepoint(event.pos):
                    config["lesson"] = 2
                    return 7
                elif lesson3_rect.collidepoint(event.pos):
                    config["lesson"] = 3
                    return 7
                elif lesson4_rect.collidepoint(event.pos):
                    config["lesson"] = 4
                    return 7
                elif lesson5_rect.collidepoint(event.pos):
                    config["lesson"] = 5
                    return 7
                elif lesson6_rect.collidepoint(event.pos):
                    config["lesson"] = 6
                    return 7
                elif lesson7_rect.collidepoint(event.pos):
                    config["lesson"] = 7
                    return 7
                elif lesson8_rect.collidepoint(event.pos):
                    config["lesson"] = 8
                    return 7
                elif back_rect.collidepoint(event.pos):
                    return 1
                    
        if running:  
            #draw the board
            screen.blit(board, (0, 0))
            blurred_bg = blur()
            screen.blit(blurred_bg, (0, 0))

            #print profiles
            screen.blit(lesson1_img, lesson1_rect)
            screen.blit(lesson2_img, lesson2_rect)
            screen.blit(lesson3_img, lesson3_rect)
            screen.blit(lesson4_img, lesson4_rect)
            screen.blit(lesson5_img, lesson5_rect)
            screen.blit(lesson6_img, lesson6_rect)
            screen.blit(lesson7_img, lesson7_rect)
            screen.blit(lesson8_img, lesson8_rect)
            screen.blit(back_img, back_rect)

            #print names and titles
            screen.blit(title, (400 - title.get_width()//2, 150))

            screen.blit(name1, (160 - name1.get_width()//2, 395))  

            screen.blit(name2, (320 - name2.get_width()//2, 395))  

            screen.blit(name3, (480 - name3.get_width()//2, 395))  

            screen.blit(name4, (640 - name4.get_width()//2, 395))  

            screen.blit(name5, (160 - name5.get_width()//2, 575))  
            
            screen.blit(name6, (320 - name6.get_width()//2, 575))  

            screen.blit(name7, (480 - name7.get_width()//2, 575))  

            screen.blit(name8, (640 - name8.get_width()//2, 575))   
        
            pygame.display.flip() #update display

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = third()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

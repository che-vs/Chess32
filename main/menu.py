import pygame
import sys
import subprocess
import numpy as np

from PIL import Image, ImageFilter

def first(screen, config):
    logo = pygame.image.load("images/logo.png") #changes app icon
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32") #app caption

    board = pygame.image.load("images/board.png") #background

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
    #create all the buttons
    play_button = pygame.transform.scale(pygame.image.load("images/menuassets/play.png"), (100, 100))  
    bot_button = pygame.transform.scale(pygame.image.load("images/menuassets/bot.png"), (100, 100))

    settings_button = pygame.transform.scale(pygame.image.load("images/menuassets/handbookbutton.png"), (100, 100))  
    quit_button = pygame.transform.scale(pygame.image.load("images/menuassets/quitbutton.png"), (100, 100)) 

    brand = pygame.transform.scale(pygame.image.load("images/menuassets/logologo.png"), (600, 600))

    #create hitboxes for the buttons
    brand_rect = brand.get_rect(center=(400, 300))  

    play_button_rect = play_button.get_rect(center=(300, 550)) 
    bot_button_rect = bot_button.get_rect(center=(500, 550))
    
    settings_button_rect = settings_button.get_rect(center=(300, 680))
    quit_button_rect = quit_button.get_rect(center=(500, 680))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the game is force quit the game quits
                running = False
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #esc to quit
                    running = False
                    return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos): #add click functionality
                    return 2
                
                elif bot_button_rect.collidepoint(event.pos):   
                    return 4

                elif settings_button_rect.collidepoint(event.pos):
                    return 3

                elif brand_rect.collidepoint(event.pos):
                    return 6

                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"

        if running:  
            #draw the board
            screen.blit(board, (0, 0))
            blurred_bg = blur() #blur the background
            screen.blit(blurred_bg, (0, 0)) #print the blurred background

            #print the buttons and hitboxes
            screen.blit(play_button, play_button_rect.topleft)
            screen.blit(bot_button, bot_button_rect.topleft)
            screen.blit(settings_button, settings_button_rect.topleft)
            screen.blit(quit_button, quit_button_rect.topleft)
            screen.blit(brand, brand_rect)
            pygame.display.flip() #update the board


    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = first()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()


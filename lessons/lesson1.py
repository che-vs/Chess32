import pygame
import chess
import sys

from PIL import Image, ImageFilter
import numpy as np

def lesson1(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson 1")

    board = pygame.image.load("images/board.png") 

    #colours
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    BLACK = (0, 0, 0)
    GOLD = (255, 215, 0)

    #fonts size
    fontlarge = pygame.font.Font(None, 48)  #names
    fontmedium = pygame.font.Font(None, 31)  #descriptions
    fontXL = pygame.font.Font(None, 64)  #title
    fontsmall = pygame.font.Font(None, 24)  #level labels

    current_page = 1

    #title
    title = fontXL.render("Lesson 1 - Controls", True, GOLD)

    #Page 1 - Controls
    line1 = fontmedium.render("• Click on any icon to navigate through the game", True, WHITE)
    line2 = fontmedium.render("• Press U to undo moves", True, WHITE)
    line3 = fontmedium.render("• Press Esc to exit at any point in the program", True, WHITE)
    line4 = fontmedium.render("• Press B to return to menu", True, WHITE)
    line5 = fontmedium.render("• Press R to reset game", True, WHITE)
    line6 = fontmedium.render("• Use arrow keys to navigate through Lesson pages if", True, WHITE)
    line7 = fontmedium.render("  there are multiple pages. Page numbers in bottom right.", True, WHITE)

    #Page 2 - Secret Page

    title1 = fontXL.render("DISCLAMER", True, GOLD)
    
    line8 = fontmedium.render("  LEVEL 8 AI IS NOT TO BE MESSED WITH", True, WHITE)
    line9 = fontmedium.render("  PLAY AT YOUR OWN RISK", True, WHITE)
    line10 = fontmedium.render("  NO MAN HAS COME OUT ALIVE", True, WHITE)
    line11 = fontmedium.render("  YOU HAVE BEEN WARNED", True, WHITE)

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

    back_img = pygame.transform.scale(pygame.image.load("images/gameover/mainmenu.jpg"), (100, 100))   
    
    back_rect = back_img.get_rect(center=(100, 60))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #esc to quit
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_LEFT: #previous page
                    current_page = max(1, current_page - 1)
                elif event.key == pygame.K_RIGHT: #next page
                    current_page = min(2, current_page + 1)
                elif event.key == pygame.K_b: #return to menu
                    return 3

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return 3

        if running:  
            #draw the board
            screen.blit(board, (0, 0))
            blurred_bg = blur()
            screen.blit(blurred_bg, (0, 0))

            screen.blit(back_img, back_rect)
            
            #Page indicator
            page_text = fontsmall.render(f"Page {current_page}/1", True, WHITE)
            screen.blit(page_text, (700, 770))

            if current_page == 1: #If the page is one draw lines for page 1
                screen.blit(title, (400 - title.get_width()//2, 150))

                screen.blit(line1, (100, 300))
                screen.blit(line2, (100, 330))
                screen.blit(line3, (100, 360))
                screen.blit(line4, (100, 390))
                screen.blit(line5, (100, 420))
                screen.blit(line6, (100, 450))
                screen.blit(line7, (100, 480))
                
            elif current_page == 2:
                screen.blit(title1, (400 - title1.get_width()//2, 150))

                screen.blit(line8, (100, 300))
                screen.blit(line9, (100, 330))
                screen.blit(line10, (100, 360))
                screen.blit(line11, (100, 390))

            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = lesson1()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

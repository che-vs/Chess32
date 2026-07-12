import pygame
import chess
import sys

from PIL import Image, ImageFilter
import numpy as np

def lesson7(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson 7")

    board = pygame.image.load("images/board.png")

    control = pygame.transform.scale(pygame.image.load("lessons/images/lesson7/control.png"), (250, 250))

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
    title = fontXL.render("Lesson 7 - Winning Tips", True, GOLD)

    #Page 1 - Winning Tips for Beginners
    line1 = fontmedium.render("• Try to control the center of the board.", True, WHITE)
    line2 = fontmedium.render("• Develop your pieces early - Start with knights", True, WHITE)
    line3 = fontmedium.render("  and bishops.", True, WHITE)
    line4 = fontmedium.render("• Castle your king.", True, WHITE)
    line5 = fontmedium.render("• Connect your rooks.", True, WHITE)
    line6 = fontmedium.render("• Do not leave pieces hanging.", True, WHITE)
    line7 = fontmedium.render("• Don't bring out your queen too early.", True, WHITE)

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
                    current_page = min(1, current_page + 1)
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

            if current_page == 1:
                screen.blit(title, (400 - title.get_width()//2, 150))
                screen.blit(line1, (100, 250))
                screen.blit(line2, (100, 300))
                screen.blit(line3, (100, 330))
                screen.blit(line4, (100, 360))
                screen.blit(line5, (100, 390))
                screen.blit(line6, (100, 420))
                screen.blit(line7, (100, 450))
                screen.blit(control, (250, 500))

            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = lesson7()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

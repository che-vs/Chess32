import pygame
import chess
import sys

from PIL import Image, ImageFilter
import numpy as np

def lesson2(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson 2")

    board = pygame.image.load("images/board.png")

    chessboard = pygame.transform.scale(pygame.image.load("lessons/images/lesson2/chessboard.png"), (250, 250))   

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
    title1 = fontXL.render("Lesson 2 Part 1 - What is Chess?", True, GOLD)

    #Page 1 - What is Chess?
    line1 = fontmedium.render("• Chess is a two-player board game.", True, WHITE)
    line2 = fontmedium.render("• One player uses the white pieces, the other uses", True, WHITE)
    line3 = fontmedium.render("  the black pieces.", True, WHITE)
    line4 = fontmedium.render("• White always moves first.", True, WHITE)
    line5 = fontmedium.render("• Players take turns moving one piece at a time.", True, WHITE)
    line6 = fontmedium.render("• The goal of the game is to checkmate the opponent’s king.", True, WHITE)

    title2 = fontXL.render("Lesson 2 Part 2 - The Chessboard", True, GOLD)
    
    #Page 2 - The Chessboard
    line7 = fontmedium.render("• The chessboard has 64 squares.", True, WHITE)
    line8 = fontmedium.render("• There are 8 columns (files) and 8 rows (ranks).", True, WHITE)
    line9 = fontmedium.render("• Each square is either light or dark.", True, WHITE)
    line10 = fontmedium.render("• The bottom-right square for White is always light.", True, WHITE)
    line11 = fontmedium.render("• The black king is always on a light square and vice versa", True, WHITE)

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
            page_text = fontsmall.render(f"Page {current_page}/2", True, WHITE)
            screen.blit(page_text, (700, 770))

            if current_page == 1: #If the page is one draw lines for page 1
                screen.blit(title1, (400 - title1.get_width()//2, 150))

                screen.blit(line1, (100, 300))
                screen.blit(line2, (100, 330))
                screen.blit(line3, (100, 360))
                screen.blit(line4, (100, 390))
                screen.blit(line5, (100, 420))
                screen.blit(line6, (100, 450))

            elif current_page == 2:
                screen.blit(title2, (400 - title2.get_width()//2, 150))

                screen.blit(line7, (100, 300))
                screen.blit(line8, (100, 330))
                screen.blit(line9, (100, 360))
                screen.blit(line10, (100, 390))
                screen.blit(line11, (100, 420))

                screen.blit(chessboard, (250, 500))
                
            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = lesson2()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

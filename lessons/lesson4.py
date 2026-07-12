import pygame
import chess
import sys

from PIL import Image, ImageFilter
import numpy as np

def lesson4(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson 4")

    board = pygame.image.load("images/board.png")

    capture = pygame.transform.scale(pygame.image.load("lessons/images/lesson4/capture.jpg"), (250, 250))   

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
    title = fontlarge.render("Lesson 4 Part 1 - Capturing Pieces", True, GOLD)

    #Page 1 - Capturing Pieces
    line1 = fontmedium.render("• A capture happens when a piece moves onto a", True, WHITE)
    line2 = fontmedium.render("  square occupied by an opponent's piece.", True, WHITE)
    line3 = fontmedium.render("• The captured piece is removed from the board.", True, WHITE)
    line4 = fontmedium.render("• Only one piece may occupy a square.", True, WHITE)

    #title
    title1 = fontlarge.render("Lesson 4 Part 2 - Piece Values", True, GOLD)

    #Page 1 - Capturing Pieces
    line5 = fontmedium.render("• Pawn: 1", True, WHITE)
    line6 = fontmedium.render("• Knight and Bishop: 3", True, WHITE)
    line7 = fontmedium.render("• Rook: 5", True, WHITE)
    line8 = fontmedium.render("• Queen: 9", True, WHITE)
    line9 = fontmedium.render("• King: Priceless (the game can no", True, WHITE)
    line10 = fontmedium.render("  longer go on if the king is dead)", True, WHITE)

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

            if current_page == 1:
                screen.blit(title, (400 - title.get_width()//2, 150))
                screen.blit(line1, (100, 250))
                screen.blit(line2, (100, 280))
                screen.blit(line3, (100, 310))
                screen.blit(line4, (100, 340))
                screen.blit(capture, (250, 400))
            elif current_page == 2:
                screen.blit(title1, (400 - title1.get_width()//2, 150))
                screen.blit(line5, (100, 250))
                screen.blit(line6, (100, 290))
                screen.blit(line7, (100, 320))
                screen.blit(line8, (100, 350))
                screen.blit(line9, (100, 380))
                screen.blit(line10, (100, 410))
                
            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = lesson4()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

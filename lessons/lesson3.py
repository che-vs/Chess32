import pygame
import chess
import sys

from PIL import Image, ImageFilter
import numpy as np

def lesson3(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson 3")

    board = pygame.image.load("images/board.png") 

    kingmovement = pygame.transform.scale(pygame.image.load("lessons/images/lesson3/kingmovement.png"), (250, 250))   
    queenmovement = pygame.transform.scale(pygame.image.load("lessons/images/lesson3/queenmovement.png"), (250, 250))   
    bishopmovement = pygame.transform.scale(pygame.image.load("lessons/images/lesson3/bishopmovement.png"), (250, 250))   
    knightmovement = pygame.transform.scale(pygame.image.load("lessons/images/lesson3/knightmovement.png"), (250, 250))   
    rookmovement = pygame.transform.scale(pygame.image.load("lessons/images/lesson3/rookmovement.png"), (250, 250))   
    pawnmovement = pygame.transform.scale(pygame.image.load("lessons/images/lesson3/pawnmovement.png"), (250, 250))   

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
    title1 = fontXL.render("Lesson 3 Part 1 - The Pawn", True, GOLD)

    #Page 1 - Pawn
    line1 = fontmedium.render("• Pawns move forward one square.", True, WHITE)
    line2 = fontmedium.render("• On their first move, they may move two squares.", True, WHITE)
    line3 = fontmedium.render("• Pawns capture diagonally.", True, WHITE)
    line4 = fontmedium.render("• Pawns cannot move backward.", True, WHITE)

    title2 = fontXL.render("Lesson 3 Part 2 - The Rook", True, GOLD)
    
    #Page 2 - Rook
    line5 = fontmedium.render("• Rooks move in straight lines.", True, WHITE)
    line6 = fontmedium.render("• They can move up, down, left, or right.", True, WHITE)
    line7 = fontmedium.render("• Rooks cannot jump over other pieces.", True, WHITE)

    title3 = fontXL.render("Lesson 3 Part 3 - The Bishop", True, GOLD)
    
    #Page 3 - Bishop
    line8 = fontmedium.render("• Bishops move diagonally.", True, WHITE)
    line9 = fontmedium.render("• A bishop always stays on the same color square.", True, WHITE)
    line10 = fontmedium.render("• Bishops cannot jump over other pieces.", True, WHITE)

    title4 = fontXL.render("Lesson 3 Part 4 - The Knight", True, GOLD)
    
    #Page 4 - Knight
    line11 = fontmedium.render("• Knights move in an L-shape.", True, WHITE)
    line12 = fontmedium.render("• They move two squares in one direction and one", True, WHITE)
    line13 = fontmedium.render("  square sideways.", True, WHITE)
    line14 = fontmedium.render("• Knights can jump over other pieces.", True, WHITE)

    title5 = fontXL.render("Lesson 3 Part 5 - The Queen", True, GOLD)
    
    #Page 5 - Queen
    line15 = fontmedium.render("• The queen moves like a rook and a bishop combined.", True, WHITE)
    line16 = fontmedium.render("• She can move straight or diagonally.", True, WHITE)
    line17 = fontmedium.render("• The queen is the most powerful piece.", True, WHITE)

    title6 = fontXL.render("Lesson 3 Part 6 - The King", True, GOLD)
    
    #Page 6 - King
    line18 = fontmedium.render("• The king moves one square in any direction.", True, WHITE)
    line19 = fontmedium.render("• The king is the most important piece.", True, WHITE)
    line20 = fontmedium.render("• If the king is trapped in check, the game ends.", True, WHITE)

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
                    current_page = min(6, current_page + 1)
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
            page_text = fontsmall.render(f"Page {current_page}/6", True, WHITE)
            screen.blit(page_text, (700, 770))

            if current_page == 1: #If the page is one draw lines for page 1
                screen.blit(title1, (400 - title1.get_width()//2, 150))
                screen.blit(line1, (100, 250))
                screen.blit(line2, (100, 300))
                screen.blit(line3, (100, 330))
                screen.blit(line4, (100, 360))
                screen.blit(pawnmovement, (250, 500))
            elif current_page == 2:
                screen.blit(title2, (400 - title2.get_width()//2, 150))
                screen.blit(line5, (100, 250))
                screen.blit(line6, (100, 300))
                screen.blit(line7, (100, 330))
                screen.blit(rookmovement, (250, 500))
            elif current_page == 3:
                screen.blit(title3, (400 - title3.get_width()//2, 150))
                screen.blit(line8, (100, 250))
                screen.blit(line9, (100, 300))
                screen.blit(line10, (100, 330))
                screen.blit(bishopmovement, (250, 500))
            elif current_page == 4:
                screen.blit(title4, (400 - title4.get_width()//2, 150))
                screen.blit(line11, (100, 250))
                screen.blit(line12, (100, 300))
                screen.blit(line13, (100, 330))
                screen.blit(line14, (100, 360))
                screen.blit(knightmovement, (250, 500))
            elif current_page == 5:
                screen.blit(title5, (400 - title5.get_width()//2, 150))
                screen.blit(line15, (100, 250))
                screen.blit(line16, (100, 300))
                screen.blit(line17, (100, 330))
                screen.blit(queenmovement, (250, 500))
            elif current_page == 6:
                screen.blit(title6, (400 - title6.get_width()//2, 150))
                screen.blit(line18, (100, 250))
                screen.blit(line19, (100, 300))
                screen.blit(line20, (100, 330))
                screen.blit(kingmovement, (250, 500))

            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = lesson3()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

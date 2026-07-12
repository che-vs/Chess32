import pygame
import chess
import sys

from PIL import Image, ImageFilter
import numpy as np

def lesson5(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Lesson 5")

    board = pygame.image.load("images/board.png")

    check = pygame.transform.scale(pygame.image.load("lessons/images/lesson5/check.png"), (250, 250))
    checkmate = pygame.transform.scale(pygame.image.load("lessons/images/lesson5/checkmate.png"), (250, 250))
    draw = pygame.transform.scale(pygame.image.load("lessons/images/lesson5/draw.png"), (250, 250))
    stalemate = pygame.transform.scale(pygame.image.load("lessons/images/lesson5/stalemate.png"), (250, 250))

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
    title = fontXL.render("Lesson 5 Part 1 - Check", True, GOLD)

    #Page 1 - Check
    line1 = fontmedium.render("• Check means the king is under attack.", True, WHITE)
    line2 = fontmedium.render("• When your king is in check, you must respond.", True, WHITE)
    line3 = fontmedium.render("• You may move the king, block the attack, or", True, WHITE)
    line4 = fontmedium.render("  capture the attacking piece.", True, WHITE)

    title1 = fontXL.render("Lesson 5 Part 2 - Checkmate", True, GOLD)
    
    #Page 2 - Checkmate
    line5 = fontmedium.render("• Checkmate means the king is in check and", True, WHITE)
    line6 = fontmedium.render("  cannot escape.", True, WHITE)
    line7 = fontmedium.render("• The game ends immediately when checkmate", True, WHITE)
    line8 = fontmedium.render("  happens.", True, WHITE)
    line9 = fontmedium.render("• The king is never captured.", True, WHITE)

    title2 = fontXL.render("Lesson 5 Part 3 - Stalemate/Draw", True, GOLD)
    
    #Page 2 - Stalemate/Draw
    line10 = fontmedium.render("• Stalemate means the king can no longer move to a safe", True, WHITE)
    line11 = fontmedium.render("  square but also has no other pieces to move while not in check", True, WHITE)
    line12 = fontmedium.render("• A draw occurs when the same two moves are repeated thrice,", True, WHITE)
    line13 = fontmedium.render("  both sides have insufficient material to checkmate eachother", True, WHITE)
    line14 = fontmedium.render("• or when 50 moves without captures or pawn moves occur.", True, WHITE)

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
                    current_page = min(3, current_page + 1)
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
            page_text = fontsmall.render(f"Page {current_page}/3", True, WHITE)
            screen.blit(page_text, (700, 770))

            if current_page == 1:
                screen.blit(title, (400 - title.get_width()//2, 150))
                screen.blit(line1, (100, 250))
                screen.blit(line2, (100, 280))
                screen.blit(line3, (100, 310))
                screen.blit(line4, (100, 340))
                screen.blit(check, (250, 450))
            elif current_page == 2:
                screen.blit(title1, (400 - title1.get_width()//2, 150))
                screen.blit(line5, (100, 250))
                screen.blit(line6, (100, 280))
                screen.blit(line7, (100, 310))
                screen.blit(line8, (100, 340))
                screen.blit(line9, (100, 370))
                screen.blit(checkmate, (250, 450))
            elif current_page == 3:
                screen.blit(title2, (400 - title2.get_width()//2, 150))
                screen.blit(line10, (100, 250))
                screen.blit(line11, (100, 280))
                screen.blit(line12, (100, 310))
                screen.blit(line13, (100, 340))
                screen.blit(line14, (100, 370))
                screen.blit(draw, (100, 450))
                screen.blit(stalemate, (400, 450))

            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = lesson5()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

import pygame
import sys
import subprocess
import numpy as np

from PIL import Image, ImageFilter

def sixth(screen):
    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    pygame.display.set_caption("Chess32 - Credits")

    board = pygame.image.load("images/board.png") 

    #colors
    WHITE = (255, 255, 255)
    GOLD = (255, 215, 0)
    LIGHT_GOLD = (255, 230, 150)

    #font sizes
    font_title = pygame.font.Font(None, 64)
    font_section = pygame.font.Font(None, 48)
    font_name = pygame.font.Font(None, 36)
    font_credit = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24) #for page numbers

    current_page = 1
    total_pages = 4

    #title
    title = font_title.render("Chess32 Credits", True, GOLD)

    #Page 1 - Development Team
    section1 = font_section.render("Development Team", True, WHITE)
    name1 = font_name.render("Chief Programmer", True, GOLD)
    credit1 = font_credit.render("Lewis Chavara", True, WHITE)  

    name2 = font_name.render("Game Design", True, GOLD)
    credit2 = font_credit.render("Lewis Chavara", True, WHITE)

    name3 = font_name.render("UI/UX Design", True, GOLD)
    credit3 = font_credit.render("Lewis Chavara", True, WHITE)

    name4 = font_name.render("Testing & Quality Assurance", True, GOLD)
    credit4 = font_credit.render("Lewis Chavara", True, WHITE)

    #Page 2 - External Libraries
    section2 = font_section.render("External Libraries", True, WHITE)
    lib1 = font_name.render("Pygame", True, GOLD)
    credit_lib1 = font_credit.render("Game development framework", True, LIGHT_GOLD)

    lib2 = font_name.render("Python-Chess", True, GOLD)
    credit_lib2 = font_credit.render("Chess logic and move validation", True, LIGHT_GOLD)

    lib3 = font_name.render("Pillow (PIL)", True, GOLD)
    credit_lib3 = font_credit.render("Image processing and effects", True, LIGHT_GOLD)

    lib4 = font_name.render("NumPy", True, GOLD)
    credit_lib4 = font_credit.render("Mathematical operations", True, LIGHT_GOLD)

    #Page 3 - Special Thanks
    section3 = font_section.render("Special Thanks", True, WHITE)
    thanks1 = font_name.render("Chess Programming Wiki", True, GOLD)
    credit_thanks1 = font_credit.render("Educational resources and algorithms", True, LIGHT_GOLD)

    thanks2 = font_name.render("Open Source Community", True, GOLD)
    credit_thanks2 = font_credit.render("Libraries and inspiration", True, LIGHT_GOLD)

    thanks3 = font_name.render("Beta Testers", True, GOLD)
    credit_thanks3 = font_credit.render("For valuable feedback and bug reports", True, LIGHT_GOLD)

    #Page 4 - Copyright
    section4 = font_section.render("Copyright Information", True, WHITE)
    copyright1 = font_name.render("Chess32 © 2024", True, GOLD)
    credit_copyright1 = font_credit.render("All rights reserved", True, LIGHT_GOLD)

    copyright2 = font_name.render("License", True, GOLD)
    credit_copyright2 = font_credit.render("For personal and educational use", True, LIGHT_GOLD)

    copyright3 = font_name.render("Acknowledgments", True, GOLD)
    credit_copyright3 = font_credit.render("Thank you for playing!", True, LIGHT_GOLD)

    def blur():
        screenArray = pygame.surfarray.array3d(screen)
        screenArray = np.transpose(screenArray, (1, 0, 2))
        
        pilImage = Image.fromarray(screenArray.astype("uint8"), "RGB")
        
        blurred = pilImage.filter(ImageFilter.GaussianBlur(radius=5))
        
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
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_LEFT:
                    current_page = max(1, current_page - 1)
                elif event.key == pygame.K_RIGHT:
                    current_page = min(total_pages, current_page + 1)
                elif event.key == pygame.K_b:
                    return 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return 1
                    
        if running:  
            #Draw the board with blur effect
            screen.blit(board, (0, 0))
            blurred_bg = blur()
            screen.blit(blurred_bg, (0, 0))

            #Draw back button and title
            screen.blit(back_img, back_rect)
            screen.blit(title, (400 - title.get_width()//2, 100))
            
            #Page indicator
            page_text = font_small.render(f"Page {current_page}/{total_pages}", True, WHITE)
            screen.blit(page_text, (700, 770))

            #Page content
            if current_page == 1:
                screen.blit(section1, (400 - section1.get_width()//2, 180))
                screen.blit(name1, (400 - name1.get_width()//2, 290))
                screen.blit(credit1, (400 - credit1.get_width()//2, 320))
                screen.blit(name2, (400 - name2.get_width()//2, 390))
                screen.blit(credit2, (400 - credit2.get_width()//2, 420))
                screen.blit(name3, (400 - name3.get_width()//2, 490))
                screen.blit(credit3, (400 - credit3.get_width()//2, 520))
                screen.blit(name4, (400 - name4.get_width()//2, 590))
                screen.blit(credit4, (400 - credit4.get_width()//2, 620))
                
            elif current_page == 2:
                screen.blit(section2, (400 - section2.get_width()//2, 180))
                screen.blit(lib1, (400 - lib1.get_width()//2, 290))
                screen.blit(credit_lib1, (400 - credit_lib1.get_width()//2, 320))
                screen.blit(lib2, (400 - lib2.get_width()//2, 390))
                screen.blit(credit_lib2, (400 - credit_lib2.get_width()//2, 420))
                screen.blit(lib3, (400 - lib3.get_width()//2, 490))
                screen.blit(credit_lib3, (400 - credit_lib3.get_width()//2, 520))
                screen.blit(lib4, (400 - lib4.get_width()//2, 590))
                screen.blit(credit_lib4, (400 - credit_lib4.get_width()//2, 620))
                
            elif current_page == 3:
                screen.blit(section3, (400 - section3.get_width()//2, 180))
                screen.blit(thanks1, (400 - thanks1.get_width()//2, 290))
                screen.blit(credit_thanks1, (400 - credit_thanks1.get_width()//2, 320))
                screen.blit(thanks2, (400 - thanks2.get_width()//2, 390))
                screen.blit(credit_thanks2, (400 - credit_thanks2.get_width()//2, 420))
                screen.blit(thanks3, (400 - thanks3.get_width()//2, 490))
                screen.blit(credit_thanks3, (400 - credit_thanks3.get_width()//2, 520))
                
            elif current_page == 4:
                screen.blit(section4, (400 - section4.get_width()//2, 180))
                screen.blit(copyright1, (400 - copyright1.get_width()//2, 290))
                screen.blit(credit_copyright1, (400 - credit_copyright1.get_width()//2, 320))
                screen.blit(copyright2, (400 - copyright2.get_width()//2, 390))
                screen.blit(credit_copyright2, (400 - credit_copyright2.get_width()//2, 420))
                screen.blit(copyright3, (400 - copyright3.get_width()//2, 490))
                screen.blit(credit_copyright3, (400 - credit_copyright3.get_width()//2, 520))

            pygame.display.flip()

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = sixth()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

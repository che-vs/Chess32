import pygame
import chess
import subprocess
import sys
import random
import time

from PIL import Image, ImageFilter
import numpy as np

import threading #To prevent unresponsiveness while the AI is thinking

from bots.bot1 import *
from bots.bot2 import *
from bots.bot3 import *
from bots.bot4 import *
from bots.bot5 import *
from bots.bot6 import *
from bots.bot7 import *
from bots.bot8 import *

def BotLevel(level): #returns the correct function based on level selected
    if level == 1:
        return level1
    elif level == 2:
        return level2  
    elif level == 3:
        return level3
    elif level == 4:
        return level4
    elif level == 5:
        return level5
    elif level == 6:
        return level6
    elif level == 7:
        return level7
    elif level == 8:
        return level8
    else:
        return level1  

def ColPicker():
    col = random.randint(1,2) #Player and Bot colours are randomised 
    if col == 1:
        return chess.WHITE, chess.BLACK
    else:
        return chess.BLACK, chess.WHITE

def fifth(screen, config):  #This is the main function for state 5 (baseplate/bot game)

    sqsize = 100

    levelnum = config["level"]
    pygame.display.set_caption(f"Chess32 - Bot Level {levelnum}")

    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    PlayerCol, BotCol = ColPicker()
    BotFunc = BotLevel(levelnum)

    #Load piece images
    def load_images():
        pieces = ["P", "R", "N", "B", "Q", "K", "p", "r", "n", "b", "q", "k"]
        images = {}
        for piece in pieces:
            if piece.isupper():
                folder = "images/white"
            else:
                folder = "images/black"
            images[piece] = pygame.image.load(f"{folder}/{piece}.png")
        return images

    def draw_board(images): #draws images
        boardpng = pygame.image.load("images/board.png")
        screen.blit(boardpng, (0, 0))

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                col = chess.square_file(square) #board faces player
                if PlayerCol == chess.WHITE:
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)
                else:
                    col = 7 - chess.square_file(square)
                    row = chess.square_rank(square)
                screen.blit(images[piece.symbol()], (col * sqsize, row * sqsize))

    def BotMove(board): #importing AI function
        move = BotFunc(board)
        return move

    def check(): #highlight when in check
        if board.is_check():
            if board.turn == chess.WHITE:
                king_square = board.king(chess.WHITE)
            else:
                king_square = board.king(chess.BLACK)

            if PlayerCol == chess.WHITE:
                col = chess.square_file(king_square)
                row = 7 - chess.square_rank(king_square)
            else:
                col = 7 - chess.square_file(king_square) 
                row = chess.square_rank(king_square)
                
            red = (255, 0, 0)
            x = col * sqsize
            y = row * sqsize
            pygame.draw.rect(screen, red, (x, y, sqsize, sqsize), 4)

    def checkmate(): #highlight when checkmate
        nonlocal state, InCheckmate
        if board.is_checkmate():
            king_square = board.king(board.turn)

            if PlayerCol == chess.WHITE:
                col = chess.square_file(king_square)
                row = 7 - chess.square_rank(king_square)
            else:
                col = 7 - chess.square_file(king_square) 
                row = chess.square_rank(king_square)

            red = pygame.Surface((sqsize, sqsize), pygame.SRCALPHA)
            red.fill((255, 0, 0, 128))
            screen.blit(red, (col * sqsize, row * sqsize))
            pygame.display.flip()

            if board.turn == chess.WHITE: #switch to gameover screen and sets the correct background for winners
                InCheckmate = "White"
            else:
                InCheckmate = "Black"

            pygame.time.delay(500) #0.5s before gameover screen
            state = "GameOver"

    def draw(board):
        nonlocal stalemate, state

        #get position of kings
        white = board.king(chess.WHITE)
        black = board.king(chess.BLACK)

        #Check if the game is drawn due to any of these conditions:
        # - Stalemate: Player to move has no legal moves but is not in check
        # - Insufficient material: Not enough pieces to force checkmate (e.g. king vs king)
        # - Threefold repetition: Same position repeated three times
        # - Fifty-move rule: 50 moves without a pawn move or capture

        if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition(3) or board.is_fifty_moves():
            stalemate = True

            if PlayerCol == chess.WHITE:
                col1 = chess.square_file(white)     #get column
                row1 = 7 - chess.square_rank(white) #flip row for black
                col2 = chess.square_file(black)
                row2 = 7 - chess.square_rank(black)
            else:
                col1 = 7 - chess.square_file(white) #flip col for black
                row1 = chess.square_rank(white)     #get row
                col2 = 7 - chess.square_file(black)
                row2 = chess.square_rank(black)

            grey = pygame.Surface((sqsize, sqsize), pygame.SRCALPHA)
            grey.fill((128, 128, 128, 200)) #colour in grey

            screen.blit(grey, (col1 * sqsize, row1 * sqsize))
            screen.blit(grey, (col2 * sqsize, row2 * sqsize))

            pygame.display.flip()
            pygame.time.delay(1000) #1s delay before gameover screen

            state = "GameOver"
            
        else:
            stalemate = False

    def legal(selected_square):
        piece = board.piece_at(selected_square)

        if piece is not None: #as in the selected square isnt just an empty square
            #get all legal moves for the selected piece
            LegalMoves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]
            for square in LegalMoves:
                if PlayerCol == chess.WHITE:
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)
                else:
                    col = 7 - chess.square_file(square)
                    row = chess.square_rank(square)

                green = (0, 255, 0)
                x = col * sqsize
                y = row * sqsize
                pygame.draw.rect(screen, green, (x, y, sqsize, sqsize), 4)
            return LegalMoves
        return []

    def MoveHighlight():
        if move_history:
            last_move = move_history[-1]
            from_square = last_move.from_square #square from last move
            to_square = last_move.to_square #final square
            
            highlighted_squares = [from_square, to_square] #highlights both squares
            
            for square in highlighted_squares:
                if PlayerCol == chess.WHITE:
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)
                else:
                    col = 7 - chess.square_file(square)
                    row = chess.square_rank(square)
                
                highlight_color = (255, 215, 0, 100)  #Gold with transparency
                highlight_surface = pygame.Surface((sqsize, sqsize), pygame.SRCALPHA)
                highlight_surface.fill(highlight_color)
                screen.blit(highlight_surface, (col * sqsize, row * sqsize))

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

    def Promotion(from_square, to_square):
        piece = board.piece_at(from_square)

        if piece is None or piece.piece_type != chess.PAWN:
            return False
        
        to_rank = chess.square_rank(to_square)

        #White pawn reaching rank 7 (8th rank) or Black pawn reaching rank 0 (1st rank)
        if piece.color == chess.WHITE and to_rank == 7:
            return True

        elif piece.color == chess.BLACK and to_rank == 0:
            return True

        return False

    def PromotionMenu(images):
        blurState = blur()
        screen.blit(blurState, (0, 0))

        overlay = pygame.Surface((800, 800))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128) #make it semi-transparent
        screen.blit(overlay, (0, 0))

        if board.turn == chess.WHITE:
            pieces = ["Q", "R", "B", "N"] #White pieces
        else:
            pieces = ["q", "r", "b", "n"] #Black pieces

        screen.blit(images[pieces[0]], (250, 250))
        Queen = pygame.Rect(250, 250, 100, 100)

        screen.blit(images[pieces[1]], (450, 250))
        Rook = pygame.Rect(450, 250, 100, 100)

        screen.blit(images[pieces[2]], (250, 450))
        Bishop = pygame.Rect(250, 450, 100, 100)

        screen.blit(images[pieces[3]], (450, 450))
        Knight = pygame.Rect(450, 450, 100, 100)

        rects = [Queen, Rook, Bishop, Knight]
        return rects, pieces

    def InvertSelection(location):
        #convert mouse click to chess square based on player color
        col = location[0] // sqsize
        row = location[1] // sqsize

        if PlayerCol == chess.WHITE:
            square = chess.square(col, 7 - row) 
        else:
            square = chess.square(7 - col, row)  

        return square

    #game state variables
    board = chess.Board()
    state = "InGame"
    InCheckmate = "White"
    stalemate = False
    pendingMove = None
    ai_thinking = False
    ai_move = None
    move_history = []

    #####################################################################################################################################################

    #Main game loop
    images = load_images()
    running = True
    selected_square = None
    move_history = []
    clock = pygame.time.Clock()

    #draw initial board immediately to prevent black screen
    draw_board(images)
    pygame.display.flip()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #r to reset
                    return 5  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: #b to go back
                    return 4  
                    

            if state == "InGame" and board.turn == PlayerCol:  #Only allow player moves when it's their turn
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    square = InvertSelection(location)

                    if selected_square is None:
                        piece = board.piece_at(square)
                        if piece and piece.color == board.turn:
                            selected_square = square
                    else:
                        piece = board.piece_at(selected_square)
                        if (piece and piece.piece_type == chess.PAWN and
                                ((piece.color == chess.WHITE and chess.square_rank(square) == 7) or
                                 (piece.color == chess.BLACK and chess.square_rank(square) == 0))):
                            pendingMove = (selected_square, square)
                            state = "Promotion"
                            selected_square = None
                        else:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                board.push(move)
                                move_history.append(move)
                            selected_square = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        if move_history and len(move_history) >= 2:  #Undo both player and AI moves
                            board.pop()  #Undo AI move
                            board.pop()  #Undo player move
                            move_history.pop()
                            move_history.pop()
                        elif move_history:  #Only player move to undo
                            board.pop()
                            move_history.pop()

            elif state == "Promotion": #promotion menu to select promotion piece
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    choice = 0

                    #check if the mouse clicks on the button
                    if 250 <= mouse_x <= 350 and 250 <= mouse_y <= 350:
                        choice = chess.QUEEN
                    elif 450 <= mouse_x <= 550 and 250 <= mouse_y <= 350:
                        choice = chess.ROOK
                    elif 250 <= mouse_x <= 350 and 450 <= mouse_y <= 550:
                        choice = chess.BISHOP
                    elif 450 <= mouse_x <= 550 and 450 <= mouse_y <= 550:
                        choice = chess.KNIGHT

                    if choice > 0 and pendingMove is not None:
                        from_square, to_square = pendingMove
                        promotion_move = chess.Move(from_square, to_square, choice)

                        if promotion_move in board.legal_moves:
                            board.push(promotion_move) #promotes the pawn
                            move_history.append(promotion_move)

                        pendingMove = None
                        selected_square = None
                        state = "InGame" #switches back to game

            elif state == "GameOver":
                running = True
                pygame.display.set_caption("Game Over")

                whitewin = pygame.image.load("images/gameover/whitewin.png")
                blackwin = pygame.image.load("images/gameover/blackwin.png")
                stalemate_img = pygame.image.load("images/gameover/stalemate.png")

                MainMenu = pygame.transform.scale(pygame.image.load("images/gameover/mainmenu.jpg"), (100, 100))
                MainMenu_Rect = MainMenu.get_rect(center=(200, 700))

                PlayAgain = pygame.transform.scale(pygame.image.load("images/gameover/playagain.jpg"), (100, 100))
                PlayAgain_Rect = PlayAgain.get_rect(center=(400, 700))

                Exit = pygame.transform.scale(pygame.image.load("images/gameover/exit.jpg"), (100, 100))
                Exit_Rect = Exit.get_rect(center=(600, 700))

                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if MainMenu_Rect.collidepoint(event.pos):
                                return 1 
                            elif PlayAgain_Rect.collidepoint(event.pos):
                                return 5  
                            elif Exit_Rect.collidepoint(event.pos):
                                running = False
                                pygame.quit()
                                sys.exit()

                    if running:
                        if stalemate == True:
                            screen.blit(stalemate_img, (0, 0))
                        else:
                            if InCheckmate == "White":
                                screen.blit(blackwin, (0, 0))
                            else:
                                screen.blit(whitewin, (0, 0))

                        screen.blit(MainMenu, MainMenu_Rect)
                        screen.blit(PlayAgain, PlayAgain_Rect.topleft)
                        screen.blit(Exit, Exit_Rect.topleft)

                        pygame.display.flip()

        #####
        if state == "InGame" and board.turn == BotCol and not ai_thinking: #Threading was added with the help of AI 
            ai_thinking = True                                             #Threading allows the AI to run at a higher depth without crashes
                                                                           #A higher depth does mean longer wait times but also more work on the CPU resulting in unresponsiveness

            def ai_thread():                                               
                nonlocal ai_move #nonlocal allows nested functions to modify the outer functions variables
                board_copy = board.copy()
                ai_move = BotFunc(board_copy)

            thread = threading.Thread(target=ai_thread)
            thread.start()

        if ai_thinking and ai_move is not None: #when done
            board.push(ai_move) 
            move_history.append(ai_move)
            ai_thinking = False
            ai_move = None
            pygame.display.flip()

        #######Drawing#######
                
        if running and state == "InGame":
            draw_board(images)

            MoveHighlight()

            if selected_square is not None and board.turn == PlayerCol:
                legal(selected_square)

            check()
            checkmate()
            draw(board)
            
            pygame.display.flip()

        elif running and state == "Promotion":
            draw_board(images)
            MoveHighlight()
            PromotionMenu(images)
            pygame.display.flip()

        clock.tick(60)  #60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    result = fifth()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

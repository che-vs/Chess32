import pygame
import chess
import subprocess
import sys

from PIL import Image, ImageFilter
import numpy as np

def second(screen):

    sqsize = 100
    pygame.display.set_caption("Chess32 - Two Player")

    logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)

    #load piece images
    def load_images():
        pieces = ["P", "R", "N", "B", "Q", "K", "p", "r", "n", "b", "q", "k"]
        images = {}
        for piece in pieces:
            if piece.isupper():
                folder = "images/white"  #white pieces folder
            else:
                folder = "images/black"  #black pieces folder
            images[piece] = pygame.image.load(f"{folder}/{piece}.png")
        return images

    def draw_board(images): #draw board and pieces
        boardpng = pygame.image.load("images/board.png")
        screen.blit(boardpng, (0, 0))
        
        #draw pieces onto board
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                #calculate piece position (flipped for Black's turn)
                if board.turn == chess.WHITE:
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)
                else:
                    col = 7 - chess.square_file(square)
                    row = chess.square_rank(square)
                screen.blit(images[piece.symbol()], (col * sqsize, row * sqsize))

    #####################################################################################################################################################

    board = chess.Board()  #Chess Module functionality was implemented with help of a friend (for setting up pieces and legal moves)
    state = "InGame"       #changes states to allow activities outside the game that affect the game
    InCheckmate = "White"
    stalemate = False
    pendingMove = None
    move_history = []      #for undoing moves

    def check():
        if board.is_check():
            if board.turn == chess.WHITE:
                king_square = board.king(chess.WHITE) #white king
            else:
                king_square = board.king(chess.BLACK) #black king
            #calculate highlight position (flipped for Black's turn)
            if board.turn == chess.WHITE:
                col = chess.square_file(king_square)
                row = 7 - chess.square_rank(king_square)
            else:
                col = 7 - chess.square_file(king_square)
                row = chess.square_rank(king_square)
                        
            red = (255, 0, 0)
            x = col * sqsize
            y = row * sqsize

            pygame.draw.rect(screen, (red), (x, y, sqsize, sqsize), 4)

    def checkmate():
        nonlocal InCheckmate, state  

        if board.is_checkmate():
            #get king position
            if board.turn == chess.WHITE:
                king_square = board.king(chess.WHITE) #white king
            else:
                king_square = board.king(chess.BLACK) #black king
            #calculate highlight position (flipped for Black's turn)
            if board.turn == chess.WHITE:
                col = chess.square_file(king_square)
                row = 7 - chess.square_rank(king_square)
            else:
                col = 7 - chess.square_file(king_square)
                row = chess.square_rank(king_square)

            red = pygame.Surface((sqsize, sqsize), pygame.SRCALPHA)
            red.fill((255, 0, 0, 128))

            #highlight the king in dark red
            screen.blit(red, (col * sqsize, row * sqsize))
            pygame.display.flip()  #update display

            if board.is_checkmate():
                if board.turn == chess.WHITE:
                    InCheckmate = "White"
                else:
                    InCheckmate = "Black"
                
            #wait 0.5 seconds
            pygame.time.delay(500)

            state = "GameOver" #changes game state from InGame to GameOver

    def draw(board):
        nonlocal stalemate, state

        white = board.king(chess.WHITE) 
        black = board.king(chess.BLACK) 

        if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition(3) or board.is_fifty_moves():
            stalemate = True

            if board.turn == chess.WHITE:
                col1 = chess.square_file(white)#first row and col for the first king
                row1 = 7 - chess.square_rank(white)
                col2 = chess.square_file(black)#second row and col for the second king
                row2 = 7 - chess.square_rank(black)#this is to highlight both kings grey because nobody won
            else:
                col1 = 7 - chess.square_file(white)
                row1 = chess.square_rank(white)
                col2 = 7 - chess.square_file(black)
                row2 = chess.square_rank(black)
        
            grey = pygame.Surface((sqsize, sqsize), pygame.SRCALPHA)
            grey.fill((128, 128, 128, 200))

            screen.blit(grey, (col1 * sqsize, row1 * sqsize))
            screen.blit(grey, (col2 * sqsize, row2 * sqsize))
            pygame.display.flip()  #update display

            #wait 1 second
            pygame.time.delay(1000)

            state = "GameOver" #changes game state from InGame to GameOver

        else:
            stalemate = False

    def legal(selected_square):
        piece = board.piece_at(selected_square)

        if piece is not None: #as in the selected square isnt just an empty square
            #get all legal moves for the selected piece
            LegalMoves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]

            for square in LegalMoves:
                if board.turn == chess.WHITE:
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)
                else:
                    col = 7 - chess.square_file(square)
                    row = chess.square_rank(square)

                green = (0, 255, 0)
                x = col * sqsize
                y = row * sqsize

                pygame.draw.rect(screen, (green), (x, y, sqsize, sqsize), 4)

            return LegalMoves
        return []

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
        overlay.set_alpha(128)  #Make it semi transparent
        screen.blit(overlay, (0, 0))
        
        if board.turn == chess.WHITE:
            pieces = ["Q", "R", "B", "N"]  #White pieces
        else:
            pieces = ["q", "r", "b", "n"]  #Black pieces

        #Queen
        screen.blit(images[pieces[0]], (250, 250))
        Queen = pygame.Rect(250, 350, 100, 100)

        #Rook  
        screen.blit(images[pieces[1]], (450, 250))
        Rook = pygame.Rect(450, 350, 100, 100)

        #Bishop 
        screen.blit(images[pieces[2]], (250, 450))
        Bishop = pygame.Rect(250, 250, 100, 100)

        #Knight 
        screen.blit(images[pieces[3]], (450, 450))
        Knight = pygame.Rect(450, 250, 100, 100)
        
        #Put all the rectangles in a list for click detection
        rects = [Queen, Rook, Bishop, Knight]
        
        return rects, pieces

    def MoveHighlight(): #to easily see who moved last and moved what
        if move_history:
            last_move = move_history[-1]
            from_square = last_move.from_square #square from last move
            to_square = last_move.to_square     #final square
            
            highlighted_squares = [from_square, to_square] #highlights both squares
            
            for square in highlighted_squares:
                if board.turn == chess.WHITE:
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)
                else:
                    col = 7 - chess.square_file(square)
                    row = chess.square_rank(square)
                
                highlight_color = (255, 215, 0, 100)  #Gold with transparency
                highlight_surface = pygame.Surface((sqsize, sqsize), pygame.SRCALPHA)
                highlight_surface.fill(highlight_color)
                screen.blit(highlight_surface, (col * sqsize, row * sqsize))

    #####################################################################################################################################################

    #Main game

    images = load_images()  
    running = True  
    selected_square = None  
    move_history = [] #logs the moves

    while running:  
        for event in pygame.event.get():  #check for events
            if event.type == pygame.QUIT:  #if the window is closed
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
                    return 2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: #b to go back
                    return 1

            if state == "InGame":
                if event.type == pygame.MOUSEBUTTONDOWN:  
                    #get mouse position
                    location = pygame.mouse.get_pos()  
                    col = location[0] // sqsize  
                    row = location[1] // sqsize  
                    #calculate square index (flipped for Black's turn)
                    if board.turn == chess.WHITE:
                        square = chess.square(col, 7 - row)
                    else:
                        square = chess.square(7 - col, row)

                    if selected_square is None: 
                        #Only select squares with pieces belonging to the current player
                        piece = board.piece_at(square)
                        if piece and piece.color == board.turn: 
                            selected_square = square  

                    else:  #if a square is already selected
                        #Check if this is a promotion move first
                        piece = board.piece_at(selected_square)
                        if (piece and piece.piece_type == chess.PAWN and 
                            ((piece.color == chess.WHITE and chess.square_rank(square) == 7) or (piece.color == chess.BLACK and chess.square_rank(square) == 0))):
                                pendingMove = (selected_square, square)  #Store the move
                                state = "Promotion"  #Switch to promotion state
                                selected_square = None
                        else:
                            #Regular move handling
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                board.push(move) 
                                move_history.append(move)
                                pygame.time.delay(100)  #0.1ms delay
                            selected_square = None 

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:  #if "U" is pressed
                        if move_history:  #check move history
                            board.pop()  #undo last move
                            move_history.pop()  #remove last move from history

########################################Separating the game states####################################################################################

            elif state == "Promotion":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    
                    #Check which piece was clicked
                    choice = 0
                    if 250 <= mouse_x <= 350 and 250 <= mouse_y <= 350:      #Queen 
                        choice = chess.QUEEN
                    elif 450 <= mouse_x <= 550 and 250 <= mouse_y <= 350:    #Rook
                        choice = chess.ROOK   
                    elif 250 <= mouse_x <= 350 and 450 <= mouse_y <= 550:    #Bishop
                        choice = chess.BISHOP 
                    elif 450 <= mouse_x <= 550 and 450 <= mouse_y <= 550:    #Knight 
                        choice = chess.KNIGHT
                    
                    #If a piece was clicked, make the move
                    if choice > 0 and pendingMove is not None:
                        from_square, to_square = pendingMove
                        
                        #Create the promotion move
                        promotion_move = chess.Move(from_square, to_square, choice)
                        
                        if promotion_move in board.legal_moves:
                            board.push(promotion_move)
                            move_history.append(promotion_move)
                        
                        #Reset everything back to normal
                        pendingMove = None
                        selected_square = None
                        state = "InGame"
                
            
########################################Separating the game states####################################################################################

            elif state == "GameOver":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MainMenu_Rect.collidepoint(event.pos):
                        return 1

                    elif PlayAgain_Rect.collidepoint(event.pos):
                        return 2

                    elif Exit_Rect.collidepoint(event.pos):
                        running = False 
                        pygame.quit()
                        sys.exit()

        if running and state == "InGame":
            draw_board(images)
            MoveHighlight()
            
            if selected_square is not None:
                legal(selected_square)  
            
            check()
            checkmate()
            draw(board)
            
            pygame.display.flip()  #update display
            
        elif running and state == "Promotion":
            draw_board(images)  #Draw the board first
            PromotionMenu(images)  #Then draw the promotion menu on top
            pygame.display.flip()  #update display

        elif running and state == "GameOver":
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

    pygame.quit()
    sys.exit()

#conditional statement checks whether the file is being run as a script or being imported into another file
#this means without the statement the program would work fine unless being imported into another file

if __name__ == "__main__":
    result = second()
    if result == "quit":
        running = False
        pygame.quit()
        sys.exit()

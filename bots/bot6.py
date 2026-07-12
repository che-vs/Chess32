import chess
import random

def level6(board):
    points = {
        chess.PAWN: 100, #A pawn is a 100 centipawns
        chess.KNIGHT: 300, #A Knight is about 3 pawns
        chess.BISHOP: 320, #A Bishop is worth slightly more
        chess.ROOK: 500, #A rook is slightly worse than both a bishop and knight
        chess.QUEEN: 900, #A queen is around the value of two rooks
        chess.KING: 10000, #Liability
    }

    #MVVLVA = Most Valuable Victim and Least Valuable Aggressor
    #This allows for move ordering to make the most of alpha beta pruning
    #Without this it is up to luck if the best tree comes first or last losing the pruning benefits

    MVVLVA = { #MVVLVA concept learnt from chessprogrammingwiki
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    #These piece square tables were adapted from Simply in Dev Chess AI video
    #piece square tables give values to the squares the pieces are on, allowing for positional play
    #white piece-square tables
    pawn_mid = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -20, -20, 10, 10, 5,
        -5, 5, -10, 0, 0, -10, 5, -5,
        -10, 0, 0, 20, 20, 0, 0, -10,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    knight_mid = [
        -50, -60, -40, -30, -30, -40, -60, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -50, -60, -40, -30, -30, -40, -60, -50
    ]

    bishop_mid = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]

    rook_mid = [
        0, -50, 0, 15, 5, 15, -50, 0,
        -25, 0, 0, 0, 0, 0, 0, -25,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    queen_mid = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 5, 0, -10,
        -10, 0, 5, 5, 5, 5, 5, -10,
        -5, 0, 5, 5, 5, 5, 0, 0,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]

    king_mid = [
        20, 40, 10, 0, 0, 5, 40, 20,
        20, 20, -10, -30, -30, -10, 20, 20,
        -10, -20, -20, -30, -30, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]

    king_end = [ #separate table for endgame since king is strong piece in endgames
        -50, -30, -30, -30, -30, -30, -30, -50,
        -30, -30, 0, 0, 0, 0, -30, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -50, -40, -30, -20, -20, -30, -40, -50
    ]
    
    score = 0

    #black piece-square tables
    pawn_black = [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        -10, 0, 0, 20, 20, 0, 0, -10,
        -5, 5, -10, 0, 0, -10, 5, -5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ]

    knight_black = [
        -50, -60, -40, -30, -30, -40, -60, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -60, -40, -30, -30, -40, -60, -50
    ]

    bishop_black = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ]

    rook_black = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -25, 0, 0, 0, 0, 0, 0, -25,
        0, -50, 0, 15, 5, 15, -50, 0
    ]

    queen_black = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ]

    king_black = [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -30, -30, -20, -20, -20, -10,
        20, 20, -10, -30, -30, -10, 20, 20,
        20, 40, 10, 0, 0, 5, 40, 20
    ]

    king_black_end = [ #separate table for endgame since king is strong piece in endgames
        -50, -40, -30, -20, -20, -30, -40, -50,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -30, 0, 0, 0, 0, -30, -30,
        -50, -30, -30, -30, -30, -30, -30, -50
    ]

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5] #center of the board

    starting_squares = { #squares the pieces start on

        chess.WHITE: {
            chess.PAWN: [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2],
            chess.KNIGHT: [chess.B1, chess.G1],
            chess.BISHOP: [chess.C1, chess.F1],
            chess.ROOK: [chess.A1, chess.H1],
            chess.QUEEN: [chess.D1],
            chess.KING: [chess.E1]
        },
        
        chess.BLACK: {
            chess.PAWN: [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7],
            chess.KNIGHT: [chess.B8, chess.G8],
            chess.BISHOP: [chess.C8, chess.F8],
            chess.ROOK: [chess.A8, chess.H8],
            chess.QUEEN: [chess.D8],
            chess.KING: [chess.E8]
        }
    }

    def evaluate(board):
        score = 0
        #determine if we are in an endgame
        piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square))
        is_endgame = piece_count <= 10
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                #Material value
                material_value = points[piece.piece_type]
                
                #Positional value (adjust scaling as needed)
                positional_value = 0

                if piece.piece_type == chess.PAWN:
                    if piece.color == chess.WHITE:
                        table_value = pawn_mid[square]  #White pawn table
                    else:
                        table_value = pawn_black[square]  #Black pawn table

                elif piece.piece_type == chess.KNIGHT:
                    if piece.color == chess.WHITE:
                        table_value = knight_mid[square]  #White knight table
                    else:
                        table_value = knight_black[square]  #Black knight table

                elif piece.piece_type == chess.BISHOP:
                    if piece.color == chess.WHITE:
                        table_value = bishop_mid[square]  #White bishop table
                    else:
                        table_value = bishop_black[square]  #Black bishop table

                elif piece.piece_type == chess.ROOK:
                    if piece.color == chess.WHITE:
                        table_value = rook_mid[square]  #White rook table
                    else:
                        table_value = rook_black[square]  #Black rook table

                elif piece.piece_type == chess.QUEEN:
                    if piece.color == chess.WHITE:
                        table_value = queen_mid[square]  #White queen table
                    else:
                        table_value = queen_black[square]  #Black queen table

                elif piece.piece_type == chess.KING:
                    if is_endgame:
                        if piece.color == chess.WHITE:
                            table_value = king_end[square]  #White king endgame table
                        else:
                            table_value = king_black_end[square]  #Black king endgame table
                    else:
                        if piece.color == chess.WHITE:
                            table_value = king_mid[square]  #White king middlegame table
                        else:
                            table_value = king_black[square]  #Black king middlegame table

                positional_value = table_value

                #add to score
                if piece.color == chess.WHITE:
                    score += material_value + (positional_value / 3)
                else:
                    score -= material_value + (positional_value / 3)

###### Control of the Center ######
        
        for square in center_squares:
            white_attackers = len(board.attackers(chess.WHITE, square)) 
            black_attackers = len(board.attackers(chess.BLACK, square))
            score += 5 * (white_attackers - black_attackers)

###### Piece Development ###### 

        if not is_endgame: #only applies to the opening and middlegame
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece:
                    #improved evaluation score for piece development
                    if square not in starting_squares[piece.color].get(piece.piece_type, []):
                        if piece.color == chess.WHITE:
                            score += 5
                        else:
                            score -= 5    

###### King Safety ######
        
        if board.fullmove_number < 15: 
            if board.has_castling_rights(chess.WHITE):
                score += 10 #Bonus for still having castling rights
            else:
                white_king_square = board.king(chess.WHITE)
                if white_king_square in [chess.G1, chess.C1]:  #Kingside or Queenside
                    score += 50  
                elif white_king_square != chess.E1:  
                    score -= 30  #Penalty for moving king without castling
            
            if board.has_castling_rights(chess.BLACK):
                score -= 10
            else:
                black_king_square = board.king(chess.BLACK)
                if black_king_square in [chess.G8, chess.C8]:  
                    score -= 50  
                elif black_king_square != chess.E8:  
                    score += 30  
                    
        return score

    def move_score(move):
        score = 0

        #1. Captures (highest priority)
        if board.is_capture(move):
            if board.is_en_passant(move):
                victim_value = 1  #Pawn
            else:
                victim = board.piece_at(move.to_square) #piece being captured
                victim_value = MVVLVA.get(victim.piece_type, 0) if victim else 0 #look up victim value 

                aggressor = board.piece_at(move.from_square) #get the piece making capture
                aggressor_value = MVVLVA.get(aggressor.piece_type, 0) if aggressor else 0 #look up aggressor value

                score += 1000 + (victim_value * 10 - aggressor_value) #calculate capture score #prioritises low value pieces capturing high value ones

        #2. Promotions
        if move.promotion: 
            score += 900

        #3. Checks
        if board.gives_check(move):
            score += 100

        return score

    def minimax(board, depth, alpha, beta, maximizing): #credit to chessprogrammingwiki for teaching me how to create evaluation functions and minimax algorithms
        #base case: reached depth limit or game over
        if depth == 0 or board.is_game_over():
            return evaluate(board)
        
        if maximizing:
            best_value = -float("inf") #start with worst possible score for white
            for move in board.legal_moves:
                board_copy = board.copy() #test on copy of board
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, False) #recursively evaluate
                if current_value > best_value:
                    best_value = current_value
                #Alpha-beta pruning - removes other search trees if current tree is better in worst case scenario
                if best_value > alpha: #it removes the others because the AI always assumes the opponent plays the best move
                    alpha = best_value
                if alpha >= beta:
                    break  #prune the remaining moves
            return best_value
        else:
            best_value = float("inf") #worst possible score for black
            for move in board.legal_moves:
                board_copy = board.copy()
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, True)
                if current_value < best_value:
                    best_value = current_value

                #Alpha-beta pruning
                if best_value < beta:
                    beta = best_value
                if alpha >= beta:
                    break  #Prune the remaining moves
            return best_value

    def best_move(board, depth=4):
        best_move = None
        alpha = -float("inf")  
        beta = float("inf")

        #Sort moves by score (highest first)
        ordered_moves = sorted(board.legal_moves, key=move_score, reverse=True)
        
        if board.turn == chess.WHITE:
            #playing as white: maximize evaluation (white pieces are positive)
            best_value = -float("inf")#start with worst possible score
            for move in ordered_moves:
                board_copy = board.copy() #test on copy of board
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, False) #evaluate position with minimax
                
                if current_value > best_value:
                    best_value = current_value
                    best_move = move

                #update alpha at the root level for pruning
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        else:
            #playing as black: minimize evaluation (black pieces are negative)
            best_value = float("inf")
            for move in ordered_moves:
                board_copy = board.copy()
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, True)
                
                if current_value < best_value:
                    best_value = current_value
                    best_move = move

                beta = min(beta, best_value)
                if alpha >= beta:
                    break
                
        return best_move

    #main execution: find and return best move
    final_move = best_move(board)
    if final_move:
        return final_move
    return None

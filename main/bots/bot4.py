import chess

def level4(board):
    def evaluate(board):

        points = {
            chess.PAWN: 100, #A pawn is a 100 centipawns
            chess.KNIGHT: 300, #A Knight is about 3 pawns
            chess.BISHOP: 320, #A Bishop is worth slightly more
            chess.ROOK: 500, #A rook is slightly worse than both a bishop and knight
            chess.QUEEN: 900, #A queen is around the value of two rooks
            chess.KING: 10000, #Liability
        }

        from bots.tables import (
            pawn_mid, knight_mid, bishop_mid, rook_mid, queen_mid, king_mid, king_end,
            pawn_black, knight_black, bishop_black, rook_black, queen_black,
            king_black, king_black_end,
        )

        #determine if we are in an endgame
        piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square))
        is_endgame = piece_count <= 10
        
        for square in chess.SQUARES: #count all squares on board
            piece = board.piece_at(square)
            if piece:
                #Material value
                material_value = points[piece.piece_type]
                table_value = 0

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
                    score += material_value + (positional_value / 3.0)
                else:
                    score -= material_value + (positional_value / 3.0)
                    
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

    def best_move(board, depth=3):
        best_move = None
        alpha = -float("inf")  
        beta = float("inf") 
        
        if board.turn == chess.WHITE:
            #playing as white: maximise evaluation (white pieces are positive)
            best_value = -float("inf")#start with worst possible score
            for move in board.legal_moves:
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
            #playing as black: minimise evaluation (black pieces are negative)
            best_value = float("inf")
            for move in board.legal_moves:
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

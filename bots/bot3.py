import chess
import random

def level3(board):
    def evaluate_board(board):
        points = {
            chess.PAWN: 100, #A pawn is a 100 centipawns
            chess.KNIGHT: 300, #A Knight is about 3 pawns
            chess.BISHOP: 320, #A Bishop is worth slightly more
            chess.ROOK: 500, #A rook is slightly worse than both a bishop and knight
            chess.QUEEN: 900, #A queen is around the value of two rooks
            chess.KING: 10000, #Liability
        }
        
        score = 0
        for square in chess.SQUARES: #count all squares on board
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += points[piece.piece_type] #add points for maximising player (white)
                else:
                    score -= points[piece.piece_type] #subtract points for minimising player (black)
        return score

    def minimax(board, depth, alpha, beta, maximizing): #credit to chessprogrammingwiki for teaching me how to create evaluation functions and minimax algorithms
        #base case: reached depth limit or game over
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)
        
        if maximizing:
            best_value = -float("inf") #start with worst possible score for white
            for move in board.legal_moves:
                board_copy = board.copy() #test on copy of board
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, False) #recursively evaluate

                best_value = max(best_value, current_value)
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break  #Beta cutoff
            return best_value

        else:
            best_value = float("inf") #worst possible score for black
            for move in board.legal_moves:
                board_copy = board.copy()
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, True)

                best_value = min(best_value, current_value)
                beta = min(beta, best_value)
                if alpha >= beta:
                    break  #Alpha cutoff
            return best_value

    def best_move(board, depth=4):
        best_move = None
        alpha = -float("inf")  
        beta = float("inf") 
        
        if board.turn == chess.WHITE:
            best_value = -float("inf")
            for move in board.legal_moves:
                board_copy = board.copy()
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, alpha, beta, False)
                
                if current_value > best_value:
                    best_value = current_value
                    best_move = move
                    
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        else:
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

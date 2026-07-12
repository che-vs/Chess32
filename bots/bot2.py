import chess
import random

points = {          #each piece is worth a certain number of points which is used to calculate material advantage
    chess.PAWN: 100, #A pawn is a 100 centipawns
    chess.KNIGHT: 300, #A Knight is about 3 pawns
    chess.BISHOP: 320, #A Bishop is worth slightly more
    chess.ROOK: 500, #A rook is slightly worse than both a bishop and knight
    chess.QUEEN: 900, #A queen is around the value of two rooks
    chess.KING: 10000, #Liability
}

def level2(board):
    def evaluate_board(board):
        score = 0
        for square in chess.SQUARES: #count all squares on board
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += points[piece.piece_type] #add points for maximising player (white)
                else:
                    score -= points[piece.piece_type] #subtract points for minimising player (black)
        return score

    def minimax(board, depth, maximizing): #credit to chessprogrammingwiki for teaching me how to create evaluation functions and minimax algorithms
        #base case: reached depth limit or game over
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)
        
        if maximizing:
            best_value = -float("inf") #start with worst possible score for white
            for move in board.legal_moves:
                #make a move on a copy of the board so the player doesnt see 
                board_copy = board.copy()
                board_copy.push(move)
                #recursively evaluate
                current_value = minimax(board_copy, depth - 1, False)
                #update if this move is better
                if current_value > best_value:
                    best_value = current_value
            return best_value
        else:
            best_value = float("inf") #worst possible score for black
            for move in board.legal_moves:
                board_copy = board.copy()
                board_copy.push(move)
                current_value = minimax(board_copy, depth - 1, True)
                if current_value < best_value:
                    best_value = current_value
            return best_value

    def best_move(board, depth=3):
        best_move = None
        best_value = -float("inf") #start with worst possible score
        
        for move in board.legal_moves:
            board_copy = board.copy() #test on copy of board
            board_copy.push(move)
            current_value = minimax(board_copy, depth - 1, False) #evaluate position with minimax

            if board.turn == chess.WHITE:
                if board.is_capture(move): #points for piece captures
                    current_value += points[(board.piece_at(move.to_square)).piece_type]
            else:
                if board.is_capture(move): #points for piece captures
                    current_value -= points[(board.piece_at(move.to_square)).piece_type]

            #update if this move is better
            if current_value > best_value or (current_value == best_value and random.random() > 0.5):
                best_value = current_value
                best_move = move
                
        return best_move

    #main execution: find and return best move
    final_move = best_move(board)
    if final_move:
        return final_move
    return None

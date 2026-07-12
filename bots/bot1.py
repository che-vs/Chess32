import random

def level1(board):
    legal_moves = list(board.legal_moves) #list of legal moves
    if legal_moves:
        move = random.choice(legal_moves) #random move from list
        return move #plays the move
    return None

import chess
import random
import time
import chess.polyglot
    
def level8(board):
    try:
        with chess.polyglot.open_reader("codekiddy.bin") as reader: #codekiddy.bin is an opening database in polygot format
            entries = list(reader.find_all(board))                  #Downloaded from a github repository 
            if entries:                                             #Author unknown
                return random.choice(entries).move
    except:
        pass
    
    points = {
        chess.PAWN: 100, #A pawn is a 100 centipawns
        chess.KNIGHT: 300, #A Knight is about 3 pawns
        chess.BISHOP: 320, #A Bishop is worth slightly more
        chess.ROOK: 500, #A rook is slightly worse than both a bishop and knight
        chess.QUEEN: 900, #A queen is around the value of two rooks
        chess.KING: 1000000, #Liability
    }

    #MVVLVA = Most Valuable Victim and Least Valuable Aggressor
    #This allows for move ordering to make the most of alpha beta pruning
    #Without this it is up to luck if the best tree comes first or last losing the pruning benefits

    MVVLVA = { #MVVLVA concept learnt from chessprogrammingwiki
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 320,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 200000
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
        
        if not is_endgame: 
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
                victim_value = MVVLVA[chess.PAWN] 
                attacker_value = MVVLVA[chess.PAWN]
            else:
                victim = board.piece_at(move.to_square) #piece being captured
                attacker = board.piece_at(move.from_square) #piece capturing

                victim_value = MVVLVA[victim.piece_type] if victim else 0 #value of victim
                attacker_value = MVVLVA[attacker.piece_type] if victim else 0 #value of attacker

                score += (victim_value * 10) - attacker_value #calculate capture score #prioritises low value pieces capturing high value ones

            score += 50

            #Static Exchange Evaluation - Reduces blunders
            board.push(move)

            #After push the board.turn has switched so attackers are now board.turn
            if board.is_attacked_by(board.turn, move.to_square):
                score -= attacker_value * 2  #big penalty for hanging the piece

            board.pop()

        #2. Promotions
        if move.promotion: 
            score += 800

        #3. Checks
        if board.gives_check(move):
            score += 30

        return score

    def quiescence(board, alpha, beta, maximizing, start_time, time_lim): #Quiescence search concept learnt from Simply in Dev Chess AI video
        #Quiescence search - only searches captures, checks, and promotions to avoid the horizon effect and find quiet positions for evaluation

        if time.time() - start_time > time_lim:
            return evaluate(board)

        stand_pat = evaluate(board) #stand pat means do nothing
        
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -100000
            else:
                return 100000
        
        if board.is_game_over():
            return 0
        
        if maximizing:
            #do nothing if current position is already good enough
            if stand_pat >= beta:
                return beta  #Beta cutoff
            if stand_pat > alpha:
                alpha = stand_pat
                
            #Generate only tactical moves (captures, checks, promotions)
            tactical_moves = []
            for move in board.legal_moves:
                if (board.is_capture(move) or 
                    board.gives_check(move) or 
                    move.promotion):
                    tactical_moves.append(move)
            
            #If no tactical moves, return stand_pat evaluation
            if not tactical_moves:
                return stand_pat
            
            #Search tactical moves
            for move in sorted(tactical_moves, key=move_score, reverse=True):
                if time.time() - start_time > time_lim:
                    break
                board.push(move)
                score = quiescence(board, alpha, beta, False, start_time, time_lim)
                board.pop()
                
                if score >= beta:
                    return beta  #Beta cutoff
                if score > alpha:
                    alpha = score
                    
            return alpha
            
        else:  #Minimizing player
            #Stand pat for minimizing player
            if stand_pat <= alpha:
                return alpha  #Alpha cutoff
            if stand_pat < beta:
                beta = stand_pat
                
            #Generate only tactical moves
            tactical_moves = []
            for move in board.legal_moves:
                if (board.is_capture(move) or 
                    board.gives_check(move) or 
                    move.promotion):
                    tactical_moves.append(move)
            
            if not tactical_moves:
                return stand_pat
            
            #Search tactical moves
            for move in sorted(tactical_moves, key=move_score, reverse=True):
                if time.time() - start_time > time_lim:
                    break
                board.push(move)
                score = quiescence(board, alpha, beta, True, start_time, time_lim)
                board.pop()
                
                if score <= alpha:
                    return alpha  #Alpha cutoff
                if score < beta:
                    beta = score
                    
            return beta

    transposition_table = {} #holds positions in cache #Transposition Table concept learnt from chessprogrammingwiki    

    def minimax(board, depth, alpha, beta, maximizing, start_time, time_lim): #credit to chessprogrammingwiki for teaching me how to create evaluation functions and minimax algorithms
        if time.time() - start_time > time_lim:
            return evaluate(board)

        board_fen = board.fen()  #Use FEN as a key
    
        if board_fen in transposition_table:
            entry = transposition_table[board_fen]
            if entry["depth"] == depth: #if depth of the position evaluated in transposition table is equal or higher
                return entry["value"] #return value 
        
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -100000000 - depth 
            else:
                return 100000000 + depth   
        
        if board.is_game_over():  #Draws
            return 0

        if depth == 0:
            return quiescence(board, alpha, beta, maximizing, start_time, time_lim)
        
        legal_moves_list = sorted(board.legal_moves, key=move_score, reverse=True)
        
        if maximizing:
            best_value = -float("inf")
            for move in legal_moves_list:
                if time.time() - start_time > time_lim:
                    break
                board.push(move)
                current_value = minimax(board, depth - 1, alpha, beta, False, start_time, time_lim)
                board.pop()
                
                if current_value > best_value:
                    best_value = current_value

                #Alpha-beta pruning
                if best_value > alpha:
                    alpha = best_value
                if alpha >= beta:
                    break  #prune the remaining moves

            transposition_table[board_fen] = { #stores the position
                "value": best_value, #stores the value of the position
                "depth": depth       #stores the depth of the position
            }
                
            return best_value

        else:
            best_value = float("inf")
            for move in legal_moves_list:
                if time.time() - start_time > time_lim:
                    break
                board.push(move)
                current_value = minimax(board, depth - 1, alpha, beta, True, start_time, time_lim)
                board.pop()
                
                if current_value < best_value:
                    best_value = current_value

                #Alpha-beta pruning
                if best_value < beta:
                    beta = best_value
                if alpha >= beta:
                    break  #Prune the remaining moves

            transposition_table[board_fen] = {
                "value": best_value,
                "depth": depth
            }
                
            return best_value

    def best_move(board, max_depth=4):  #Increased max_depth since we have time management
        time_lim = 15
        start_time = time.time()
        
        if len(transposition_table) > 10000: #clears every 10000 items
            transposition_table.clear()
                    
        best_move_found = None
        best_value = 0
        
        #Check for immediate checkmate first
        legal_moves_list = sorted(board.legal_moves, key=move_score, reverse=True)
        for move in legal_moves_list:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move  #Immediately return the checkmate move
            board.pop()

        #Sort moves by score (highest first)
        ordered_moves = sorted(legal_moves_list, key=move_score, reverse=True)
        
        #Iterative deepening - search at increasing depths
        for depth in range(1, max_depth + 1):
            if time.time() - start_time > time_lim:
                break  #Stop if we have exceeded time limit
                
            current_best_move = None #aspiration windows to narrow down target range for the current search
            if depth == 1:
                alpha = -float("inf")
                beta = float("inf")
            else:
                window = 50
                alpha = best_value - window
                beta = best_value + window

            #principal variation move ordering searches the best move from previous depth first
            if best_move_found and best_move_found in ordered_moves:
                ordered_moves.remove(best_move_found)
                ordered_moves.insert(0, best_move_found)
            
            if board.turn == chess.WHITE:
                current_best_value = -float("inf")
                for move in ordered_moves:
                    if time.time() - start_time > time_lim: #returns best move found so far if time limit exceeded
                        break
                        
                    board.push(move)
                    current_value = minimax(board, depth - 1, alpha, beta, False, start_time, time_lim)
                    board.pop()
                    
                    if current_value > current_best_value:
                        current_best_value = current_value
                        current_best_move = move
                    
                    alpha = max(alpha, current_best_value)
                    if alpha >= beta:
                        break

                #research if we fall outside of aspiration windows
                if depth > 1 and (current_best_value <= best_value - 50 or current_best_value >= best_value + 50):
                    alpha = -float("inf")
                    beta = float("inf")
                    current_best_value = -float("inf")
                    for move in ordered_moves:
                        if time.time() - start_time > time_lim:
                            break
                        board.push(move)
                        current_value = minimax(board, depth - 1, alpha, beta, False, start_time, time_lim)
                        board.pop()
                        if current_value > current_best_value:
                            current_best_value = current_value
                            current_best_move = move
                        alpha = max(alpha, current_best_value)
                        if alpha >= beta:
                            break
                        
            else:
                current_best_value = float("inf")
                for move in ordered_moves:
                    if time.time() - start_time > time_lim:
                        break
                        
                    board.push(move)
                    current_value = minimax(board, depth - 1, alpha, beta, True, start_time, time_lim)
                    board.pop()
                    
                    if current_value < current_best_value:
                        current_best_value = current_value
                        current_best_move = move
                    
                    beta = min(beta, current_best_value)
                    if alpha >= beta:
                        break

                #research if we fall outside the aspiration window
                if depth > 1 and (current_best_value <= best_value - 50 or current_best_value >= best_value + 50):
                    alpha = -float("inf")
                    beta = float("inf")
                    current_best_value = float("inf")
                    for move in ordered_moves:
                        if time.time() - start_time > time_lim:
                            break
                        board.push(move)
                        current_value = minimax(board, depth - 1, alpha, beta, True, start_time, time_lim)
                        board.pop()
                        if current_value < current_best_value:
                            current_best_value = current_value
                            current_best_move = move
                        beta = min(beta, current_best_value)
                        if alpha >= beta:
                            break
            
            #Only update if a better move is found at this depth
            if current_best_move:
                best_move_found = current_best_move
                best_value = current_best_value
        
        return best_move_found if best_move_found else ordered_moves[0] if ordered_moves else None
    
    final_move = best_move(board)
    if final_move:
        return final_move
    return None

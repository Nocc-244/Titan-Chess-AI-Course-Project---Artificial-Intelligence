import chess

# ==============================================================================
# 1. HỆ THỐNG ĐÁNH GIÁ MA TRẬN VỊ TRÍ GỐC (ĐÃ CHUẨN HÓA ĐẢO CHIỀU ĐEN / TRẮNG)
# ==============================================================================
PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 325, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  0, 10, 10,  0,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
      0,  0,  0,  5,  5,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
      0,  0,  5,  5,  5,  5,  0, -5,
     -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MIDDLE_TABLE = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30
]

KING_END_TABLE = [
    -50,-30,-30,-30,-30,-30,-30,-50,
    -30,-10,  0,  0,  0,  0,-10,-30,
    -30,  0, 20, 30, 30, 20,  0,-30,
    -30,  0, 30, 40, 40, 30,  0,-30,
    -30,  0, 30, 40, 40, 30,  0,-30,
    -30,  0, 20, 30, 30, 20,  0,-30,
    -30,-10,  0,  0,  0,  0,-10,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

PIECE_TABLES = {
    chess.PAWN: PAWN_TABLE, chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE, chess.ROOK: ROOK_TABLE, chess.QUEEN: QUEEN_TABLE
}

def is_endgame(board):
    heavy_pieces = len(board.pieces(chess.QUEEN, chess.WHITE)) + \
                   len(board.pieces(chess.QUEEN, chess.BLACK)) + \
                   len(board.pieces(chess.ROOK, chess.WHITE)) + \
                   len(board.pieces(chess.ROOK, chess.BLACK))
    return heavy_pieces <= 2

def evaluate_board(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fifty_moves(): 
        return 0
        
    score = 0
    endgame = is_endgame(board)
    
    # --- PHẦN 1: BẮT BUỘC TÍNH ĐIỂM MA TRẬN TĨNH ---
    for piece_type, value in PIECE_VALUES.items():
        # Quân Trắng: Đọc chỉ số xuôi theo ma trận gốc (square)
        for square in board.pieces(piece_type, chess.WHITE):
            score += value
            if piece_type == chess.KING:
                score += KING_MIDDLE_TABLE[square] if not endgame else KING_END_TABLE[square]
            elif piece_type in PIECE_TABLES:
                score += int(PIECE_TABLES[piece_type][square] * (0.6 if not endgame else 1.0))
                
        # Quân Đen: Đọc ngược hướng ma trận gốc, phải dùng square_mirror
        for square in board.pieces(piece_type, chess.BLACK):
            score -= value
            b_idx = chess.square_mirror(square)
            if piece_type == chess.KING:
                score -= KING_MIDDLE_TABLE[b_idx] if not endgame else KING_END_TABLE[b_idx]
            elif piece_type in PIECE_TABLES:
                score -= int(PIECE_TABLES[piece_type][b_idx] * (0.6 if not endgame else 1.0))

    # --- GIỮ NGUYÊN CÁC CHỈ SỐ LỢI THẾ TĨNH BỔ TRỢ CỦA BỒ ---
    if not endgame:
        if board.has_kingside_castling_rights(chess.WHITE): score += 40
        if board.has_queenside_castling_rights(chess.WHITE): score += 30
        if board.has_kingside_castling_rights(chess.BLACK): score -= 40
        if board.has_queenside_castling_rights(chess.BLACK): score -= 30
        
        if board.king(chess.WHITE) != chess.E1:
            if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
                score -= 60
        if board.king(chess.BLACK) != chess.E8:
            if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
                score += 60

    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2: score += 35
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2: score -= 35
    
    mobility_weight = 2
    if board.turn == chess.WHITE:
        score += board.legal_moves.count() * mobility_weight
    else:
        score -= board.legal_moves.count() * mobility_weight
            
    return score

# ==============================================================================
# GIỮ NGUYÊN HOÀN TOÀN CƠ CHẾ SẮP XẾP NƯỚC ĐI VÀ ALPHA-BETA
# ==============================================================================
def score_move(board, move):
    score = 0
    if board.gives_check(move):
        score += 5000
        
    if board.is_capture(move):
        from_piece = board.piece_at(move.from_square)
        to_piece = board.piece_at(move.to_square)
        if from_piece and to_piece:
            score += 1000 * PIECE_VALUES.get(to_piece.piece_type, 0) - PIECE_VALUES.get(from_piece.piece_type, 0)
        else:
            score += 1000
            
    if move.promotion:
        score += 9000
    return score

def quiescence_search(board, alpha, beta, is_maximizing):
    stand_pat = evaluate_board(board)
    if is_maximizing:
        if stand_pat >= beta: return beta
        if alpha < stand_pat: alpha = stand_pat
        capture_moves = list(board.generate_legal_captures())
        capture_moves.sort(key=lambda m: score_move(board, m), reverse=True)
        for move in capture_moves:
            board.push(move)
            score = quiescence_search(board, alpha, beta, False)
            board.pop()
            if score >= beta: return beta
            if score > alpha: alpha = score
        return alpha
    else:
        if stand_pat <= alpha: return alpha
        if beta > stand_pat: beta = stand_pat
        capture_moves = list(board.generate_legal_captures())
        capture_moves.sort(key=lambda m: score_move(board, m), reverse=True)
        for move in capture_moves:
            board.push(move)
            score = quiescence_search(board, alpha, beta, True)
            board.pop()
            if score <= alpha: return alpha
            if score < beta: beta = score
        return beta

def alpha_beta(board, depth, alpha, beta, is_maximizing, history_set):
    if depth <= 0:
        if board.is_check(): depth += 1
        else: return quiescence_search(board, alpha, beta, is_maximizing)
            
    if board.is_game_over():
        if board.is_checkmate():
            return -100000 - depth if board.turn == chess.WHITE else 100000 + depth
        return 0 

    if history_set and board.can_claim_threefold_repetition():
        return 0

    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda m: score_move(board, m), reverse=True)

    if is_maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            board.push(move)
            evaluation = alpha_beta(board, depth - 1, alpha, beta, False, history_set)
            board.pop()
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, max_eval)
            if beta <= alpha: break 
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            evaluation = alpha_beta(board, depth - 1, alpha, beta, True, history_set)
            board.pop()
            min_eval = min(min_eval, evaluation)
            beta = min(beta, min_eval)
            if beta <= alpha: break 
        return min_eval

# ==============================================================================
# HÀM ĐIỀU PHỐI CHÍNH
# ==============================================================================
def find_best_move(board, depth, history, ai_color):
    legal_moves = list(board.legal_moves)
    if not legal_moves: return None
        
    legal_moves.sort(key=lambda m: score_move(board, m), reverse=True)
    best_move = legal_moves[0]
    alpha = -float('inf')
    beta = float('inf')
    
    history_set = True if history and len(history) > 1 else False
    
    if ai_color == chess.WHITE:
        best_value = -float('inf')
        for move in legal_moves:
            board.push(move)
            # Đi Trắng (Maximizing) -> Nước tiếp theo của Đen phải là Minimizing (False)
            board_value = alpha_beta(board, depth - 1, alpha, beta, False, history_set)
            board.pop()
            if board_value > best_value:
                best_value = board_value
                best_move = move
            alpha = max(alpha, best_value)
    else:
        best_value = float('inf')
        for move in legal_moves:
            board.push(move)
            # Đi Đen (Minimizing) -> Nước tiếp theo của Trắng phải là Maximizing (True)
            board_value = alpha_beta(board, depth - 1, alpha, beta, True, history_set)
            board.pop()
            if board_value < best_value:
                best_value = board_value
                best_move = move
            beta = min(beta, best_value)
            
    return best_move
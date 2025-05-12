from abc import ABC, abstractmethod
import random

import chess


class Agent(ABC):
    """An `Agent` decides what move to make on a given board."""

    @abstractmethod
    def pick_move(self, board: chess.Board) -> chess.Move: ...


class RandomAgent(Agent):
    """A `RandomAgent` always chooses a random legal move."""

    def pick_move(self, board: chess.Board) -> chess.Move:
        options = list(board.generate_legal_moves())
        return random.choice(options)


class MinMaxABAgent(Agent):
    def pick_move(self, board):
        return self.minimax(board, depth=3)[0]

    def score_board(self, board):
        score = 0

        if board.is_checkmate():
            return -9999 if board.turn else 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        check_bonus = 0.5
        if board.is_check():
            if board.turn:
                score -= check_bonus
            else:
                score += check_bonus

        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 4,
            chess.ROOK: 5,
            chess.QUEEN: 10,
            chess.KING: 0
        }

        #These are all upside down when viewing, meaning the first row is rank 1, then row 2 is rank 2...
        placement_score = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.25, 0.25, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.25, 0.25, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]

        mobility_weight =   {chess.PAWN:  .2,
                            chess.KNIGHT: .1,
                            chess.BISHOP: .1,
                            chess.ROOK:   .05,
                            chess.QUEEN:  .02,
                            chess.KING:   0}
        for square, piece in board.piece_map().items():
            value = piece_values[piece.piece_type]

            if piece.color == chess.WHITE:
                score += value
                
                score += placement_score[square]


            else:  # black piece
                score -= value
                # mirror the square so black uses the same table
                score += placement_score[square]

            mobility = len(board.attacks(square))
            # weight by piece value (so queen’s moves matter more) and global factor
            mob_bonus = mobility * mobility_weight[piece.piece_type]

            if piece.color == chess.WHITE:
                score += mob_bonus
            else:
                score -= mob_bonus

        return score
        
        

    
    def minimax(self, board, depth, alpha = -float("inf"), beta = float("inf")):
        if depth == 0 or board.is_game_over():
            return None, self.score_board(board)

        best_move = random.choice([move for move in board.legal_moves])
        maximizing_player = board.turn

        if maximizing_player:
            max_score = -float("inf")
            for move in board.legal_moves:
                board.push(move)
                score = self.minimax(board, depth - 1, alpha, beta)[1]
                board.pop()

                if max_score < score:
                    best_move = move
                    max_score  = score
            
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            #print(max_score)
            return best_move, max_score
        else:
            min_score = float("inf")
            for move in board.legal_moves:
                board.push(move)
                score = self.minimax(board, depth - 1, alpha, beta)[1]
                board.pop()
                
                if min_score > score:
                    best_move = move
                    min_score  = score

                beta = min(beta, score)
                if beta <= alpha:
                    break
            #print(min_score)
            return best_move, min_score

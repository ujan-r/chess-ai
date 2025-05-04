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

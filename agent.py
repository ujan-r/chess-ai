from abc import ABC, abstractmethod

import chess


class Agent(ABC):
    """An `Agent` decides what move to make on a given board."""

    @abstractmethod
    def pick_move(self, board: chess.Board) -> chess.Move: ...

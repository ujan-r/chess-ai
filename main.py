import chess
import time

from agent import Agent, RandomAgent
from ui import RemoteRenderer


def play(
    white: Agent,
    black: Agent,
    board: chess.Board | None = None,
) -> chess.Outcome:
    if board is None:
        board = chess.Board()

    with RemoteRenderer(('localhost', 3000)) as renderer:
        while not board.is_game_over():
            agent = white if board.turn is chess.WHITE else black
            move = agent.pick_move(board)
            board.push(move)
            renderer.send(move)
            time.sleep(0.1)

    result = board.outcome()
    assert result is not None
    return result


white = RandomAgent()
black = RandomAgent()
outcome = play(white, black)
match outcome.winner:
    case chess.WHITE:
        print('White wins!')
    case chess.BLACK:
        print('Black wins!')
    case _:
        print("It's a draw!")

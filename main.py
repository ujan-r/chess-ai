import chess

from agent import Agent, RandomAgent


def play(
    white: Agent,
    black: Agent,
    board: chess.Board | None = None,
) -> chess.Outcome:
    if board is None:
        board = chess.Board()

    while not board.is_game_over():
        agent = white if board.turn is chess.WHITE else black
        move = agent.pick_move(board)
        board.push(move)

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

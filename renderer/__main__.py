import argparse
import socket

import chess


parser = argparse.ArgumentParser()
parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=3000,
    help='the port to listen on (default: %(default)s)',
)

args = parser.parse_args()
port = args.port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', port))
    s.listen()
    print('Listening on port', port)

    conn, addr = s.accept()
    with conn:
        board = chess.Board()
        print(board)
        while True:
            data = conn.recv(8).decode()
            move = chess.Move.from_uci(data)
            board.push(move)
            print()
            print(board)

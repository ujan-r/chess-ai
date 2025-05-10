import argparse
import functools
import os
import socket

import chess
import pygame as pg


BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
DARK = pg.Color(100, 120, 200)
LIGHT = pg.Color(200, 200, 220)


def draw_board(board: chess.Board, window: pg.Surface):
    height = window.height // 8
    width = window.width // 8

    for square in range(64):
        row, col = divmod(square, 8)
        x, y = col * width, row * height

        color = DARK if (row + col) % 2 else LIGHT
        pg.draw.rect(window, color, (x, y, width, height))

        if (piece := board.piece_at(8 * (7 - row) + col)) is not None:
            sprite = get_asset(piece)
            window.blit(sprite, (x, y))


@functools.cache
def get_asset(piece: chess.Piece) -> pg.Surface:
    match piece:
        case chess.Piece(chess.PAWN, chess.WHITE):
            name = 'pawn-white'
        case chess.Piece(chess.KNIGHT, chess.WHITE):
            name = 'knight-white'
        case chess.Piece(chess.BISHOP, chess.WHITE):
            name = 'bishop-white'
        case chess.Piece(chess.ROOK, chess.WHITE):
            name = 'rook-white'
        case chess.Piece(chess.QUEEN, chess.WHITE):
            name = 'queen-white'
        case chess.Piece(chess.KING, chess.WHITE):
            name = 'king-white'
        case chess.Piece(chess.PAWN, chess.BLACK):
            name = 'pawn-black'
        case chess.Piece(chess.KNIGHT, chess.BLACK):
            name = 'knight-black'
        case chess.Piece(chess.BISHOP, chess.BLACK):
            name = 'bishop-black'
        case chess.Piece(chess.ROOK, chess.BLACK):
            name = 'rook-black'
        case chess.Piece(chess.QUEEN, chess.BLACK):
            name = 'queen-black'
        case chess.Piece(chess.KING, chess.BLACK):
            name = 'king-black'
        case _:
            raise ValueError('unknown piece:', piece)

    path = os.path.join('renderer', 'assets', name + '.svg')
    return pg.image.load_sized_svg(path, (64, 64))

board = chess.Board()

pg.init()
window = pg.display.set_mode((512, 512))
pg.display.set_caption('Chess')

window.fill(BLACK)
pg.display.update()

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
    conn.setblocking(False)
    with conn:
        draw_board(board, window)
        running = True
        while running:
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    break
            try:
                data = conn.recv(8)
            except socket.error:
                # Our socket is non-blocking, so we can just continue if there's
                # nothing to read.
                continue

            # The client won't be sending any more data; we're done.
            if not data:
                break

            move = chess.Move.from_uci(data.decode())
            board.push(move)
            draw_board(board, window)

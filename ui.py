import socket

import chess


class RemoteRenderer:
    def __init__(self, address):
        self.address = address

    def send(self, move: chess.Move):
        data = move.uci().ljust(6, '\0').encode()
        assert len(data) == 6
        self.conn.sendall(data)

    def __enter__(self):
        self.conn = socket.socket()
        self.conn.connect(self.address)
        return self

    def __exit__(self, *_):
        self.conn.close()

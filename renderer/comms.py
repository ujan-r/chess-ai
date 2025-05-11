from dataclasses import dataclass, field
import socket

import chess


@dataclass
class MoveReader:
    connection: socket.socket
    buffer: bytearray = field(default_factory=bytearray)

    def __post_init__(self):
        if self.connection.getblocking():
            msg = 'wanted a non-blocking connection but received a blocking one'
            raise ValueError(msg)

    def read(self) -> chess.Move | None:
        try:
            msg = self.connection.recv(6)
            if not msg:
                raise ConnectionAbortedError
            else:
                self.buffer.extend(msg)
        except socket.error:
            pass

        if len(self.buffer) >= 6:
            data = self.buffer[:6]
            self.buffer = self.buffer[6:]
            return chess.Move.from_uci(data.decode().strip())

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

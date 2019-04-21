import threading
import socket

from events import EventHandler


class SocketServer:
    def __init__(self):
        self.server = None  # type: socket.socket
        self.messages = []
        self.on_received = EventHandler(self)
        self.is_running = False
        self.connects = []

    def start_server(self, host: str = '0.0.0.0', port: int = 8080, backlog: int = 1):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(backlog)
        self.is_running = True

        accept_thread = threading.Thread(target=self.accept)
        accept_thread.setDaemon(True)
        accept_thread.start()

        send_thread = threading.Thread(target=self.send)
        send_thread.setDaemon(True)
        send_thread.start()

    def close(self):
        self.is_running = False
        for conn in self.connects:
            conn.close()
        self.connects.clear()
        self.server.close()

    def accept(self):
        while self.is_running:
            conn, addr = self.server.accept()
            self.connects.append(conn)
            receive_thread = threading.Thread(target=self.receive, args=[conn])
            receive_thread.setDaemon(True)
            receive_thread.start()

    def send(self):
        while self.is_running:
            for conn in self.connects:
                if len(self.messages) > 0:
                    msgs = self.messages.copy()
                    self.messages.clear()
                    for msg in msgs:
                        conn.sendall(msg.encode())

    def receive(self, conn):
        while self.is_running:
            data = conn.recv(4096)
            if not data: break
            self.on_received(str(data, encoding="utf8"))
        conn.close()
        self.connects.remove(conn)

    def send_message(self, msg: str):
        self.messages.append(msg)

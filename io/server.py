import socket
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import Hyphen

class Server:
    def __init__(
        self,
        hyphen: 'Hyphen',
        host_addr: str = "10.10.10.12",
        port: int = 65432, 
    ) -> None:
        self.HOST = host_addr
        self.PORT = port
        self.Hyphen = hyphen
    
    def run_server(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print("Started Server")

            connection, addr = s.accept()
            with connection:
                print(f"Connected by: {addr}")
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break

                    print(f"Received: {data.decode()}")
                    connection.sendall(f"Showing on screen: {data}".encode())
                    self.Hyphen.display_message(data.decode())

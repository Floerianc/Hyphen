import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        raise Exception(str(e) + "\n1. Perhaps the server hasn't even started yet?\n2. You started the client before the server started.\n3. The server is trying to listen on a address that already is in use.")
    
    while True:
        msg = input("Message to show on screen\n> ")
        if msg == "exit":
            break
        else:
            s.sendall(msg.encode())
            data = s.recv(1024)
            print(f"Server-side msg: {data.decode()}")
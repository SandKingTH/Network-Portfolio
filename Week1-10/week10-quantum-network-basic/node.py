import socket
import threading
import time
import sys
from config import HOST, BUFFER_SIZE, UPDATE_INTERVAL
from token import Token

BASE_PORT = int(sys.argv[1])
PEER_PORTS = [int(p) for p in sys.argv[2:]]

token_queue = []

def send_token(peer_port, token):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))
        s.sendall(token.message.encode())
        s.close()
        print(f"[NODE {BASE_PORT}] Sent token to {peer_port}")
        return True
    except:
        print(f"[NODE {BASE_PORT}] Failed to send to {peer_port}")
        return False

def forward_loop():
    while True:
        for token in token_queue[:]:
            for peer in PEER_PORTS:
                if send_token(peer, token):
                    token_queue.remove(token)
                    break
        time.sleep(UPDATE_INTERVAL)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()
    print(f"[NODE {BASE_PORT}] Listening...")
    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        token = Token(data)
        message = token.read_token()
        if message:
            print(f"[NODE {BASE_PORT}] Consumed token: {message}")
            # ไม่ forward ต่อ → token ถูก consume แล้ว
        else:
            print(f"[NODE {BASE_PORT}] Token invalid/used")
        conn.close()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    forward_thread = threading.Thread(target=forward_loop, daemon=True)
    server_thread.start()
    forward_thread.start()
    while True:
        msg = input(f"[NODE {BASE_PORT}] Enter message (or blank to exit): ")
        if not msg:
            break
        token_queue.append(Token(msg))

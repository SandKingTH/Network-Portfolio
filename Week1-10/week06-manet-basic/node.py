# node.py
import socket
import threading
import random
import time
from config import HOST, BASE_PORT, BUFFER_SIZE, NEIGHBORS, FORWARD_PROBABILITY, TTL
neighbor_table = set(NEIGHBORS)
def forward_message(message, ttl, exclude_port=None):
    for peer_port in neighbor_table:
        if peer_port == exclude_port:
            continue
        if random.random() > FORWARD_PROBABILITY:
            print(f"[NODE {BASE_PORT}] Decided NOT to forward to {peer_port} (Probability)")
            continue
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2) 
            s.connect((HOST, peer_port))
            payload = f"{message}|{ttl}|{BASE_PORT}"
            s.sendall(payload.encode())
            s.close()
            print(f"[NODE {BASE_PORT}] Forwarded to {peer_port} (TTL left: {ttl})")
        except (ConnectionRefusedError, socket.timeout):
            print(f"[NODE {BASE_PORT}] Peer {peer_port} is offline")

def handle_incoming(conn, addr):
    try:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data: return
        msg, ttl_str, sender_port = data.split('|')
        ttl = int(ttl_str)
        sender_port = int(sender_port)
        print(f"\n[NODE {BASE_PORT}] Received: '{msg}' from Port {sender_port} (TTL={ttl})")
        if ttl > 0:
            threading.Thread(target=forward_message, args=(msg, ttl - 1, sender_port)).start()
            
    except Exception as e:
        print(f"Error handling data: {e}")
    finally:
        conn.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, port))
    server.listen(5)
    print(f"[NODE {port}] Server started. Listening for neighbors...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_incoming, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    t = threading.Thread(target=start_server, args=(BASE_PORT,), daemon=True)
    t.start()
    time.sleep(1)
    print(f"--- Node {BASE_PORT} is ready ---")
    print("Commands: 'send <message>' to start gossip, 'exit' to quit")
    while True:
        try:
            cmd = input(f"[NODE {BASE_PORT}] > ")
            if cmd.startswith("send "):
                msg_content = cmd[5:]
                forward_message(msg_content, TTL)
            elif cmd == "exit":
                break
        except KeyboardInterrupt:
            break

    print("Node shutting down...")
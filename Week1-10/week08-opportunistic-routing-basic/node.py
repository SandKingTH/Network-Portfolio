import socket
import threading
import time
import sys
from config import HOST, BUFFER_SIZE, FORWARD_THRESHOLD, UPDATE_INTERVAL
from delivery_table import DeliveryTable

BASE_PORT = int(sys.argv[1])
PEER_PORTS = [int(p) for p in sys.argv[2:]]

delivery_table = DeliveryTable()
message_queue = []

def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))
        s.sendall(message.encode())
        s.close()
        print(f"[NODE {BASE_PORT}] Sent: {message} to {peer_port}")
        return True
    except (ConnectionRefusedError, socket.timeout):
        return False

def forward_loop():
    while True:
        candidates = delivery_table.get_best_candidates(FORWARD_THRESHOLD)
        for msg in message_queue[:]:
            for peer in candidates:
                if send_message(peer, msg):
                    message_queue.remove(msg)
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
        print(f"[NODE {BASE_PORT}] Received: {data}")
        message_queue.append(data)
        conn.close()

if __name__ == "__main__":
    # เติม peer ทุกตัวลง delivery_table ด้วย prob=1.0
    for peer in PEER_PORTS:
        delivery_table.update_probability(peer, 1.0)

    # เริ่ม server และ forwarding thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    forward_thread = threading.Thread(target=forward_loop, daemon=True)
    server_thread.start()
    forward_thread.start()
    while True:
        msg = input(f"[NODE {BASE_PORT}] Enter message (or blank to exit): ")
        if not msg:
            break
        message_queue.append(msg)

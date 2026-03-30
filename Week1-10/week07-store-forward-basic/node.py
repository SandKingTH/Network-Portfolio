# node.py

import socket
import threading
import time
import sys
from config import HOST, BUFFER_SIZE, RETRY_INTERVAL, get_peer_ports
from message_queue import MessageQueue

# ================================
# รับ BASE_PORT จาก argument
# ================================
if len(sys.argv) < 2:
    print("Usage: python node.py <BASE_PORT>")
    sys.exit(1)

BASE_PORT = int(sys.argv[1])
PEER_PORTS = get_peer_ports(BASE_PORT)

queue = MessageQueue()

print(f"[NODE {BASE_PORT}] Starting...")
print(f"[NODE {BASE_PORT}] Peers = {PEER_PORTS}")


# ================================
# SEND MESSAGE
# ================================
def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))
        s.sendall(message.encode())
        s.close()
        return True
    except Exception:
        return False


# ================================
# RETRY LOOP
# ================================
def retry_loop():
    while True:
        time.sleep(RETRY_INTERVAL)

        messages = queue.get_messages()
        if messages:
            print(f"[NODE {BASE_PORT}] Retry loop running... Queue size = {len(messages)}")

        for msg_entry in messages:
            peer = msg_entry["peer"]
            message = msg_entry["message"]
            attempts = msg_entry.get("attempts", 0) + 1

            print(f"[NODE {BASE_PORT}] Retrying to {peer}... (attempt {attempts})")

            if send_message(peer, message):
                print(f"[NODE {BASE_PORT}] Sent stored message to {peer}")
                queue.remove_message(msg_entry)
            else:
                print(f"[NODE {BASE_PORT}] Still cannot reach {peer}")
                queue.inc_attempts(msg_entry)


# ================================
# SERVER
# ================================
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening for messages...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        print(f"[NODE {BASE_PORT}] Received: '{data}' from {addr}")
        conn.close()


# ================================
# SEND INITIAL MESSAGES
# ================================
def send_initial_messages():
    for peer in PEER_PORTS:
        msg = f"hello from node {BASE_PORT}"
        if send_message(peer, msg):
            print(f"[NODE {BASE_PORT}] Sent to {peer}")
        else:
            print(f"[NODE {BASE_PORT}] Peer {peer} unavailable, storing message")
            queue.add_message(msg, peer)

    print(f"[NODE {BASE_PORT}] Queue size: {len(queue.get_messages())}")


# ================================
# MAIN
# ================================
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=retry_loop, daemon=True).start()

    # รอให้ server thread พร้อมก่อน
    time.sleep(2)

    send_initial_messages()

    # กันโปรแกรมปิด
    while True:
        cmd = input(f"[NODE {BASE_PORT}] Enter peer_port message (or 'exit'): ")

        if cmd.lower() == "exit":
            print(f"[NODE {BASE_PORT}] Exiting...")
            break

        try:
            peer_str, message = cmd.split(" ", 1)
            peer = int(peer_str)

            if send_message(peer, message):
                print(f"[NODE {BASE_PORT}] Sent manually to {peer}")
            else:
                print(f"[NODE {BASE_PORT}] Peer {peer} unavailable, storing message")
                queue.add_message(message, peer)

        except ValueError:
            print("Format: <peer_port> <message>")
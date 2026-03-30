# config.py

HOST = "127.0.0.1"
BUFFER_SIZE = 1024
RETRY_INTERVAL = 5

def get_peer_ports(port):
    if port == 8000:
        return [8001, 8002]
    elif port == 8001:
        return [8000, 8002]
    elif port == 8002:
        return [8000, 8001]
    else:
        return []

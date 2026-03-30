import socket
import struct
from config import MULTICAST_GROUP, PORT, BUFFER_SIZE
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(("", PORT))
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print(f"[RECEIVER] Joined {MULTICAST_GROUP}:{PORT} (Multiple instances ready)")
while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"[RECEIVER] {addr} -> {data.decode()}")
    except KeyboardInterrupt:
        print("\n[RECEIVER] Stopping...")
        break
sock.close()
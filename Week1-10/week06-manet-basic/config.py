# config.py
import sys

HOST = "127.0.0.1"
BUFFER_SIZE = 1024
FORWARD_PROBABILITY = 0.8  # ปรับให้สูงขึ้นหน่อยเพื่อให้เห็นการส่งต่อชัดเจน
TTL = 3

# ตรวจสอบว่ามีการใส่ Port มาทาง Command Line หรือไม่
if len(sys.argv) < 2:
    print("Usage: python node.py <PORT>")
    sys.exit(1)

BASE_PORT = int(sys.argv[1])

# กำหนด Topology แบบ Simple Line: 7000 <-> 7001 <-> 7002
if BASE_PORT == 7000:
    NEIGHBORS = [7001]
elif BASE_PORT == 7001:
    NEIGHBORS = [7000, 7002]
elif BASE_PORT == 7002:
    NEIGHBORS = [7001]
else:
    NEIGHBORS = []
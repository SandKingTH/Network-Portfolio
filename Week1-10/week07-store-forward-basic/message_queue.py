# message_queue.py

import time
import threading
from collections import deque

class MessageQueue:
    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def add_message(self, message, peer_port):
        with self.lock:
            self.queue.append({
                "message": message,
                "peer": peer_port,
                "timestamp": time.time(),
                "attempts": 0
            })

    def get_messages(self):
        with self.lock:
            return list(self.queue)

    def remove_message(self, msg):
        with self.lock:
            if msg in self.queue:
                self.queue.remove(msg)

    def inc_attempts(self, msg):
        with self.lock:
            for item in self.queue:
                if item is msg:
                    item["attempts"] += 1
                    break


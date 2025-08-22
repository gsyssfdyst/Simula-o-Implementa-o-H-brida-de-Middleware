# common/lamport_clock.py
import threading

class LogicalClock:
    """A simple thread-safe logical (Lamport) clock.

    Methods:
    - tick(): increment the local logical time and return it.
    - sync(received_time): merge with a received timestamp and advance.
    - get_current_time(): return the current logical time.
    """
    def __init__(self):
        self.time = 0
        self._lock = threading.Lock()

    def tick(self):
        """Increment the clock by one (local event)."""
        with self._lock:
            self.time += 1
            return self.time

    def sync(self, received_time):
        """Sync the clock with a received timestamp from another node."""
        with self._lock:
            self.time = max(self.time, received_time) + 1
            return self.time

    def get_current_time(self):
        """Return the current logical time without modifying it."""
        with self._lock:
            return self.time
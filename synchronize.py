import threading


class counter_share:
    '''
    multiple threads can share.
    '''

    def __init__(self, initial_key=0):
        self._key = initial_key
        self._key_lock = threading.Lock()

    def incr(self, delta=1):
        with self._key_lock:
            # Increasing the counter with lock
            self._key += delta

    def decr(self, delta=1):
        with self._key_lock:
            # Decreasing the counter with lock
            self._key -= delta

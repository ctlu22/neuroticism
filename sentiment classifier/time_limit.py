###### USAGE:
# try:
# 	with time_limit(5):
# 		long_function_call()
# except TimeoutException:
# 	print "Timed out"

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

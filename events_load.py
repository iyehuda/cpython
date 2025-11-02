from pathlib import Path
import pickle
import sys

from contextlib import contextmanager


atexit_pickle = Path("/tmp/atexit.pickle").read_bytes()
print_pickle = Path("/tmp/print.pickle").read_bytes()

events = []
active = False


def hook(event, args):
    if active:
        events.append((event, args))


sys.addaudithook(hook)


@contextmanager
def capture_events(name: str):
    print("-" * 50, f" {name} ", "-" * 50)
    global active
    events.clear()
    active = True
    try:
        yield
    except Exception as e:
        print(f"{name} failed: {e}")
    finally:
        active = False

        for event, args in events:
            print(f"{event:<24}: {args!r}")


with capture_events(" atexit "):
    pickle.loads(atexit_pickle)

with capture_events(" print "):
    pickle.loads(print_pickle)

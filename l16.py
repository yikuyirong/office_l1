
from contextlib import contextmanager

@contextmanager
def tag(value):
    print("Begin %s" % value)
    yield
    print("End %s" % value)

with tag("Tag"):
    print("Hello world")
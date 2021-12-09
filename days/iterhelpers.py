import itertools

def chunked(it, n):
    it = iter(it)
    return zip(*([it]*n))

def transpose(it):
    return zip(*it)

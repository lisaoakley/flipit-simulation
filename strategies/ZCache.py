from cachetools import cached, TTLCache, keys

__all__ = ('zkey')

def zkey(a, z, *args, **kwargs):
    return keys.hashkey(z[0], *args, **kwargs)
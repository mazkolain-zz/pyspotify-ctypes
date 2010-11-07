import ctypes

libspotify = ctypes.WinDLL("libspotify")

__all__ = ["album", "artist", "search", "session", "user"]

#structure definitions
class audioformat(ctypes.Structure):
    pass

#completion of types
audioformat._fields = [
    ("sample_type", ctypes.c_int),
    ("sample_rate", ctypes.c_int),
    ("channels", ctypes.c_int),
]
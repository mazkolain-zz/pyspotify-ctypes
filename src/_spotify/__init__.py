import os
import ctypes

if os.name == "nt":
    dllobj = ctypes.WinDLL
    dllfile = "win32/libspotify.dll"

if os.name == "posix":
    dllobj = ctypes.CDLL
    dllfile = "linux/x86/libspotify.so"

else:
    raise OSError("Cannot run in that environment: %s" % os.name)


libspotify = dllobj(os.path.join(os.path.dirname(__file__), "../../lib", dllfile))

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
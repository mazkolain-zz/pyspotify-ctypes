import os
import ctypes

#Module index
__all__ = ["album", "artist", "search", "session", "user"]


#Platform-specific initializations
if os.name == "nt":
    library = ctypes.WinDLL
    callback = ctypes.WINFUNCTYPE
    dllfile = "win32/libspotify.dll"

if os.name == "posix":
    library = ctypes.CDLL
    callback = ctypes.CFUNCTYPE
    dllfile = "linux/x86/libspotify.so"

else:
    raise OSError("Cannot run in that environment: %s" % os.name)


#Global libspotify instance
libspotify = library(
    os.path.join(os.path.dirname(__file__), "../../lib", dllfile)
)


#structure definitions
class audioformat(ctypes.Structure):
    pass


#completion of types
audioformat._fields = [
    ("sample_type", ctypes.c_int),
    ("sample_rate", ctypes.c_int),
    ("channels", ctypes.c_int),
]
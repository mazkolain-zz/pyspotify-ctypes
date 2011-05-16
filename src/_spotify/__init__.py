import os
import ctypes

#For arch calculations
import struct


#Module index
__all__ = [
    "album", "albumbrowse", "artist", "artistbrowse",
    "image", "inbox", "link", "localtrack",
    "playlist", "playlistcontainer", "radio", "search",
    "session", "toplistbrowse", "track", "user",
]


#Calculate void pointer size, 32 or 64
voidp_size = struct.calcsize("P") * 8


#Platform-specific initializations
if os.name == "nt" and voidp_size == 32:
    library = ctypes.WinDLL
    callback = ctypes.WINFUNCTYPE
    dllfile = "win32/libspotify.dll"

elif os.name == "posix" and voidp_size in [32,64]:
    library = ctypes.CDLL
    callback = ctypes.CFUNCTYPE
    
    if voidp_size == 32:
        dllfile = "linux/x86/libspotify.so"
    
    elif voidp_size == 64:
        dllfile = "linux/x86_64/libspotify.so"

else:
    raise OSError(
        "Cannot run in that environment (os: %s; arch: %d)" %
        (os.name, voidp_size)
    )


#Global libspotify instance
libspotify = library(
    os.path.join(os.path.dirname(__file__), "../../dlls", dllfile)
)


#structure definitions
class audioformat(ctypes.Structure):
    pass

class subscribers(ctypes.Structure):
    pass

class audio_buffer_stats(ctypes.Structure):
    pass


#completion of types
audioformat._fields_ = [
    ("sample_type", ctypes.c_int),
    ("sample_rate", ctypes.c_int),
    ("channels", ctypes.c_int),
]

subscribers._fields_ = [
    ("count", ctypes.c_uint),
    ("subscribers", ctypes.POINTER(ctypes.c_char_p))
]

audio_buffer_stats._fields_ = [
    ("samples", ctypes.c_int),
    ("stutter", ctypes.c_int),
]


#Function declarations
error_message = libspotify.sp_error_message
error_message.argtypes = [ctypes.c_int]
error_message.restype = ctypes.c_char_p

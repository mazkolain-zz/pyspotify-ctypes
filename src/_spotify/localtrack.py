import ctypes

#Import handy globals
from _spotify import libspotify


create = libspotify.sp_localtrack_create
create.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_int
]
create.restype = ctypes.c_void_p

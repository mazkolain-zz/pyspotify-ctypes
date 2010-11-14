import ctypes

#Import handy globals
from _spotify import libspotify


#Function prototypes
name = libspotify.sp_artist_name
name.argtypes = [ctypes.c_void_p]
name.restype = ctypes.c_char_p

is_loaded = libspotify.sp_artist_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

add_ref = libspotify.sp_artist_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_artist_release
release.argtypes = [ctypes.c_void_p]

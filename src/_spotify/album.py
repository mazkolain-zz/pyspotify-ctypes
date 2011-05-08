import ctypes

#Import handy globals
from _spotify import libspotify


#Function prototypes
is_loaded = libspotify.sp_album_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

is_available = libspotify.sp_album_is_available
is_available.argtypes = [ctypes.c_void_p]
is_available.restype = ctypes.c_bool

artist = libspotify.sp_album_artist
artist.argtypes = [ctypes.c_void_p]
artist.restype = ctypes.c_void_p

cover = libspotify.sp_album_cover
cover.argtypes = [ctypes.c_void_p]
cover.restype = ctypes.POINTER(ctypes.c_char * 20)

name = libspotify.sp_album_name
name.argtypes = [ctypes.c_void_p]
name.restype = ctypes.c_char_p

year = libspotify.sp_album_year
year.argtypes = [ctypes.c_void_p]
year.restype = ctypes.c_int

type = libspotify.sp_album_type
type.argtypes = [ctypes.c_void_p]
type.restype = ctypes.c_int

add_ref = libspotify.sp_album_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_album_release
release.argtypes = [ctypes.c_void_p]

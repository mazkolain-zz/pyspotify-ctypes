import ctypes

#Import handy globals
from _spotify import libspotify


is_loaded = libspotify.sp_track_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

error = libspotify.sp_track_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

is_available = libspotify.sp_track_is_available
is_available.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
is_available.restype = ctypes.c_bool

is_local = libspotify.sp_track_is_local
is_local.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
is_local.restype = ctypes.c_bool

is_autolinked = libspotify.sp_track_is_autolinked
is_autolinked.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
is_autolinked.restype = ctypes.c_bool

is_starred = libspotify.sp_track_is_starred
is_starred.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
is_starred.restype = ctypes.c_bool

set_starred = libspotify.sp_track_set_starred
set_starred.argtypes = [
    ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p),
    ctypes.c_int, ctypes.c_bool
]

num_artists = libspotify.sp_track_num_artists
num_artists.argtypes = [ctypes.c_void_p]
num_artists.restype = ctypes.c_int

artist = libspotify.sp_track_artist
artist.argtypes = [ctypes.c_void_p, ctypes.c_int]
artist.restype = ctypes.c_void_p

album = libspotify.sp_track_album
album.argtypes = [ctypes.c_void_p]
album.restype = ctypes.c_void_p

name = libspotify.sp_track_name
name.argtypes = [ctypes.c_void_p]
name.restype = ctypes.c_char_p

duration = libspotify.sp_track_duration
duration.argtypes = [ctypes.c_void_p]
duration.restype = ctypes.c_int

popularity = libspotify.sp_track_popularity
popularity.argtypes = [ctypes.c_void_p]
popularity.restype = ctypes.c_int

disc = libspotify.sp_track_disc
disc.argtypes = [ctypes.c_void_p]
disc.restype = ctypes.c_int

index = libspotify.sp_track_index
index.argtypes = [ctypes.c_void_p]
index.restype = ctypes.c_int

add_ref = libspotify.sp_track_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_track_release
release.argtypes = [ctypes.c_void_p]

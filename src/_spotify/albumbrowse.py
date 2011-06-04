import ctypes

#Import handy globals
from _spotify import libspotify, callback, bool_type


#Callbacks
albumbrowse_complete_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Function prototypes
create = libspotify.sp_albumbrowse_create

create = libspotify.sp_albumbrowse_create
create.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p,
    albumbrowse_complete_cb, ctypes.c_void_p
]
create.restype = ctypes.c_void_p

is_loaded = libspotify.sp_albumbrowse_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = bool_type

error = libspotify.sp_albumbrowse_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

album = libspotify.sp_albumbrowse_album
album.argtypes = [ctypes.c_void_p]
album.restype = ctypes.c_void_p

artist = libspotify.sp_albumbrowse_artist
artist.argtypes = [ctypes.c_void_p]
artist.restype = ctypes.c_void_p

num_copyrights = libspotify.sp_albumbrowse_num_copyrights
num_copyrights.argtypes = [ctypes.c_void_p]
num_copyrights.restype = ctypes.c_int

copyright = libspotify.sp_albumbrowse_copyright
copyright.argtypes = [ctypes.c_void_p, ctypes.c_int]
copyright.restype = ctypes.c_char_p

num_tracks = libspotify.sp_albumbrowse_num_tracks
num_tracks.argtypes = [ctypes.c_void_p]
num_tracks.restype = ctypes.c_int

track = libspotify.sp_albumbrowse_track
track.argtypes = [ctypes.c_void_p, ctypes.c_int]
track.restype = ctypes.c_void_p

review = libspotify.sp_albumbrowse_review
review.argtypes = [ctypes.c_void_p]
review.restype = ctypes.c_char_p

add_ref = libspotify.sp_albumbrowse_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_albumbrowse_release
release.argtypes = [ctypes.c_void_p]

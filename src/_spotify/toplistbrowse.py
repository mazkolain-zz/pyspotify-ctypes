import ctypes

#Import handy globals
from _spotify import libspotify, callback


#Callbacks
toplistbrowse_complete_cb = callback(ctypes.c_void_p, ctypes.c_void_p)


#Function prototypes
create = libspotify.sp_toplistbrowse_create
create.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
    ctypes.c_char_p, toplistbrowse_complete_cb, ctypes.c_void_p
]
create.restype = ctypes.c_void_p

is_loaded = libspotify.sp_toplistbrowse_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

error = libspotify.sp_toplistbrowse_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

add_ref = libspotify.sp_toplistbrowse_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_toplistbrowse_release
release.argtypes = [ctypes.c_void_p]

num_artists = libspotify.sp_toplistbrowse_num_artists
num_artists.argtypes = [ctypes.c_void_p]
num_artists.restype = ctypes.c_int

artist = libspotify.sp_toplistbrowse_artist
artist.argtypes = [ctypes.c_void_p, ctypes.c_int]
artist.restype = ctypes.c_void_p

num_albums = libspotify.sp_toplistbrowse_num_albums
num_albums.argtypes = [ctypes.c_void_p]
num_albums.restype = ctypes.c_int

album = libspotify.sp_toplistbrowse_album
album.argtypes = [ctypes.c_void_p, ctypes.c_int]
album.restype = ctypes.c_void_p

num_tracks = libspotify.sp_toplistbrowse_num_tracks
num_tracks.argtypes = [ctypes.c_void_p]
num_tracks.restype = ctypes.c_int

track = libspotify.sp_toplistbrowse_track
track.argtypes = [ctypes.c_void_p, ctypes.c_int]
track.restype = ctypes.c_void_p

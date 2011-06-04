import ctypes

#Import handy globals
from _spotify import libspotify, callback, bool_type


#Callbacks
search_complete_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Function prototypes
create = libspotify.sp_search_create
create.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p,
    ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, ctypes.c_int,
    search_complete_cb, ctypes.c_void_p
]
create.restype = ctypes.c_void_p

is_loaded = libspotify.sp_search_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = bool_type

error = libspotify.sp_search_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

num_tracks = libspotify.sp_search_num_tracks
num_tracks.argtypes = [ctypes.c_void_p]
num_tracks.restype = ctypes.c_int

track = libspotify.sp_search_track
track.argtypes = [ctypes.c_void_p, ctypes.c_int]
track.restype = ctypes.c_void_p

num_albums = libspotify.sp_search_num_albums
num_albums.argtypes = [ctypes.c_void_p]
num_albums.restype = ctypes.c_int

album = libspotify.sp_search_album
album.argtypes = [ctypes.c_void_p, ctypes.c_int]
album.restype = ctypes.c_void_p

num_artists = libspotify.sp_search_num_artists
num_artists.argtypes = [ctypes.c_void_p]
num_artists.restype = ctypes.c_int

artist = libspotify.sp_search_artist
artist.argtypes = [ctypes.c_void_p, ctypes.c_int]
artist.restype = ctypes.c_void_p

query = libspotify.sp_search_query
query.argtypes = [ctypes.c_void_p]
query.restype = ctypes.c_char_p

did_you_mean = libspotify.sp_search_did_you_mean
did_you_mean.argtypes = [ctypes.c_void_p]
did_you_mean.restype = ctypes.c_char_p

total_tracks = libspotify.sp_search_total_tracks
total_tracks.argtypes = [ctypes.c_void_p]
total_tracks.restype = ctypes.c_int

total_albums = libspotify.sp_search_total_albums
total_albums.argtypes = [ctypes.c_void_p]
total_albums.restype = ctypes.c_int

total_artists = libspotify.sp_search_total_artists
total_artists.argtypes = [ctypes.c_void_p]
total_artists.restype = ctypes.c_int

add_ref = libspotify.sp_search_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_search_release
release.argtypes = [ctypes.c_void_p]

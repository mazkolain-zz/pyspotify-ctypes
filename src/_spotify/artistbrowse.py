import ctypes

#Import handy globals
from _spotify import libspotify, callback


#Callbacks
artistbrowse_complete_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Function prototypes
create = libspotify.sp_artistbrowse_create
create.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p,
    artistbrowse_complete_cb, ctypes.c_void_p
]
create.restype = ctypes.c_void_p

is_loaded = libspotify.sp_artistbrowse_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

error = libspotify.sp_artistbrowse_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

artist = libspotify.sp_artistbrowse_artist
artist.argtypes = [ctypes.c_void_p]
artist.restype = ctypes.c_void_p

num_portraits = libspotify.sp_artistbrowse_num_portraits
num_portraits.argtypes = [ctypes.c_void_p]
num_portraits.restype = ctypes.c_int

portrait = libspotify.sp_artistbrowse_portrait
portrait.argtypes = [ctypes.c_void_p, ctypes.c_int]
portrait.restype = ctypes.POINTER(ctypes.c_byte)

num_tracks = libspotify.sp_artistbrowse_num_tracks
num_tracks.argtypes = [ctypes.c_void_p]
num_tracks.restype = ctypes.c_int

track = libspotify.sp_artistbrowse_track
track.argtypes = [ctypes.c_void_p, ctypes.c_int]
track.restype = ctypes.c_void_p

num_albums = libspotify.sp_artistbrowse_num_albums
num_albums.argtypes = [ctypes.c_void_p]
num_albums.restype = ctypes.c_int

album = libspotify.sp_artistbrowse_album
album.argtypes = [ctypes.c_void_p, ctypes.c_int]
album.restype = ctypes.c_void_p

num_similar_artists = libspotify.sp_artistbrowse_num_similar_artists
num_similar_artists.argtypes = [ctypes.c_void_p]
num_similar_artists.restype = ctypes.c_int

similar_artist = libspotify.sp_artistbrowse_similar_artist
similar_artist.argtypes = [ctypes.c_void_p, ctypes.c_int]
similar_artist.restype = ctypes.c_void_p

biography = libspotify.sp_artistbrowse_biography
biography.argtypes = [ctypes.c_void_p]
biography.restype = ctypes.c_char_p

add_ref = libspotify.sp_artistbrowse_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_artistbrowse_release
release.argtypes = [ctypes.c_void_p]

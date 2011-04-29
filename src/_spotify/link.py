import ctypes

#Import handy globals
from _spotify import libspotify


#Function protoypes
create_from_string = libspotify.sp_link_create_from_string
create_from_string.argtypes = [ctypes.c_char_p]
create_from_string.restype = ctypes.c_void_p

create_from_track = libspotify.sp_link_create_from_track
create_from_track.argtypes = [ctypes.c_void_p, ctypes.c_int]
create_from_track.restype = ctypes.c_void_p

create_from_album = libspotify.sp_link_create_from_album
create_from_album.argtypes = [ctypes.c_void_p]
create_from_album.restype = ctypes.c_void_p

create_from_artist = libspotify.sp_link_create_from_artist
create_from_artist.argtypes = [ctypes.c_void_p]
create_from_artist.restype = ctypes.c_void_p

create_from_search = libspotify.sp_link_create_from_search
create_from_search.argtypes = [ctypes.c_void_p]
create_from_search.restype = ctypes.c_void_p

create_from_playlist = libspotify.sp_link_create_from_playlist
create_from_playlist.argtypes = [ctypes.c_void_p]
create_from_playlist.restype = ctypes.c_void_p

create_from_user = libspotify.sp_link_create_from_user
create_from_user.argtypes = [ctypes.c_void_p]
create_from_user.restype = ctypes.c_void_p

as_string = libspotify.sp_link_as_string
as_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
as_string.restype = ctypes.c_int

type = libspotify.sp_link_type
type.argtypes = [ctypes.c_void_p]
type.restype = ctypes.c_int

as_track = libspotify.sp_link_as_track
as_track.argtypes = [ctypes.c_void_p]
as_track.restype = ctypes.c_void_p

as_track_and_offset = libspotify.sp_link_as_track_and_offset
as_track_and_offset.argtypes = [ctypes.c_void_p, ctypes.c_int]
as_track_and_offset.restype = ctypes.c_void_p

as_album = libspotify.sp_link_as_album
as_album.argtypes = [ctypes.c_void_p]
as_album.restype = ctypes.c_void_p

as_artist = libspotify.sp_link_as_artist
as_artist.argtypes = [ctypes.c_void_p]
as_artist.restype = ctypes.c_void_p

as_user = libspotify.sp_link_as_user
as_user.argtypes = [ctypes.c_void_p]
as_user.restype = ctypes.c_void_p

add_ref = libspotify.sp_link_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_link_release
release.argtypes = [ctypes.c_void_p]

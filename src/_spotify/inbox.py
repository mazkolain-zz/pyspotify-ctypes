import ctypes

#Import handy globals
from _spotify import libspotify, callback


#Callbacks
inboxpost_complete_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Function prototypes
post_tracks = libspotify.sp_inbox_post_tracks
post_tracks.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_char_p,
    inboxpost_complete_cb, ctypes.c_void_p
]
post_tracks.restype = ctypes.c_void_p

error = libspotify.sp_inbox_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

add_ref = libspotify.sp_inbox_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_inbox_release
release.argtypes = [ctypes.c_void_p]

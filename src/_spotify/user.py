import ctypes

#Import handy globals
from _spotify import libspotify


#Function prototypes
canonical_name = libspotify.sp_user_canonical_name
canonical_name.argtypes = [ctypes.c_void_p]
canonical_name.restype = [ctypes.c_char_p]

display_name = libspotify.sp_user_display_name
display_name.argtypes = [ctypes.c_void_p]
display_name.restype = ctypes.c_char_p

is_loaded = libspotify.sp_user_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

full_name = libspotify.sp_user_full_name
full_name.argtypes = [ctypes.c_void_p]
full_name.restype = ctypes.c_char_p

picture = libspotify.sp_user_picture
picture.argtypes = [ctypes.c_void_p]
picture.restype = ctypes.c_char_p

relation_type = libspotify.sp_user_relation_type
relation_type.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
relation_type.restype = ctypes.c_int

add_ref = libspotify.sp_user_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_user_release
release.argtypes = [ctypes.c_void_p]

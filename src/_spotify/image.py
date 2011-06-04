import ctypes

#Import handy globals
from _spotify import libspotify, callback, bool_type


#Callbacks
image_loaded_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Function prototypes
create = libspotify.sp_image_create
create.argtypes = [ctypes.c_void_p, ctypes.c_char * 20]
create

add_load_callback = libspotify.sp_image_add_load_callback
add_load_callback.argtypes = [
    ctypes.c_void_p, image_loaded_cb, ctypes.c_void_p
]

remove_load_callback = libspotify.sp_image_remove_load_callback
remove_load_callback.argtypes = [
    ctypes.c_void_p, image_loaded_cb, ctypes.c_void_p
]

is_loaded = libspotify.sp_image_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = bool_type

error = libspotify.sp_image_error
error.argtypes = [ctypes.c_void_p]
error.restype = ctypes.c_int

format = libspotify.sp_image_format
format.argtypes = [ctypes.c_void_p]
format.restype = ctypes.c_int

data = libspotify.sp_image_data
data.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]
data.restype = ctypes.c_void_p

image_id = libspotify.sp_image_image_id
image_id.argtypes = [ctypes.c_void_p]
image_id.restype = ctypes.POINTER(ctypes.c_byte)

add_ref = libspotify.sp_image_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_image_release
release.argtypes = [ctypes.c_void_p]

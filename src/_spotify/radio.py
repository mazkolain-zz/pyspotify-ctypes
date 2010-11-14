import ctypes

#Import handy globals
from _spotify import libspotify

#Import low level search api
import search as _search


radio_create = libspotify.sp_radio_search_create
radio_create.argtypes = [
    ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint,
    ctypes.c_int, _search.search_complete_cb, ctypes.c_void_p
]
radio_create.restype = ctypes.c_void_p

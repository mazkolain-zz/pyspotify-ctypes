import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface

#Import low level search api
import search as _search



class RadioInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)


    def search_create(self, *args):
        return self._get_func(
            'sp_radio_search_create',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint,
            ctypes.c_int, _search.search_complete_cb, ctypes.c_void_p
        )(*args)

import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, callback, bool_type


#Callbacks
search_complete_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)



class SearchInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'create',
            'sp_search_create',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_char_p,
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            search_complete_cb, ctypes.c_void_p
        )
        
        self._register_func(
            'is_loaded',
            'sp_search_is_loaded',
            bool_type,
            ctypes.c_void_p
        )
        
        self._register_func(
            'error',
            'sp_search_error',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'num_tracks',
            'sp_search_num_tracks',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'track',
            'sp_search_track',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'num_albums',
            'sp_search_num_albums',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'album',
            'sp_search_album',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'num_artists',
            'sp_search_num_artists',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'artist',
            'sp_search_artist',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'query',
            'sp_search_query',
            ctypes.c_char_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'did_you_mean',
            'sp_search_did_you_mean',
            ctypes.c_char_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'total_tracks',
            'sp_search_total_tracks',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'total_albums',
            'sp_search_total_albums',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'total_artists',
            'sp_search_total_artists',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'add_ref',
            'sp_search_add_ref',
            None,
            ctypes.c_void_p
        )
        
        self._register_func(
            'release',
            'sp_search_release',
            None,
            ctypes.c_void_p
        )

import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, callback, bool_type


#Callbacks
albumbrowse_complete_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)



class AlbumBrowseInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'create',
            'sp_albumbrowse_create',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_void_p, albumbrowse_complete_cb, ctypes.c_void_p
        )
        
        self._register_func(
            'is_loaded',
            'sp_albumbrowse_is_loaded',
            bool_type,
            ctypes.c_void_p
        )
        
        self._register_func(
            'error',
            'sp_albumbrowse_error',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'album',
            'sp_albumbrowse_album',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'artist',
            'sp_albumbrowse_artist',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'num_copyrights',
            'sp_albumbrowse_num_copyrights',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'copyright',
            'sp_albumbrowse_copyright',
            ctypes.c_char_p,
            ctypes.c_void_p, ctypes.c_int
        )
            
        self._register_func(
            'num_tracks',
            'sp_albumbrowse_num_tracks',
            ctypes.c_int,
            ctypes.c_void_p
        )
            
        self._register_func(
            'track',
            'sp_albumbrowse_track',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )
            
        self._register_func(
            'review',
            'sp_albumbrowse_review',
            ctypes.c_char_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'add_ref',
            'sp_albumbrowse_add_ref',
            None,
            ctypes.c_void_p
        )
        
        self._register_func(
            'release',
            'sp_albumbrowse_release',
            None,
            ctypes.c_void_p
        )

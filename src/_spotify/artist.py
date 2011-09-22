import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, bool_type



class ArtistInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'name',
            'sp_artist_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'is_loaded',
            'sp_artist_is_loaded',
            bool_type,
            ctypes.c_void_p
        )

        self._register_func(
            'add_ref',
            'sp_artist_add_ref',
            None,
            ctypes.c_void_p
        )

        self._register_func(
            'release',
            'sp_artist_release',
            None,
            ctypes.c_void_p
        )

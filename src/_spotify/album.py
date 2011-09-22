import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, bool_type



class AlbumInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'is_loaded',
            'sp_album_is_loaded',
            bool_type,
            ctypes.c_void_p
        )

        self._register_func(
            'is_available',
            'sp_album_is_available',
            bool_type,
            ctypes.c_void_p
        )

        self._register_func(
            'artist',
            'sp_album_artist',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'cover',
            'sp_album_cover',
            ctypes.POINTER(ctypes.c_byte * 20),
            ctypes.c_void_p
        )

        self._register_func(
            'name',
            'sp_album_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'year',
            'sp_album_year',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'type',
            'sp_album_type',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'add_ref',
            'sp_album_add_ref',
            None,
            ctypes.c_void_p,
        )

        self._register_func(
            'release',
            'sp_album_release',
            None,
            ctypes.c_void_p
        )

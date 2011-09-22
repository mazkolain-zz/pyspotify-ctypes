import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface



class LinkInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'create_from_string',
            'sp_link_create_from_string',
            ctypes.c_void_p,
            ctypes.c_char_p
        )

        self._register_func(
            'create_from_track',
            'sp_link_create_from_track',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )

        self._register_func(
            'create_from_album',
            'sp_link_create_from_album',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_album_cover',
            'sp_link_create_from_album_cover',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_artist',
            'sp_link_create_from_artist',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_artist_portrait',
            'sp_link_create_from_artist_portrait',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_artistbrowse_portrait',
            'sp_link_create_from_artistbrowse_portrait',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_search',
            'sp_link_create_from_search',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_playlist',
            'sp_link_create_from_playlist',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_user',
            'sp_link_create_from_user',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'create_from_image',
            'sp_link_create_from_image',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'as_string',
            'sp_link_as_string',
            ctypes.c_int,
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
        )

        self._register_func(
            'type',
            'sp_link_type',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'as_track',
            'sp_link_as_track',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'as_track_and_offset',
            'sp_link_as_track_and_offset',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )

        self._register_func(
            'as_album',
            'sp_link_as_album',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'as_artist',
            'sp_link_as_artist',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'as_user',
            'sp_link_as_user',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'add_ref',
            'sp_link_add_ref',
            None,
            ctypes.c_void_p
        )

        self._register_func(
            'release',
            'sp_link_release',
            None,
            ctypes.c_void_p
        )

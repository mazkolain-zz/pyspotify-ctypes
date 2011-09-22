import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, bool_type



class UserInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'canonical_name',
            'sp_user_canonical_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'display_name',
            'sp_user_display_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'is_loaded',
            'sp_user_is_loaded',
            bool_type,
            ctypes.c_void_p
        )

        self._register_func(
            'full_name',
            'sp_user_full_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'picture',
            'sp_user_picture',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'relation_type',
            'sp_user_relation_type',
            ctypes.c_int,
            ctypes.c_void_p, ctypes.c_void_p
        )

        self._register_func(
            'add_ref',
            'sp_user_add_ref',
            None,
            ctypes.c_void_p
        )

        self._register_func(
            'release',
            'sp_user_release',
            None,
            ctypes.c_void_p
        )

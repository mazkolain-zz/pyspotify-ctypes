import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, bool_type



class TrackInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'is_loaded',
            'sp_track_is_loaded',
            bool_type,
            ctypes.c_void_p
        )

        self._register_func(
            'error',
            'sp_track_error',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'is_available',
            'sp_track_is_available',
            bool_type,
            ctypes.c_void_p, ctypes.c_void_p
        )

        self._register_func(
            'is_local',
            'sp_track_is_local',
            bool_type,
            ctypes.c_void_p, ctypes.c_void_p
        )

        self._register_func(
            'is_autolinked',
            'sp_track_is_autolinked',
            bool_type,
            ctypes.c_void_p, ctypes.c_void_p
        )

        self._register_func(
            'is_starred',
            'sp_track_is_starred',
            bool_type,
            ctypes.c_void_p, ctypes.c_void_p
        )

        self._register_func(
            'set_starred',
            'sp_track_set_starred',
            None,
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_int, bool_type
        )

        self._register_func(
            'num_artists',
            'sp_track_num_artists',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'artist',
            'sp_track_artist',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )

        self._register_func(
            'album',
            'sp_track_album',
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        self._register_func(
            'name',
            'sp_track_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )

        self._register_func(
            'duration',
            'sp_track_duration',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'popularity',
            'sp_track_popularity',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'disc',
            'sp_track_disc',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'index',
            'sp_track_index',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'add_ref',
            'sp_track_add_ref',
            None,
            ctypes.c_void_p
        )

        self._register_func(
            'release',
            'sp_track_release',
            None,
            ctypes.c_void_p
        )

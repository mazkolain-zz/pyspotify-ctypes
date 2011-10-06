import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, bool_type



class UserInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)


    def canonical_name(self, *args):
        return self._get_func(
            'sp_user_canonical_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )(*args)


    def display_name(self, *args):
        return self._get_func(
            'sp_user_display_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )(*args)


    def is_loaded(self, *args):
        return self._get_func(
            'sp_user_is_loaded',
            bool_type,
            ctypes.c_void_p
        )(*args)


    def full_name(self, *args):
        return self._get_func(
            'sp_user_full_name',
            ctypes.c_char_p,
            ctypes.c_void_p
        )(*args)


    def picture(self, *args):
        return self._get_func(
            'sp_user_picture',
            ctypes.c_char_p,
            ctypes.c_void_p
        )(*args)


    def relation_type(self, *args):
        return self._get_func(
            'sp_user_relation_type',
            ctypes.c_int,
            ctypes.c_void_p, ctypes.c_void_p
        )(*args)


    def add_ref(self, *args):
        return self._get_func(
            'sp_user_add_ref',
            None,
            ctypes.c_void_p
        )(*args)


    def release(self, *args):
        return self._get_func(
            'sp_user_release',
            None,
            ctypes.c_void_p
        )(*args)

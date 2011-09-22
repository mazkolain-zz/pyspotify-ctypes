import ctypes

#Import handy globals
from _spotify import LibSpotifyInterface, callback, bool_type


#Callbacks
image_loaded_cb = callback(None, ctypes.c_void_p, ctypes.c_void_p)



class ImageInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'create',
            'sp_image_create',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_char * 20
        )

        self._register_func(
            'create_from_link',
            'sp_image_create_from_link',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_void_p
        )

        self._register_func(
            'add_load_callback',
            'sp_image_add_load_callback',
            None,
            ctypes.c_void_p, image_loaded_cb, ctypes.c_void_p
        )

        self._register_func(
            'remove_load_callback',
            'sp_image_remove_load_callback',
            None,
            ctypes.c_void_p, image_loaded_cb, ctypes.c_void_p
        )

        self._register_func(
            'is_loaded',
            'sp_image_is_loaded',
            bool_type,
            ctypes.c_void_p
        )

        self._register_func(
            'error',
            'sp_image_error',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'format',
            'sp_image_format',
            ctypes.c_int,
            ctypes.c_void_p
        )

        self._register_func(
            'data',
            'sp_image_data',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)
        )

        self._register_func(
            'image_id',
            'sp_image_image_id',
            ctypes.POINTER(ctypes.c_byte),
            ctypes.c_void_p
        )

        self._register_func(
            'add_ref',
            'sp_image_add_ref',
            None,
            ctypes.c_void_p
        )

        self._register_func(
            'release',
            'sp_image_release',
            None,
            ctypes.c_void_p
        )

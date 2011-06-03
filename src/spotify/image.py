'''
Created on 02/05/2011

@author: mazkolain
'''
import ctypes

from _spotify import image as _image

from spotify import DuplicateCallbackError, UnknownCallbackError, handle_sp_error

from spotify.utils.decorators import synchronized

import binascii



@synchronized
def create(session, image_id):
    buf = (ctypes.c_char * 20)()
    buf.value = binascii.a2b_hex(image_id)
    
    return Image(
        _image.create(session.get_struct(), buf)
    )



class ProxyImageCallbacks:
    __image = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, image, callbacks):
        self.__image = image
        self.__callbacks = callbacks
        self.__c_callback = _image.image_loaded_cb(self.image_loaded)
    
    def image_loaded(self, image_struct, userdata):
        self.__callbacks.image_loaded(self.__image)
    
    def get_c_callback(self):
        return self.__c_callback



class ImageCallbacks:
    def image_loaded(self, image):
        pass



class ImageFormat:
    Unknown = -1
    JPEG = 0



class Image:
    __image_struct = None
    __callbacks = None
    
    
    def __init__(self, image_struct):
        self.__image_struct = image_struct
        self.__callbacks = {}
    
    
    @synchronized
    def add_load_callback(self, callback):
        cb_id = id(callback)
        
        if cb_id in self.__callbacks:
            raise DuplicateCallbackError()
        
        else:
            proxy = ProxyImageCallbacks(
                self, callback
            )
            
            self.__callbacks[cb_id] = {
                "callback": callback,
                "proxy": proxy,
            }
            
            _image.add_load_callback(
                self.__image_struct, proxy.get_c_callback(), None
            )
    
    
    @synchronized
    def remove_load_callback(self, callback):
        cb_id = id(callback)
        
        if cb_id not in self.__callbacks:
            raise UnknownCallbackError()
        
        else:
            c_callback = self.__callbacks[cb_id]["proxy"].get_c_callback()
            _image.remove_load_callback(
                self.__image_struct, ctypes.byref(c_callback), None
            )
            del self.__callbacks[cb_id]
        
    
    @synchronized
    def remove_all_load_callbacks(self):
        for item in self.__callbacks:
            self.remove_load_callback(item["callback"])
    
    
    @synchronized
    def is_loaded(self):
        return _image.is_loaded(self.__image_struct)
    
    
    @synchronized
    def error(self):
        return _image.error(self.__image_struct)
    
    
    @synchronized
    def format(self):
        return _image.format(self.__image_struct)
    
    
    @synchronized
    def data(self):
        size = ctypes.c_size_t()
        raw = _image.data(self.__image_struct, ctypes.pointer(size))
        dest = ctypes.cast(raw, ctypes.POINTER(ctypes.c_char * size.value))
        return str(buffer(dest.contents))
    
    
    def get_struct(self):
        return self.__image_struct
    
    
    def __del__(self):
        self.remove_all_load_callbacks()

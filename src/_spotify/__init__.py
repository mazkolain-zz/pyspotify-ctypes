import struct, os, ctypes, sys
import weakref
from _spotify.utils import moduletracker


#Module index
__all__ = [
    "album", "albumbrowse", "artist", "artistbrowse",
    "image", "inbox", "link", "localtrack",
    "playlist", "playlistcontainer", "radio", "search",
    "session", "toplistbrowse", "track", "user", "utils",
]


#Some fallbacks for python 2.4
if hasattr(ctypes, "c_bool"):
    bool_type = ctypes.c_bool
else:
    bool_type = ctypes.c_ubyte


#Calculate void pointer size, 32 or 64
voidp_size = struct.calcsize("P") * 8

#Impor library loading routine
if os.name == "nt":
    from _ctypes import FreeLibrary as dlclose
else:
    from _ctypes import dlclose


#Platform-specific initializations
if os.name == "nt" and voidp_size == 32:
    callback = ctypes.WINFUNCTYPE

elif os.name == "posix" and voidp_size in [32,64]:
    callback = ctypes.CFUNCTYPE
    
else:
    raise OSError(
        "Cannot run in that environment (os: %s; arch: %d)" %
        (os.name, voidp_size)
    )



class ModuleInterface(object):
    __registered_funcs = None
    __library = None
    
    
    def __init__(self):
        self.__registered_funcs = {}
    
    
    def _load_library(self):
        pass
    
    
    def get_library(self):
        if self.__library is None:
            self.__library = self._load_library()
        
        return self.__library
    
    
    def __getattr__(self, name):
        if name not in self.__registered_funcs:
            raise AttributeError
        
        else:
            def func_caller(*args):
                func = self.__registered_funcs[name]
                return func(*args)
            
            return func_caller
    
    
    def _get_func2(self, name, orig_name, restype, *argtypes):
        if name not in self.__registered_funcs:
            lib = self.get_library()
            func = getattr(lib, orig_name)
            func.argtypes = argtypes
            func.restype = restype
            self.__registered_funcs[name] = func
        
        return self.__registered_funcs[name]
    
    
    def _get_func(self, name, restype, *argtypes):
        return self._get_func2(name, name, restype, *argtypes)
    
    
    def _register_func(self, name, orig_name, restype, *argtypes):
        return self._get_func2(name, orig_name, restype, *argtypes)



class LibSpotifyInterface(ModuleInterface):
    def __init__(self):
        ModuleInterface.__init__(self)
        moduletracker.track_module(self)
    
    
    def _load_library(self):
        ll = CachingLibraryLoader()
        return ll.load('libspotify')



_library_refs = {}



def unload_library():
    li = LibSpotifyInterface()
    _unload_library('libspotify', li.get_library()._handle)



def can_unload_library():
    return moduletracker.count_tracked_modules() == 0



def _unload_library(name, handle):
    #delete from the library refs dict
    if name in _library_refs:
        del _library_refs[name]
    
    #unload it
    dlclose(handle)
    print "dll unloaded"
    print handle



class CachingLibraryLoader:
    def _get_filename(self, name):
        if os.name == 'nt':
            return '%s.dll' % name
        
        elif os.name == 'posix':
            if sys.platform.startswith('linux'):
                return '%s.so' % name
            
            elif sys.platform == 'darwin':
                return name
    
    
    def _get_loader(self):
        if os.name == 'nt':
            return ctypes.windll
        
        elif os.name == 'posix':
            return ctypes.cdll
    
    
    def _load(self, name):
        loader = self._get_loader()
        
        #Let ctypes find it
        try:
            return getattr(loader, name)
    
        #Bad luck, let's do a quirk
        except OSError:
            filename = self._get_filename(name)
            for path in sys.path:
                full_path = os.path.join(path, filename)
                if os.path.isfile(full_path):
                    return loader.LoadLibrary(full_path)
        
            raise OSError("Unable to find '%s'" % name)
    
    
    def load(self, name):
        #Load if not found on the cache 
        if name not in _library_refs:
            library = self._load(name)
            _library_refs[name] = weakref.ref(library)
        
        else:
            ref = _library_refs[name]
            library = ref()
        
        return library



#structure definitions
class audioformat(ctypes.Structure):
    pass

class subscribers(ctypes.Structure):
    pass

class audio_buffer_stats(ctypes.Structure):
    pass



#completion of types
audioformat._fields_ = [
    ("sample_type", ctypes.c_int),
    ("sample_rate", ctypes.c_int),
    ("channels", ctypes.c_int),
]

subscribers._fields_ = [
    ("count", ctypes.c_uint),
    ("subscribers", ctypes.c_char_p * 1),
]

audio_buffer_stats._fields_ = [
    ("samples", ctypes.c_int),
    ("stutter", ctypes.c_int),
]



#Low level declaration interface
class SpotifyInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
    
    
    def error_message(self, *args):
        return self._get_func(
            'sp_error_message',
            ctypes.c_char_p,
            ctypes.c_int
        )(*args)
    
    
    def build_id(self, *args):
        return self._get_func(
            'build_id',
            'sp_build_id',
            ctypes.c_char_p
        )(*args)

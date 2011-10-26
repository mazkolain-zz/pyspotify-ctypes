__all__ = [
    "album", "albumbrowse", "artist", "artistbrowse",
    "image", "inbox", "link", "localtrack",
    "playlist", "playlistcontainer", "radio", "search",
    "session", "toplistbrowse", "track", "user",
]


import _spotify
import threading

from spotify.utils.decorators import synchronized



def handle_sp_error(errcode):
    if errcode != 0:
        iface = _spotify.SpotifyInterface()
        msg = iface.error_message(errcode)
        raise LibSpotifyError(msg)



class LibSpotifyError(Exception):
    pass



class DuplicateCallbackError(LibSpotifyError):
    pass



class UnknownCallbackError(LibSpotifyError):
    pass



class SampleType:
    Int16NativeEndian = 0



class ConnectionRules:
    Network = 0x1
    NetworkIfRoaming = 0x2
    AllowSyncOverMobile = 0x4
    AllowSyncOverWifi = 0x8



class ConnectionType:
    Unknown = 0
    Disconnected = 1
    Mobile = 2
    MobileRoaming = 3
    Wifi = 4
    Wired = 5



class MainLoop:
    _event = None
    _quit = None
    
    def __init__(self):
        self._event = threading.Event()
        self._quit = False
    
    def loop(self, session):
        timeout = None
        
        while not self._quit:
            self._event.wait(timeout)
            self._event.clear()
            timeout = session.process_events()
    
    def notify(self):
        self._event.set()
    
    def quit(self):
        self._quit = True
        self.notify()



class CallbackItem:
    def __init__(self, **args):
        self.__dict__.update(args)



class CallbackQueueManager:
    _callbacks = None
    
    def __init__(self):
        self._callbacks = []
        
    def add_callback(self, condition, callback, *args):
        self._callbacks.append(
            CallbackItem(
                condition = condition,
                callback = callback,
                args = args,
            )
        )
    
    def process_callbacks(self):
        for item in self._callbacks:
            if item.condition():
                self._callbacks.remove(item)
                item.callback(*item.args)



class BulkConditionChecker:
    _conditions = None
    _event = None
    
    def __init__(self):
        self._conditions = []
        self._event = threading.Event()
    
    
    @synchronized
    def add_condition(self, condition):
        self._conditions.append(condition)
    
    
    @synchronized
    def check_conditions(self):
        for item in self._conditions:
            if item():
                self._conditions.remove(item)
            
        #If list size reaches to zero all conditions have been met
        if len(self._conditions) == 0:
            self._complete()
            return True
        
        else:
            return False
    
    
    def _complete(self):
        self._event.set()
        self.complete()
    
    
    def complete(self):
        pass
    
    
    def complete_wait(self, timeout = None):
        #Clear the event first, so we make a "clean" check
        self._event.clear()
        
        #Check conditions if they have been already met, and wait
        self.check_conditions()
        self._event.wait(timeout)
        
        #Fail if we reached here due to a timeout
        if not self._event.isSet():
            raise RuntimeError('Timed out while waiting for an event.')
            



class CallbackManager:
    __callbacks = None
    
    
    def __init__(self):
        self.__callbacks = {}
    
    
    def _create_class(self, callback):
        return None
    
    
    def add_callbacks(self, callbacks):
        cb_id = id(callbacks)
        if cb_id in self.__callbacks:
            raise DuplicateCallbackError()
        else:
            self.__callbacks[cb_id] = CallbackItem(
                callbacks = callbacks,
                custom_class = self._create_class(callbacks)
            )
    
    
    def remove_callbacks(self, callbacks):
        cb_id = id(callbacks)
        if cb_id not in self.__callbacks:
            raise UnknownCallbackError()
        else:
            del self.__callbacks[cb_id]
    
    
    def remove_all_callbacks(self):
        for item in self.__callbacks.values():
            self.remove_callbacks(item.callbacks)
    
    
    def _call_funcs(self, name, *args, **kwargs):
        for item in self.__callbacks.values():
            f = getattr(item.callbacks, name)
            f(*args, **kwargs)
    
    
    def __getattr__(self, name):
        return lambda *args, **kwargs: self._call_funcs(name, *args, **kwargs)
        
    
    def __del__(self):
        self.remove_all_callbacks()

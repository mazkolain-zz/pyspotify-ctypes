'''
Created on 26/05/2011

@author: mikel
'''
import ctypes

from _spotify import inbox as _inbox

from spotify.utils.decorators import synchronized, extract_args

from utils.finalize import track_for_finalization
from utils.weakmethod import WeakMethod
import weakref



class ProxyInboxpostCallbacks:
    __inbox = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, inbox, callbacks):
        self.__inbox = weakref.proxy(inbox)
        self.__callbacks = callbacks
        self.__c_callback = _inbox.inboxpost_complete_cb(
            WeakMethod(self.inboxpost_complete)
        )
    
    
    def inboxpost_complete(self, inbox_struct, userdata):
        self.__callbacks.inboxpost_complete(self.__inbox)
    
    
    def get_c_callback(self):
        return self.__c_callback



class InboxpostCallbacks:
    def inboxpost_complete(self, inbox):
        pass



@extract_args
@synchronized
def _finalize_inbox(inbox_interface, inbox_struct):
    inbox_interface.release(inbox_struct)
    print "inbox __del__ called"



class Inbox:
    __inbox_struct = None
    __inbox_interface = None
    __proxy_callbacks = None
    
    
    def _build_track_array(self, track_list):
        track_arr = (ctypes.c_void_p * len(track_list))()
        for index, item in enumerate(track_list):
            track_arr[index] = item.get_struct()
        return track_arr
    
    
    @synchronized
    def __init__(self, session, user, track_list, message, callbacks):
        self.__proxy_callbacks = ProxyInboxpostCallbacks(self, callbacks)
        self.__inbox_interface = _inbox.InboxInterface()
        self.__inbox_struct = self.__inbox_interface.post_tracks(
            session.get_struct(), user,
            self._build_track_array(track_list), len(track_list),
            message, self.__proxy_callbacks.get_c_callback(), None
        )
        
        #register finalizers
        args = (self.__inbox_interface, self.__inbox_struct)
        track_for_finalization(self, args, _finalize_inbox)
    
    
    @synchronized
    def error(self):
        return self.__inbox_interface.error(self.__inbox_struct)

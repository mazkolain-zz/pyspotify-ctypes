'''
Created on 26/05/2011

@author: mikel
'''
from spotify import search

from _spotify import radio as _radio

from spotify.utils.decorators import synchronized, extract_args

from utils.finalize import track_for_finalization



class Genre:
    AltPopRock  = 0x1
    Blues       = 0x2
    Country     = 0x4
    Disco       = 0x8
    Funk        = 0x10
    HardRock    = 0x20
    HeavyMetal  = 0x40
    Rap         = 0x80
    House       = 0x100
    Jazz        = 0x200
    NewWave     = 0x400
    RnB         = 0x800
    Pop         = 0x1000
    Punk        = 0x2000
    Reggae      = 0x4000
    PopRock     = 0x8000
    Soul        = 0x10000
    Techno      = 0x20000



@extract_args
@synchronized
def _finalize_radio_search(search_interface, search_struct):
    search_interface.release(search_struct)
    print "radio __del__ called"



class RadioSearch(search.Search):
    __proxy_callbacks = None
    
    
    @synchronized
    def __init__(self, session, from_year, to_year, genres, callbacks=None):
        if callbacks is not None:
            self.__proxy_callbacks = search.ProxySearchCallbacks(
                self, callbacks
            )
            c_callback = self.__proxy_callbacks.get_c_callback()
        else:
            c_callback = None
        
        self.__search_interface = _radio.RadioInterface()
        self._search_struct = self.__radio_interface.search_create(
            session.get_struct(),
            from_year, to_year, genres,
            c_callback, None
        )
        
        #register finalizers
        args = (self.__search_interface, self._search_struct)
        track_for_finalization(self, args, _finalize_radio_search)

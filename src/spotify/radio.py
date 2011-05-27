'''
Created on 26/05/2011

@author: mikel
'''
from spotify import search

from _spotify import radio as _radio



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



class RadioSearch(search.Search):
    __proxy_callbacks = None
    
    
    def __init__(self, session, from_year, to_year, genres, callbacks=None):
        if callbacks is not None:
            self.__proxy_callbacks = search.ProxySearchCallbacks(
                self, callbacks
            )
            c_callback = self.__proxy_callbacks.get_c_callback()
        else:
            c_callback = None
        
        self._search_struct = _radio.search_create(
            session.get_struct(),
            from_year, to_year, genres,
            c_callback, None
        )

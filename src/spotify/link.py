'''
Created on 29/04/2011

@author: mikel
'''
import ctypes

from _spotify import link as _link

from spotify import track, user, artist, album

from spotify.utils.decorators import synchronized



@synchronized
def create_from_string(string):
    li = _link.LinkInterface()
    return Link(li.create_from_string(string))


@synchronized
def create_from_track(track, offset = 0):
    li = _link.LinkInterface()
    return Link(li.create_from_track(track.get_struct(), offset))


@synchronized
def create_from_artist(artist):
    li = _link.LinkInterface()
    return Link(li.create_from_artist(artist.get_struct()))


@synchronized
def create_from_album(album):
    li = _link.LinkInterface()
    return Link(li.create_from_album(album.get_struct()))


@synchronized
def create_from_search(search):
    li = _link.LinkInterface()
    return Link(li.create_from_search(search.get_struct()))


@synchronized
def create_from_playlist(playlist):
    li = _link.LinkInterface()
    return Link(li.create_from_playlist(playlist.get_struct()))


@synchronized
def create_from_user(user):
    li = _link.LinkInterface()
    return Link(li.create_from_user(user.get_struct()))



class LinkType:
    Invalid = 0
    Track = 1
    Album = 2
    Artist = 3
    Search = 4
    Playlist = 5
    Profile = 6
    Starred = 7
    Localtrack = 8
    Image = 9



class Link:
    __link_struct = None
    __link_interface = None
    
    
    def __init__(self, link_struct):
        self.__link_struct = link_struct
        self.__link_interface = _link.LinkInterface()
    
    
    @synchronized
    def as_string(self):
        buf = (ctypes.c_char * 255)()
        
        #Should check return value?
        self.__link_interface.as_string(self.__link_struct, buf, 255)
        
        return buf.value
    
    
    @synchronized
    def type(self):
        return self.__link_interface.type(self.__link_struct)
    
    
    @synchronized
    def as_track(self):
        return track.Track(self.__link_interface.as_track(self.__link_struct)) 
    
    
    @synchronized
    def as_track_and_offset(self):
        offset = ctypes.c_int
        track = track.Track(self.__link_interface.as_track_and_offset)
        return track, offset.value
    
    @synchronized
    def as_album(self):
        return album.Album(self.__link_interface.as_album(self.__link_struct))
    
    
    @synchronized
    def as_artist(self):
        return artist.Artist(self.__link_interface.as_artist(self.__link_struct))
    
    
    @synchronized
    def as_user(self):
        return user.User(self.__link_interface.as_user(self.__link_struct))
    
    
    @synchronized
    def add_ref(self):
        self.__link_interface.add_ref(self.__link_struct)
    
    
    def get_struct(self):
        return self.__link_struct
    
    
    def __str__(self):
        return self.as_string()
    
    
    @synchronized
    def __del__(self):
        self.__link_interface.release(self.__link_struct)

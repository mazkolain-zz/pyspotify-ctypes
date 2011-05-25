'''
Created on 07/11/2010

@author: mikel
'''
import sys

from appkey import appkey
from spotify import session, MainLoop, playlistcontainer, playlist, handle_sp_error

from spotify import BulkConditionChecker, link, artistbrowse, albumbrowse

import cmd
import threading

#Make cherrypy available on path
sys.path.append("../lib/CherryPy-3.2.0-py2.4.egg")


#Proxy http server for resources
from spotify.utils import httpproxy, audio



class JukeboxCallbacks(session.SessionCallbacks):
    _mainloop = None
    __buf = None
    
    def __init__(self, mainloop, buf):
        self._mainloop = mainloop
        self.__buf = buf
    
    def logged_in(self, session, error):
        handle_sp_error(error)
        print "login successful"  
    
    def logged_out(self, session):
        print "logout successful"
            
    
    def connection_error(self, session, error):
        print "conn error"
        
    def log_message(self, session, data):
        print "log: %s" % data
    
    def streaming_error(self, error):
        print "streaming error: %d" % error
    
    def end_of_track(self, session):
        self.__buf.set_track_ended()
        
    def notify_main_thread(self, session):
        self._mainloop.notify()
    
    def metadata_updated(self, session):
        #print "metadata_updated"
        pass
    
    def music_delivery(self, session, data, num_samples, sample_type, sample_rate, num_channels):
        return self.__buf.music_delivery(data, num_samples, sample_type, sample_rate, num_channels)
    
    def get_audio_buffer_stats(self, session):
        return self.__buf.get_stats()



def print_user(user):
    print "user loaded (cb): %d" % user.is_loaded()


def main():
    print "uses SPOTIFY(R) CORE"
    ml = MainLoop()
    buf = audio.MemoryBuffer()
    cb = JukeboxCallbacks(ml, buf)
    s = session.Session(
        cb,
        app_key=appkey,
        user_agent="python ctypes bindings",
        settings_location="C:\\sptest\\settings",
        cache_location="C:\\sptest\\cache",
    )
    
    pr = httpproxy.ProxyRunner(s, buf)
    c = JukeboxCmd(s, ml)
    c.start()
    pr.start()
    ml.loop(s)
    pr.stop()



class JukeboxPlaylistContainerCallbacks(playlistcontainer.PlaylistContainerCallbacks):
    _checker = None
    
    def __init__(self, checker):
        self._checker = checker
    
    def container_loaded(self, container):
        self._checker.check_conditions()
        
        

#Callback classes for artist loading
class ArtistLoadCallbacks(session.SessionCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def metadata_updated(self, session):
        self.__checker.check_conditions()



class ArtistbrowseLoadCallbacks(artistbrowse.ArtistbrowseCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def artistbrowse_complete(self, artistbrowse):
        self.__checker.check_conditions()



class AlbumLoadCallbacks(session.SessionCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def metadata_updated(self, session):
        self.__checker.check_conditions()



class AlbumbrowseLoadCallbacks(albumbrowse.AlbumbrowseCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def albumbrowse_complete(self, albumbrowse):
        self.__checker.check_conditions()



#The main jukebox command prompt
class JukeboxCmd(cmd.Cmd, threading.Thread):
    prompt = "jukebox>"
    
    _session = None
    _mainloop = None
    
    def __init__(self, session, mainloop):
        cmd.Cmd.__init__(self)
        threading.Thread.__init__(self)
        self._session = session
        self._mainloop = mainloop
    
    
    def run(self):
        self.cmdloop()
    
    
    def do_login(self, line):
        args = line.split(' ', 2)
        self._session.login(args[0], args[1])
    
    
    def do_logout(self, line):
        self._session.logout()
    
    
    def do_quit(self, line):
        self._mainloop.quit()
        return True
    
    
    def _load_artist(self, id):
        full_id = "spotify:artist:%s" % id
        checker = BulkConditionChecker()
        
        #Initialize all the artist loading stuff
        link_obj = link.create_from_string(full_id)
        artist_obj = link_obj.as_artist()
        checker.add_condition(artist_obj.is_loaded)
        callbacks = ArtistLoadCallbacks(checker)
        self._session.add_callbacks(callbacks)
        checker.complete_wait(10)
        self._session.remove_callbacks(callbacks)
        
        #Now initialize the artistbrowse load stuff
        callbacks = ArtistbrowseLoadCallbacks(checker)
        artistbrowse_obj = artistbrowse.Artistbrowse(
            self._session, artist_obj, callbacks
        )
        checker.add_condition(artistbrowse_obj.is_loaded)
        checker.complete_wait(10)
        
        return artist_obj, artistbrowse_obj
    
    
    def _load_album(self, id):
        import time
        full_id = "spotify:album:%s" % id
        checker = BulkConditionChecker()
        
        #All the album loading stuff
        link_obj = link.create_from_string(full_id)
        album_obj = link_obj.as_album()
        checker.add_condition(album_obj.is_loaded)
        callbacks = AlbumLoadCallbacks(checker)
        self._session.add_callbacks(callbacks)
        checker.complete_wait(10)
        self._session.remove_callbacks(callbacks)
        
        #Now the albumbrowse object
        callbacks = AlbumbrowseLoadCallbacks(checker)
        albumbrowse_obj = albumbrowse.Albumbrowse(
            self._session, album_obj, callbacks
        )
        checker.add_condition(albumbrowse_obj.is_loaded)
        checker.complete_wait(10)
        
        return album_obj, albumbrowse_obj
    
    
    def do_artist(self, line):
        args = line.split(' ', 2)
        if len(args) != 1:
            print "this command only takes one argument"
        
        else:
            artist_obj, artistbrowse_obj = self._load_artist(args[0])
            print "artist: %s" % artist_obj.name()
            print " - Albums: %d" % artistbrowse_obj.num_albums()
            print " - Tracks: %d" % artistbrowse_obj.num_tracks()
            print " - Portraits: %d" % artistbrowse_obj.num_portraits()
    
    
    def do_album(self, line):
        args = line.split(' ', 2)
        if len(args) != 1:
            print "this command takes one argument"
        
        else:
            album_obj, albumbrowse_obj = self._load_album(args[0])
            print "album: %s" % album_obj.name()
            print " - Tracks: %d" % albumbrowse_obj.num_tracks()
            print " - Copyrights: %d" % albumbrowse_obj.num_copyrights()
    
    
    def do_list(self, line):
        container = self._session.playlistcontainer()
        
        if not container.is_loaded():
            checker = BulkConditionChecker()
            #Wait until the container is loaded
            checker.add_condition(container.is_loaded)
            callbacks = JukeboxPlaylistContainerCallbacks(checker)
            container.add_callbacks(callbacks)
            checker.complete_wait()
            
            for item in container:
                item.set_in_ram(self._session, True)
        
        if not line:
            #Print all playlists
            print "%d playlists:" % container.num_playlists()
            
            for k, item in enumerate(container):
                if item.is_loaded():
                    print "playlist #%d: %s" % (k, item.name()) 
                else:
                    print "playlist #%d: loading..." % k
        else:
            pos = int(line)
            pl = container.playlist(pos)
            print "playlist #%d, %d tracks:" % (pos, pl.num_tracks())
            
            for index,item in enumerate(pl):
                if item.is_loaded():
                    print "track #%d: %s" % (index, item.name())
                    #print item.album().cover()
                else:
                    print "track #%d: loading..." % index
    
    
    do_EOF = do_quit


if __name__ == '__main__':
    main()

'''
Created on 07/11/2010

@author: mikel
'''
from appkey import appkey
from spotify import session, SessionCallbacks, MainLoop, playlistcontainer, playlist, handle_sp_error

from spotify import BulkConditionChecker

import cmd
import threading


class JukeboxPlaylistCallbacks(playlist.PlaylistCallbacks):
    _checker = None
    
    def __init__(self, checker):
        self._checker = checker
        
    def playlist_state_changed(self, playlist):
        self._checker.check_conditions()


class JukeboxPlaylistContainerCallbacks(playlistcontainer.PlaylistContainerCallbacks):
    _checker = None
    
    def __init__(self, checker):
        self._checker = checker
    
    def container_loaded(self, container):
        self._checker.check_conditions()


class JukeboxCallbacks(SessionCallbacks):
    _mainloop = None
    
    def __init__(self, mainloop):
        self._mainloop = mainloop
    
    def logged_in(self, session, error):
        handle_sp_error(error)
        print "login successful"  
    
    def logged_out(self, session):
        print "logout successful"
            
    
    def connection_error(self, session, error):
        print "conn error"
        
    def log_message(self, session, data):
        #print "log: %s" % data
        pass
        
    def notify_main_thread(self, session):
        self._mainloop.notify()
    
    def metadata_updated(self, session):
        #print "metadata_updated"
        pass


def print_user(user):
    print "user loaded (cb): %d" % user.is_loaded()


def main():
    ml = MainLoop()
    cb = JukeboxCallbacks(ml)
    s = session.Session(
        cb,
        app_key=appkey,
        user_agent="python ctypes bindings",
        settings_location="C:\\sptest\\settings",
        cache_location="C:\\sptest\\cache",
    )
    
    c = JukeboxCmd(s, ml)
    c.start()
    ml.loop(s)
    

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
    
    
    def do_list(self, line):
        container = self._session.playlistcontainer()
    
        checker = BulkConditionChecker()
    
        if not container.is_loaded():
            #Wait until the container is loaded
            checker.add_condition(container.is_loaded)
            callbacks = JukeboxPlaylistContainerCallbacks(checker)
            container.add_callbacks(callbacks)
            checker.complete_wait()
        
            #Wait until the playlists are loaded
            for item in container:
                checker.add_condition(item.is_loaded)
                callbacks = JukeboxPlaylistCallbacks(checker)
                item.add_callbacks(callbacks)
                item.set_in_ram(True)
                checker.complete_wait()
        
        
        print "%d playlists total:" % len(container)
        
        for item in container:
            print "playlist: %s" % item.name() 
        
        #print "list should be complete here"
    
    
    do_EOF = do_quit


if __name__ == '__main__':
    main()

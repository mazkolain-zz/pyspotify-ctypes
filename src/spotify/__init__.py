__all__ = ["session", "user"]


import _spotify
import threading


def handle_sp_error(errcode):
    if errcode != 0:
        msg = _spotify.error_message(errcode)
        raise LibSpotifyError(msg)


class LibSpotifyError(Exception):
    pass


class DuplicateCallbackError(LibSpotifyError):
    pass


class UnknownCallbackError(LibSpotifyError):
    pass


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
            timeout = session.process_events()
            self._event.clear()
    
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


class SessionCallbacks:
    def logged_in(self, session, error):
        pass
    
    def logged_out(self, session):
        pass
    
    def metadata_updated(self, session):
        pass
    
    def connection_error(self, session, error):
        pass
    
    def message_to_user(self, session, message):
        pass
    
    def notify_main_thread(self, session):
        pass
    
    def music_delivery(self, format, frames, num_frames):
        pass
    
    def play_token_lost(self, session):
        pass
    
    def log_message(self, session, message):
        pass
    
    def end_of_track(self, session, error):
        pass
    
    def userinfo_updated(self, session):
        pass
    
    def start_playback(self, session):
        pass
    
    def stop_playback(self, session):
        pass
    
    def get_audio_buffer_stats(self, session, stats):
        pass

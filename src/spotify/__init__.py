__all__ = ["session", "user"]


import _spotify
import threading


def handle_sp_error(errcode):
    if errcode != 0:
        msg = _spotify.error_message(errcode)
        raise LibSpotifyError(msg)


class LibSpotifyError(Exception):
    pass


class MainLoop:
    _event = None
    
    def __init__(self):
        self._event = threading.Event()
    
    def loop(self, session):
        timeout = None
        
        while True:
            self._event.wait(timeout)
            timeout = session.process_events()
            self._event.clear()
    
    def notify(self):
        self._event.set()


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

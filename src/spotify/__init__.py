__all__ = ["session", "user"]

import session

class LibSpotifyError(Exception):
    def __init__(self, msg):
        self.msg = msg

class SpotifySessionManager:
    _session = None
    
    def __init__(self, **kwargs):
        _session = session.Session(self, kwargs)
    
    def logged_in(self):
        pass
    
    def logged_out(self):
        pass
    
    def metadata_updated(self):
        pass
    
    def connection_error(self):
        pass
    
    def message_to_user(self):
        pass
    
    def notify_main_thread(self):
        pass
    
    def search(self, query):
        pass
    
    def music_delivery(self, format, frames, num_frames):
        pass
    
    def play_token_lost(self):
        pass
    
    def log_message(self, message):
        pass
    
    def end_of_track(self):
        pass

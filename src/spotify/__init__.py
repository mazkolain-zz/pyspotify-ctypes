__all__ = ["session", "user"]

import session

class LibSpotifyError(Exception):
    def __init__(self, msg):
        self.msg = msg

class SpotifySessionManager:
    _session = None
    
    def __init__(self, username="", password="", **kwargs):
        _session = session.Session(self, **kwargs)
        _session.login(username, password)
    
    def search(self, query):
        pass
    
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

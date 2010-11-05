from ctypes import WinDLL

libspotify = WinDLL("libspotify")

__all__ = ["album", "artist", "search", "session", "user"]
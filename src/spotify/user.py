from _spotify import user as _user

from spotify.utils.decorators import synchronized


class User:
    _session = None
    _user = None
    
    
    @synchronized
    def __init__(self, session, user):
        self._session = session
        self._user = user
        
        #Ref counting
        _user.add_ref(self._user)
    
    @synchronized
    def canonical_name(self):
        return _user.canonical_name(self._user)
    
    @synchronized
    def display_name(self):
        return _user.display_name(self._user)
    
    @synchronized
    def full_name(self):
        return _user.full_name(self._user)
    
    @synchronized
    def is_loaded(self):
        return _user.is_loaded(self._user)
    
    @synchronized
    def picture(self):
        return _user.picture(self._user)
    
    @synchronized
    def relation_type(self):
        return _user.relation_type(self._session, self._user)
    
    @synchronized
    def __del__(self):
        _user.release(self._user)
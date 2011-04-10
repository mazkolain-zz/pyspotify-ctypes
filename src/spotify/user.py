from _spotify import user as _user

class User:
    _session = None
    _user = None
    
    def __init__(self, session, user):
        self._session = session
        self._user = user
        
        #Ref counting
        _user.add_ref(self._user)
    
    def canonical_name(self):
        return _user.canonical_name(self._user)
    
    def display_name(self):
        return _user.display_name(self._user)
    
    def full_name(self):
        return _user.full_name(self._user)
    
    def is_loaded(self):
        return _user.is_loaded(self._user)
    
    def picture(self):
        return _user.picture(self._user)
    
    def relation_type(self):
        return _user.relation_type(self._session, self._user)
    
    def __del__(self):
        _user.release(self._user)
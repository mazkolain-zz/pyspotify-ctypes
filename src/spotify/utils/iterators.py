'''
Created on 01/06/2011

@author: mazkolain
'''
class CallbackIterator:
    __count_method = None
    __item_method = None
    __pos = None
    
    
    def __init__(self, count_method, item_method):
        self.__count_method = count_method
        self.__item_method = item_method
        self.__pos = 0
    
    
    def __len__(self):
        return self.__count_method()
    
    
    def __iter__(self):
        return self
    
    
    def next(self):
        if self.__pos < len(self):
            item = self.__item_method(self.__pos)
            self.__pos += 1
            return item
        else:
            raise StopIteration

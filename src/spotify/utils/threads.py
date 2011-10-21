'''
Created on 22/10/2011

@author: mikel
'''
import collections
import threading



class TaskItem:
    __target = None
    __args = None
    __kwargs = None
    
    __container_id = None
    __instance_id = None
    
    
    def _get_target_instance_id(self, target):
        if hasattr(target, 'im_self'):
            return id(target.im_self)
        else:
            return id(target)
    
    
    def _get_target_container_id(self, target):
        if hasattr(target, 'im_class'):
            path = [
                target.im_class.__module__,
                target.im_class.__name__,
                target.__name__
            ]
            
        else:
            path = [
                target.__module__,
                target.__name__
            ]
        
        return '.'.join(path)
    
    
    def __init__(self, target, *args, **kwargs):
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        self.__container_id = self._get_target_container_id(target)
        self.__instance_id = self._get_target_instance_id(target)
    
    
    def get_container_id(self):
        return self.__container_id
    
    
    def get_instance_id(self):
        return self.__instance_id
    
    
    def run(self):
        self.__target(*self.__args, **self.__kwargs)



class TaskQueueManager:
    __queues = None
    
    
    def __init__(self):
        self.__queues = {}
    
    
    def has_queue(self, container_id):
        return container_id in self.__queues
    
    
    def _check_queue(self, container_id):
        if not self.has_queue(container_id):
            raise KeyError('Unknown task container: %s' % container_id)
        
        return self.__queues[container_id]
    
    
    def get_tasks(self, container_id):
        self._check_queue(container_id)
        
        #Avoid returning the live queue
        return list(self.__queues[container_id])
    
    
    def _remove_from_queue(self, queue, task):
        #Queue has remove()!
        if hasattr(queue, 'remove'):
            queue.remove(task)
        
        #pre-2.5, no remove(), snif.
        else:
            for idx, item in enumerate(queue):
                if item == task:
                    del queue[idx]
                    return
    
    
    def add(self, task):
        container_id = task.get_container_id()
        
        #New container queue needed
        if not self.has_queue(container_id):
            self.__queues[container_id] = collections.deque([task])
        
        #Append task to existing queue normally
        else:
            self.__queues[container_id].append(task)
    
    
    def remove(self, task):
        container_id = task.get_container_id()
        self._check_queue(container_id)
        
        #Remove the task first
        self._remove_from_queue(self.__queues[container_id], task)
        
        #If queue queue reached to zero length, remove it
        if len(self.__queues[container_id]) == 0:
            del self.__queues[container_id]



class TaskCountManager:
    __containers = None
    __instances = None
    
    
    def __init__(self):
        self.__containers = {}
        self.__instances = {}
    
    
    def _check_container(self, container_id, max):
        if max == 0:
            return True
        
        elif container_id not in self.__containers:
            return True
        
        elif self.__containers[container_id] < max:
            return True
        
        else:
            return False
    
    
    def _check_single_instance(self, instance_id, single_instance):
        if single_instance == False:
            return True
        
        elif instance_id not in self.__instances:
            return True
        
        else:
            return False
    
    
    def can_run(self, task, threads_per_instance, single_instance):
        container_id = task.get_container_id()
        instance_id = task.get_instance_id()
        
        if not self._check_container(container_id, threads_per_instance):
            return False
        
        elif not self._check_single_instance(instance_id, single_instance):
            return False
        
        else:
            return True
    
    
    def _add_container(self, container_id):
        if container_id not in self.__containers:
            self.__containers[container_id] = 1
        
        else:
            self.__containers[container_id] += 1
    
    
    def _remove_container(self, container_id):
        if container_id not in self.__containers:
            raise KeyError("Unknown container id: %s" % container_id)
        
        elif self.__containers[container_id] == 1:
            del self.__containers[container_id]
        
        else:
            self.__containers[container_id] -= 1
    
    
    def _add_instance(self, instance_id):
        if instance_id not in self.__instances:
            self.__instances[instance_id] = 1
        
        else:
            self.__instances[instance_id] += 1
    
    
    def _remove_instance(self, instance_id):
        if instance_id not in self.__instances:
            raise KeyError("Unknown instance id: %s" % instance_id)
        
        elif self.__instances[instance_id] == 1:
            del self.__instances[instance_id]
        
        else:
            self.__instances[instance_id] -= 1
    
    
    def add_task(self, task):
        self._add_container(task.get_container_id())
        self._add_instance(task.get_instance_id())
    
    
    def remove_task(self, task):
        self._remove_container(task.get_container_id())
        self._remove_instance(task.get_instance_id())



class TaskManager:
    #Static class instances
    __queue_manager = TaskQueueManager()
    __count_manager = TaskCountManager()
    __lock = threading.RLock()
    
    #Options
    __threads_per_class = None
    __single_instance = None
    
    
    def __init__(self, threads_per_class=10, single_instance=False):
        self.__threads_per_class = threads_per_class
        self.__single_instance = single_instance
    
    
    def _task_can_run(self, task):
        return self.__count_manager.can_run(
            task, self.__threads_per_class, self.__single_instance
        )
    
    
    def _get_next_task(self, container_id):
        for item in self.__queue_manager.get_tasks(container_id):
            if self._task_can_run(item):
                return item
        
        return None
    
    
    def _task_post(self, task):
        self.__lock.acquire()
        
        try:
            #Decrement task count
            self.__count_manager.remove_task(task)
            
            #Handle enqueued tasks
            if self.__queue_manager.has_queue(task.get_container_id()):
                #Get the next runnable task on the container
                next_task = self._get_next_task(task.get_container_id())
                
                #If it got started remove it from the queue
                if next_task is not None and self._try_start(next_task):
                    self.__queue_manager.remove(next_task)
        
        finally:
            self.__lock.release()
    
    
    def _try_start(self, task):
        def runner():
            #Run the actual task
            task.run()
            
            #And execute post actions
            self._task_post(task)
        
        #If yes, run it
        if self._task_can_run(task):
            #Register that task
            self.__count_manager.add_task(task)
            
            #And start it in a thread
            thread = threading.Thread(target=runner)
            thread.start()
            
            return True
        
        else:
            return False
    
    
    def add(self, target, *args, **kwargs):
        task = TaskItem(target, *args, **kwargs)
        self.__lock.acquire()
        
        try:
            #Enqueue if we can't start it
            if not self._try_start(task):
                self.__queue_manager.add(task)
                return False
            
            else:
                return True
        
        finally:
            self.__lock.release()

from typing import Generator,Any
from typing import Self

class Returner:
    def __init__(self,return_val:Any,msg:str) -> None:
        self.return_val = return_val
        self.msg = msg

class CheckPointFunction:
    '''
    Making a function return by checkpoints

    
    Examples
    --------
    Assing val to 1, executes, send 10 when checkpoint 'first', and return when checkpoint 'second
    >>> @CheckPointFunctionDecoration
    >>> def itertest(val):
    >>>    val +=1
    >>>    received = yield val, 'first'
    >>>    if received is not None:
    >>>        val += received
    >>>    yield val, 'second'
    >>> itertest(1).second(first=10)
    12
    '''
    def __init__(self,func:Generator[tuple[Any,str],Any,Any]) -> None:
        self.func=func
        self.init_args=tuple()
        self.init_kwargs=dict()

    def _convert_to_returner(self,point:tuple[Any,str] | Returner) -> Returner:
        if type(point) == tuple:
            point = Returner(return_val=point[0],msg=point[1])
            print('Implicitly converted to Returner')
        elif type(point) == Returner:
            pass
        else:
            raise ValueError(f'Invalid type {type(point)}')
        return point
    
    def __getattr__(self,checkpoint:str):
        class CheckPointFunctionContexted(CheckPointFunction):
            '''
            Includes where to stop(called checkpoint)
            '''
            def __init__(self,func:Generator[tuple[Any,str],Any,Any],
                         init_args:tuple,init_kwargs:dict,checkpoint:str) -> None:
                self.func=func
                self.checkpoint = checkpoint
                self.init_args = init_args
                self.init_kwargs = init_kwargs.copy()

            def __call__(self, **kwds: Any) -> Any:
                '''
                Executes until checkpoint reaches.
                
                Parameters
                ----------
                **kwds : Any
                    keyword arguments including value for sender.
                    Value will be sended when this function reaches the keyword.
                
                Returns
                --------
                Any
                    Return value when reaches the end of checkpoint.
                '''

                gen = self.func(*self.init_args,**self.init_kwargs)

                sender_memory = None
                while point := gen.send(sender_memory):
                    point : tuple[Any,str] | Returner
                    point = self._convert_to_returner(point)
                    
                    sender_memory = None
                    if point.msg == self.checkpoint:
                        return point.return_val
                    elif point.msg in kwds:
                        sender_memory = kwds[point.msg]
            def __iter__(self):
                self._gen = self.func(*self.init_args,**self.init_kwargs)
                self._stop_iter = False
                return self
            def __next__(self):
                while point := next(self._gen):
                    point = self._convert_to_returner(point)

                    if self._stop_iter:
                        raise StopIteration
                    if point.msg == self.checkpoint:
                        self._stop_iter = True
                    return point.return_val
                    
        return CheckPointFunctionContexted(self.func,self.init_args,self.init_kwargs,checkpoint)
    def __call__(self, *args: Any, **kwds: Any) -> Self:
        '''
        Set arguments when initializing
        
        Parameters
        ----------
        *args : Any
            Positional arguments when initializing.
        *kwds : Any
            Keyword arguments when initializing.

        Returns
        --------
        Self
            Returns itself.
        
        Examples
        --------
        Initialize value val to 1.
        >>> @CheckPointFunctionDecoration
        >>> def itertest(val):
        >>>    val +=1
        >>>    received = yield val, 'first'
        >>>    if received is not None:
        >>>        val += received
        >>>    yield val, 'second'
        >>> itertest(1)
        '''
        self.init_args= args
        self.init_kwargs = kwds.copy()
        return self

    def __iter__(self):
        self._gen = self.func(*self.init_args,**self.init_kwargs)
        return self
    def __next__(self):
        while point := next(self._gen):
            point = self._convert_to_returner(point)

            return point.return_val

def CheckPointFunctionDecoration(func:Generator[tuple[Any,str],Any,Any]):
    return CheckPointFunction(func)
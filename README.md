# Example
```
import checkpoint.checkpoint_function as cp

@cp.CheckPointFunctionDecoration
def func(val:int):
    x = yield val,'checkpoint1'
    yield val+x,'checkpoint2'
func(3).checkpoint2(checkpoint1=2) #It should return as 5
```
```
import checkpoint.checkpoint_function as cp

@cp.CheckPointFunctionDecoration
def func2(val:int):
    yield val,'checkpoint1'
    yield val+1,'checkpoint2'
    yield val-10,'checkpoint3'

list(func2(3).checkpoint3) #It should return as [3,4,-7]
```
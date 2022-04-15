# Mortice
Mortice is a file locking utility that provides both a functional interface and a context manager for use in locking files.  

## Usage
1. To use the context management API you have a choice of either synchronous or asynchronous use.
* For asynchronous context management use as follows:  
```python
async with Mortice(
    file, 
    open_mode, 
    blocking_status, 
    wait_time_for_blocked_calls
) as f:
    f.read()
```
* For synchronous context management use as follows:  
```python
with Mortice(
    file, 
    open_mode, 
    blocking_status, 
    wait_time_for_blocked_calls
) as f:
    f.read()
```  

2. For usage of the functional API call as follows:  

* For locking operations call:
```python
Mortice.lock_file(
    open_file: io.TextIOWrapper,
    file_open_mode: str = 'r',
    blocking: bool = True
)
```  

* For unlocking operations call:
```python
Mortice.unlock_file(
    open_file: io.TextIOWrapper,
)
```
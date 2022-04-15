# Mortice
Mortice is a file locking utility that provides both a functional interface and a context manager for use in locking files.

## Usage
For asynchronous context management use as follows:
```python
async with Mortice(
    file, 
    open_mode, 
    blocking_status, 
    wait_time_for_blocked_calls
) as f:
    f.read()
```
For synchronous context management use as follows:
```python
with Mortice(
    file, 
    open_mode, 
    blocking_status, 
    wait_time_for_blocked_calls
) as f:
    f.read()
```
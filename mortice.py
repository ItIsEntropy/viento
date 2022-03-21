# Create a lock for POSIX or NT systems and present a platform agnostic API to users.

import os
import msvcrt
from pathlib import Path
from typing import NoReturn, Callable

def lock_file(func: Callable[..., Path]) -> Path :
    def wrapper():
        open_file = func(*args, **kwargs)
        if os.name == 'nt':
            lock_file = msvcrt.locking(open_file, msvcrt.LK_LOCK,0)
            pass
        elif os.name == 'posix':
            pass
        else:
            raise RuntimeError('Mortice currently only has support for NT and POSIX based platforms')
    return wrapper

def unlock_file(func) -> NoReturn :
    pass

class FileLockingException(Exception):
    pass
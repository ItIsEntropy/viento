# Create a lock for POSIX or NT systems and present a platform agnostic API to users.

import os
from pathlib import Path
from typing import NoReturn, Callable

def lock_file(func: Callable[..., Path]) -> Path :
    def wrapper():
        open_file = func(*args, **kwargs)
        if os.name == 'nt':
            import win32con, win32file, pywintypes
            LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
            LOCK_SH = 0 # Shared lock is default lock
            LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
            overlapped = pywintypes.OVERLAPPED()
    return wrapper

def unlock_file(func) -> NoReturn :
    pass

class FileLockingException(Exception):
    pass
# Create a lock for POSIX or NT systems and present a platform agnostic API to users.
import io
import os
import sys
from pathlib import Path
from typing import NoReturn


def lock_file(file_name: Path, mode: str = 'r', blocking: bool = True) -> NoReturn:
    """
    Synchronously lock a file. Use either a blocking or non-blocking lock based on the above command.
    :param file_name: Path file representing the path to the file to lock
    :param mode: a string representing the mode to use when opening the file
    :param blocking: a boolean showing whether to use a blocking lock or not
    :return: NoReturn. does not return anything

    This method works on NT based, and POSIX compliant systems
    """
    # Define error variables

    with open(file=file_name, mode='w') as open_file:
        lock_mode: int = None
        write_modes: list[str] = ['w', 'w+', 'w+b', 'r+', 'r+b', 'a', 'a+b', 'ab', 'wb', 'wt', 'w+t']    
        read_modes: list[str] = ['r', 'rt', 'rb']
        if os.name == 'nt':  # systems with Windows NT kernel
            import msvcrt
            if mode in read_modes:  
                # reading the file, acquire a shared lock. Make it blocking if requested (blocking = True)
                lock_mode = msvcrt.LK_RLCK if blocking else msvcrt.LK_NBRLCK  
            elif mode in write_modes:  
                # writing to the file acquire an exclusive lock to prevent stale reads. Make it blocking if requested (blocking = True)
                lock_mode = msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK  
            n_bytes: int = open_file.seek(0, 2)  # get the full byte size of the file by seeking to the last byte then lock it
            msvcrt.locking(open_file.fileno(), lock_mode, n_bytes)
        elif os.name == 'posix':  # POSIX compliant systems
            import fcntl
            if mode in read_modes:  
                # reading the file, acquire a shared lock. Make it blocking if requested (blocking = True)
                lock_mode = fcntl.LOCK_SH if blocking else fcntl.LOCK_SH | fcntl.LOCK_NB
            elif mode in write_modes:  
                # writing to the file acquire an exclusive lock to prevent stale reads. Make it blocking if requested (blocking = True)
                lock_mode = fcntl.LOCK_EX if blocking else fcntl.LOCK_EX | fcntl.LOCK_NB
            fcntl.flock(open_file.fileno(), lock_mode)
        else: # Other, unknown systems
            msg: str = f"Unknown platform {sys.platform}.\n Mortice only supports 'Windows NT' and 'POSIX compliant' systems."
            raise RuntimeError(msg)
    


def unlock_file(file_name: Path, mode: str = 'r') -> NoReturn:
    """
        Synchronously ulock a file.
        :param file_name: Path file representing the path to the file to lock
        :param mode: a string representing the mode to use when opening the file
        :return: Does not return

        This method works on NT based, and POSIX compliant systems
    """

    try:
        open_file: Path = open_or_create(file_name, mode)
        if os.name == 'nt':  # systems with Windows NT kernel
            import msvcrt
            lock_mode: int = msvcrt.LK_UNLCK  # use unlock mode
            n_bytes: int = open_file.seek(0, 2)
            msvcrt.locking(open_file.fileno(), lock_mode, n_bytes)
        elif os.name == 'posix':  # POSIX compliant systems
            import fcntl
            lock_mode: int = fcntl.LOCK_UN  # use unlock mode
            fcntl.flock(open_file.fileno(), lock_mode)  # call system level fcntl function with flag to unlock file
        else:
            msg: str = f"Unknown platform {sys.platform}.\n Mortice only supports 'Windows NT' and 'POSIX' systems."
            raise RuntimeError(msg)
    except OSError as e:
        raise e
        pass  # TODO: Do something with the error, inform user and gracefully exit


async def lock_async(open_file: Path, mode: str) -> Path:
    pass  # TODO: flesh out


async def unlock_async(open_file: Path, mode: str) -> Path:
    pass  # TODO: flesh out

def acquire_lock(file_name: Path, mode: str = 'r', blocking: bool = True) -> io.TextIOWrapper :
    lock_file(file_name=file_name, mode=mode, blocking=blocking)
    pass
    

def get_file(file_name: Path, mode: str = 'r', blocking: bool = True) -> Path:
    def __enter__():
        data_file = open_or_create(file_name=file_name, mode=mode, blocking=blocking)
        return data_file


    def __exit__():
        # TODO close file
        # TODO: unlock file
        pass  # TODO: flesh out

    pass  # TODO: flesh out


async def get_file_async(file_name: Path, mode: str = 'r', blocking: bool = True) -> Path:
    def __enter__():
        pass  # TODO: flesh out

    def __exit__():
        pass  # TODO: flesh out

    pass  # TODO: flesh out

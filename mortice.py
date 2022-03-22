# Create a lock for POSIX or NT systems and present a platform agnostic API to users.
import os
import sys
from pathlib import Path
from typing import NoReturn


def open_or_create(file_name: Path, mode: str) -> Path:
    '''
    Opens a file with the given file name. if the file does not exist, it will be created.
    :param file_name: a Path object with the filename to be created
    :param mode: the access mode to open the file with
    :return: a Path object, the file requested by the caller.
    '''
    requested_file: Path = None
    if file_name.exists():
        requested_file = open(file_name, mode)
        # TODO: check for locks on the file.
    else:
        pass  # TODO create the file
    pass  # TODO: return file if it is not locked


def lock_file(file_name: Path, mode: str = 'r', blocking: bool = True) -> NoReturn:
    """
    Synchronously lock a file. Use either a blocking or non-blocking lock based on the above command.
    :param file_name: Path file representing the path to the file to lock
    :param mode: a string representing the mode to use when opening the file
    :param blocking: a boolean showing whether to use a blocking lock or not
    :return: Does not return

    This method works on NT based, and POSIX compliant systems
    """
    try:
        open_file: Path = open_or_create(file_name, mode)
        lock_mode: int = None
        if os.name == 'nt':  # systems with Windows NT kernel
            import msvcrt
            if mode == 'r':  # if we are trying to read the file, acquire a shared lock
                lock_mode = msvcrt.LK_RLCK if blocking else msvcrt.LK_NBRLCK  # get a blocking lock if blocking == True
            elif mode == 'w':  # if we are writing to the file acquire an exclusive lock to prevent stale reads
                lock_mode = msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK  # get a blocking lock if blocking == True
            else: # invalid access mode, raise error
                raise ValueError(f"unsupported open mode '{mode}'.\nvalid modes are:'r', 'w'")
            n_bytes: int = open_file.seek(0, 2)  # get the full byte size of the file by seeking to the last byte
            try:
                msvcrt.locking(open_file.fileno(), lock_mode, n_bytes)  # Lock the file with given mode
            except OSError as e:
                raise e
                pass  # TODO: Do something with the error, inform user and gracefully exit
        elif os.name == 'posix':  # POSIX compliant systems
            import fcntl
            if mode == 'r':  # if we are trying to read the file, acquire a shared lock
                # get a blocking lock if blocking == True
                lock_mode = fcntl.LOCK_SH if blocking else fcntl.LOCK_SH | fcntl.LOCK_NB
            elif mode == 'w':  # if we are writing to the file acquire an exclusive lock to prevent stale reads
                # get a blocking lock if blocking == True
                lock_mode = fcntl.LOCK_EX if blocking else fcntl.LOCK_EX | fcntl.LOCK_NB
            else: # invalid access mode, raise error
                raise ValueError(f"unsupported open mode '{mode}'.\nvalid modes are:'r', 'w'")
            fcntl.flock(open_file.fileno(), lock_mode)
        else:
            msg: str = f"Unknown platform {sys.platform}.\n Mortice only supports 'Windows NT' and 'POSIX' systems."
            raise RuntimeError(msg)
    except FileNotFoundError as e:
        pass  # TODO: Do something with the error, inform user and gracefully exit


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
        pass  # TODO: Do something with the error, inform user and gracefully exit


async def lock_async(open_file: Path, mode: str) -> Path:
    pass  # TODO: flesh out


async def unlock_async(open_file: Path, mode: str) -> Path:
    pass  # TODO: flesh out


def get_file(file_name: Path, mode: str = 'r', blocking: bool = True) -> Path:
    def __enter__():
        pass  # TODO: flesh out

    def __exit__():
        pass  # TODO: flesh out

    pass  # TODO: flesh out


async def get_file_async(file_name: Path, mode: str = 'r', blocking: bool = True) -> Path:
    def __enter__():
        pass  # TODO: flesh out

    def __exit__():
        pass  # TODO: flesh out

    pass  # TODO: flesh out

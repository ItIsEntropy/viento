# Create a lock for POSIX or NT systems and present a platform agnostic API to users.
import fileinput
import os
import msvcrt
import sys
from pathlib import Path
from typing import NoReturn, Callable


def lock_file(file_name: Path, mode: str = 'r', blocking=True) -> NoReturn:
    """
    Synchronously lock a file. Use either a blocking or non-blocking lock based on the above command.
    :param file_name: Path file representing the path to the file to lock
    :param mode: a string representing the mode to use when opening the file
    :param blocking: a boolean showing whether to use a blocking lock or not
    :return: Does not return

    This method works on NT based, and POSIX compliant systems
    """
    try:
        open_file: Path = open(file_name, mode)
        position: int = open_file.tell()  # get the current byte position in the file
        if os.name == 'nt':
            lock_mode: int = msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK
            n_bytes: int = open_file.seek(0, 2)
            try:
                msvcrt.locking(open_file.fileno(), lock_mode, n_bytes)
            except OSError as e:
                raise e
                pass  # TODO: Do something with the error, inform user and gracefully exit
        elif os.name == 'posix':

            pass
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
        open_file: Path = open(file_name, mode)
        if os.name == 'nt':
            lock_mode: int = msvcrt.LK_UNLCK
            n_bytes: int = open_file.seek(0, 2)
            try:
                msvcrt.locking(open_file.fileno(), lock_mode, n_bytes)
            except OSError as e:
                raise e
                pass  # TODO: Do something with the error, inform user and gracefully exit
            pass
        elif os.name == 'posix':
            pass
        else:
            msg: str = f"Unknown platform {sys.platform}.\n Mortice only supports 'Windows NT' and 'POSIX' systems."
            raise RuntimeError(msg)
        pass
    except OSError as e:
        pass # TODO: Do something with the error, inform user and gracefully exit
    pass


async def lock_async(open_file: Path, mode: str) -> Path:
    pass

async def unlock_async(open_file: Path, mode: str) -> Path:
    pass


class FileLockingException(Exception):
    pass

# Create a lock for POSIX or NT systems and present a platform agnostic API to users.
import io
import os
import sys
import asyncio
import time
from pathlib import Path

# Static vars to store error names
E_WOULD_BLK: str = 'Would Block'
E_NOT_LK: str = 'Already locked'
# a dictionary storing error numbers for platforms
os_errors: dict[str, dict[[str, int]]] = {
    'nt': {
        E_WOULD_BLK: 36,
        E_NOT_LK: 13,
    },
    'posix': {
        E_WOULD_BLK: 36,  # TODO: get posix value
        E_NOT_LK: 13,  # TODO: get posix value
    },
}


class Mortice:
    """
    A class to provide a static method, and context manager to lock and unlock files.
    This class has both synchronous and asynchronous methods to handle file locking.
    """

    @staticmethod
    def lock_file(open_file: io.TextIOWrapper, mode: str = 'r', blocking: bool = True) -> None:
        """
        Synchronously lock a file. Use either a blocking or non-blocking lock based on the above command.
        :param open_file: TextIOWrapper file to be locked
        :param mode: a string representing the mode to use when opening the file
        :param blocking: a boolean showing whether to use a blocking lock or not
        :return: NoReturn. does not return anything

        This method works on NT based, and POSIX compliant systems
        """
        lock_mode: int = 0
        write_modes: list[str] = ['w', 'w+', 'w+b', 'r+', 'r+b', 'a', 'a+b', 'ab', 'wb', 'wt', 'w+t']
        read_modes: list[str] = ['r', 'rt', 'rb']
        if os.name == 'nt':  # systems with Windows NT kernel
            import msvcrt
            if mode in read_modes:
                # reading the file, acquire a shared lock. Make it blocking if requested (blocking = True)
                lock_mode = msvcrt.LK_RLCK if blocking else msvcrt.LK_NBRLCK
            elif mode in write_modes:
                # writing to the file, acquire an exclusive lock to prevent stale reads.
                # Make it blocking if requested (blocking = True)
                lock_mode = msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK
            n_bytes: int = open_file.seek(0, 2)  # get the full byte size of the file
            msvcrt.locking(open_file.fileno(), lock_mode, n_bytes)
        elif os.name == 'posix':  # POSIX compliant systems
            import fcntl
            if mode in read_modes:
                # reading the file, acquire a shared lock. Make it blocking if requested (blocking = True)
                lock_mode = fcntl.LOCK_SH if blocking else fcntl.LOCK_SH | fcntl.LOCK_NB
            elif mode in write_modes:
                # writing to the file, acquire an exclusive lock to prevent stale reads.
                # Make it blocking if requested (blocking = True)
                lock_mode = fcntl.LOCK_EX if blocking else fcntl.LOCK_EX | fcntl.LOCK_NB
            fcntl.flock(open_file.fileno(), lock_mode)
        else:  # Other, unknown systems
            msg: str = f"""Unknown platform {sys.platform}.\n 
            Mortice only supports 'Windows NT' and 'POSIX compliant' systems."""
            raise RuntimeError(msg)

    @staticmethod
    def unlock_file(open_file: io.TextIOWrapper) -> None:
        """
            Synchronously ulock a file.
            :param open_file: TextIOWrapper file to be unlocked
            :return: Does not return

            This method works on NT based, and POSIX compliant systems
        """
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

    def __init__(self, file_path: Path | str, mode: str = 'r', blocking: bool = True) -> None:
        if isinstance(file_path, str):  # convert strings to Paths
            file_path = Path(os.getcwd()).joinpath(file_path)
        self.open_file: io.TextIOWrapper = open(file=file_path, mode=mode)
        print(f'file: {self.open_file}')
        self.mode: str = mode
        self.blocking: bool = blocking

    def __enter__(self) -> io.TextIOWrapper:
        wait_time: int = 1
        while True:
            try:
                print('locking')
                self.lock_file(self.open_file, self.mode, self.blocking)
                print('locked')
                return self.open_file
            except OSError as e:
                if e.errno == os_errors[os.name][E_WOULD_BLK]:  # file already locked, retry
                    if self.blocking:  # If the caller doesn't mind being blocked, gracefully degrade, otherwise raise e
                        time.sleep(wait_time)
                        wait_time += 2  # increase wait time
                        if wait_time > 10:  # drop off request, wait is too long
                            raise e
                    else:
                        raise e
                else:  # unknown error, raise it
                    raise e

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if isinstance(exc_value, OSError):
            # Handle OS error by errno here...
            print(f"This exception occurred trying to lock the file: {exc_type}")
            print(f"Exception message: {exc_value}")
            if exc_value.errno == os_errors[os.name][E_NOT_LK]:  # already unlocked or no permission
                return True
            return False
        else:
            print('unlocking')
            self.unlock_file(self.open_file)
            print('unlocked')
            return True

    async def __aenter__(self) -> io.TextIOWrapper:
        wait_time: int = 1
        while True:
            try:
                self.lock_file(self.open_file, self.mode, self.blocking)
                return self.open_file
            except OSError as e:
                if e.errno == os_errors[os.name][E_WOULD_BLK]:  # file already locked, retry
                    if self.blocking:  # If the caller doesn't mind being blocked, gracefully degrade, otherwise raise e
                        await asyncio.sleep(wait_time)
                        wait_time += 2  # increase wait time
                        if wait_time > 10:
                            raise e
                    else:
                        raise e
                else:  # unknown error, raise it
                    raise e

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> bool:
        self.unlock_file(self.open_file)
        if isinstance(exc_value, OSError):
            # Handle OS error by errno here...
            print(f"This exception occurred trying to lock the file: {exc_type}")
            print(f"Exception message: {exc_value}")
            return True
        else:
            return False

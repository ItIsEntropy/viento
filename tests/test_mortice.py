import pytest
import os
import io
import tempfile
from pathlib import Path
from src.mortice.mortice import Mortice

## Arrange step
@pytest.fixture
def create_temp_file() -> io.TextIOWrapper:
    """
    Fixture that creates temporary file
    :return: a temporary io.TextIOWrapper object
    """
    test_file: io.TextIOWrapper = tempfile.TemporaryFile()
    return test_file

@pytest.fixture
def lock_file(create_temp_file) -> io.TextIOWrapper:
    """
    Lock a file and return it to the dependant test(s) and/or fixture(s)
    :param create_temp_file: fixture that creates a temporary file
    :return:
    """
    locked_file: io.TextIOWrapper = create_temp_file
    if os.name == 'nt':
        import msvcrt
        mode: int = msvcrt.LK_NBLCK
        n_bytes: int = locked_file.seek(0, 2)
        msvcrt.locking(locked_file.fileno(), mode, n_bytes)
        return locked_file
    elif os.name == 'posix':
        import fcntl
        mode: int = fcntl.LOCK_EX | fcntl.LOCK_NB
        fcntl.flock(locked_file.fileno(), mode)
        return locked_file

deadlock_error: dict[str, int] = {'nt': 36, 'posix': 26}# TODO: get POSIX number

# TODO: lock with app and then use non blocking mode in a fixture to ensure OSError is raised.
def test_context(lock_file, create_temp_file) -> None:
    """
    Test the context manager mode
    :return: None
    """
    with pytest.raises(Exception) as e:
        with Mortice(file_path=lock_file, mode='w', blocking=False):
            pass
    assert e.value.errno == deadlock_error[os.name]

@pytest.mark.anyio
async def test_async_context(lock_file) -> None:
    """
    Test the asynchronous context manager
    :return: None
    """
    with pytest.raises(Exception) as e:
        async with Mortice(file_path=lock_file, mode='w', blocking=False):
            pass
    assert e.value.errno == deadlock_error[os.name]

def test_lock(lock_file) -> None:
    """
    Test the locking API
    :return: None
    """
    with pytest.raises(OSError) as e:
        Mortice.lock_file(lock_file)
    assert e.value.errno == deadlock_error[os.name]
def tet_unlock() -> None:
    """
    test unlock API
    :return: None
    """
    pass #TODO use fixture to unlock and test that app raises an error when called or vice versa

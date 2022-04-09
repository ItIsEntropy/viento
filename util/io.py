# TODO: create logic to make a file given a file name.
# TODO: make a bg task that deletes the file after 10 minutes.
# TODO: if file is locked then repeat after one sec ad infinitum till the file is deleted.


from importlib.metadata import entry_points
from typing import Any

async def get_file_locker() -> dict[str, Any]:
    '''
    Checks installed entrypoints for a file locking context manager that's registered to work with viento.
    '''
    # TODO make empty dict of entrypoints for lockers
    # TODO: add lockers to the dict by entrypoint name
    lockers: dict[str, Any]
    for entry_point in entry_points('viento.file_lockers'):
        lockers[entry_point.name] = entry_point
    return lockers
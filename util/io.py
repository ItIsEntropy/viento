# TODO: create logic to make a file given a file name.
# TODO: make a bg task that deletes the file after 10 minutes.
# TODO: if file is locked then repeat after one sec ad infinitum till the file is deleted.
import importlib.metadata
import io
import os
import yaml
from pathlib import Path
from typing import Any
from decouple import Config # TODO: replace with yaml configs

async def get_file_locker() -> Any:
    '''
    Checks installed entrypoints for a file locking context manager that's registered to work with viento.
    '''
    # get all viento.filelocker entrypoints, and make a dictionary of `{locker_name: file_locker}`
    lockers: dict[str, Any] = {
        entrypoint.name: entrypoint for entrypoint in importlib.metadata.entry_points().select()['viento.file_lockers']
    }
    working_dir: Path = Path(os.getcwd())
    with open(working_dir.joinpath('config.yaml'), 'r') as config_file:
        locker_setting: str = yaml.load(config_file)['file_locker']
        locker_name: str = 'mortice' if locker_setting is None else locker_setting
        try:
            return lockers[locker_name].load()
        except KeyError:
            msg = f'File locker {locker_name} is not available.\navailabler file lockers: {", ".join(sorted(lockers))}'
            print(msg) # TODO: Log this properly
        raise ValueError(msg)
        
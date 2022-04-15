import argparse
import os
from pathlib import Path
from mortice import Mortice
import importlib.metadata


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Lock or unlock a file")
    parser.add_argument('-l', default=None)
    parser.add_argument('--lock', default=None)
    parser.add_argument('-u', default=None)
    parser.add_argument('--unlock', default=None)
    args: argparse.Namespace = parser.parse_args()

    if args.lock is not None or args.l is not None:
        file_name: str = args.lock if args.lock is not None else args.l
        location: Path = Path(os.getcwd()).joinpath(file_name)
        with open(location) as open_file:
            Mortice.lock_file(open_file=open_file)
    elif args.unlock is not None or args.u is not None:
        file_name: str = args.unlock if args.unlock is not None else args.u
        location: Path = Path(os.getcwd()).joinpath(file_name)
        with open(location) as open_file:
            Mortice.unlock_file(open_file=open_file)
    else:
        raise ValueError('Provide an argument and filename to use this program')
    return 0  # parse args to make locks


if __name__ == '__main__':
    exit(main())

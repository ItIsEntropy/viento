import importlib.metadata
import logging


async def get_handlers() -> list[logging.Handler]:
    '''
    Check installed entrypoints fo a log handler that advertises itself as capabe of working with vient via the 
    `viento.log_handlers` entrypoint and returns them in a list
    '''
    # get all viento.log_handlers entrypoints, and make a list of log handlers from it
    handlers: dict[str, logging.Handler] = [
        entrypoint for entrypoint in importlib.metadata.entry_points().select()['viento.log_handlers']
    ]
    return handlers

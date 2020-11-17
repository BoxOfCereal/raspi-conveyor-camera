import asyncio
from kasa import SmartPlug
import traceback
import logging
from functools import wraps

from modules.settings import load_settings
settings = load_settings()


def aio_wrapper(f):
    """wraps the async functions"""
    @wraps(f)
    def decor(*args,**kwargs):
        return asyncio.run(f(*args,**kwargs))
    return decor

@aio_wrapper
async def turn_on_plug():
    """turn on plug"""
    try:
        p = SmartPlug(settings["smart_plug_ip"])

        await p.update()
        logging.debug('Plug Turned On')

        await p.turn_on()
    except:
        logging.error(traceback.format_exc())
   
@aio_wrapper
async def turn_off_plug():
    """turn off plug"""
    try:
        p = SmartPlug(settings["smart_plug_ip"])

        await p.update()
        logging.debug('Plug Turned Off')

        await p.turn_off()
    except:
        logging.error(traceback.format_exc())


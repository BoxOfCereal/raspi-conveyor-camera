import asyncio
from kasa import SmartPlug
import traceback

from modules.settings import load_settings
settings = load_settings()

async def init_plug():
    """init smart plug with ip denoted in settings"""
    try:
        return SmartPlug(settings["smart_plug_ip"])
    except:
        print(traceback.format_exc())
        
    

async def turn_on(plug):
    """turn on plug"""
    try:
        plug.turn_on()
    except:
        print(traceback.format_exc())
   

async def turn_off(plug):
    """turn on plug"""
    try:
        plug.turn_off()
    except:
        print(traceback.format_exc())


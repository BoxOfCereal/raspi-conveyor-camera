import asyncio
from kasa import SmartPlug

# get plug
plug_address = '192.168.0.39'

#everything needs to be run with asyncio updates
plug = SmartPlug(plug_address)
asyncio.run(plug.set_alias("conveyor_0"))
asyncio.run(plug.update())
asyncio.run(plug.turn_on())
print(plug.alias)
import discord
from threading import Thread
import time
import asyncio
import sys

client = discord.Client()

class Pipe:
    def __init__(self):
        self._in = []
        self._out = []
    def put(self, value):
        self._in.append(value)
    def get(self):
        out = self._out[:]
        self._out = []
        return out
    
pipe = None
channel = None
is_ready = False
run = True

@client.event
async def on_ready():
    global pipe, channel, is_ready, run
    is_ready = True
    while True:
        await asyncio.sleep(1)
        for i in pipe._in:
            try:
                await client.send_message(client.get_channel(channel), i)
            except:
                pass
        pipe._in = []
        if not run:
            sys.exit(0)

@client.event
async def on_message(m):
    global pipe, channel
    if m.channel.id == channel:
        pipe._out.append(m.content)

def swarm_begin(tok, channel_id):
    global pipe, channel, client
    channel = channel_id
    pipe = Pipe()
    t = Thread(target=client.run, args=(tok,))
    t.start()
    return pipe, t

def end():
    global run
    run = False





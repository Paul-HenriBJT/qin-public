# examples/stream_from_microphone.py

import asyncio
from pyqin.client import WebsocketAudioClient
from pyqin.audio_streams import microphone_audio_stream
import pyaudio
import numpy as np

def play_audio(audio_chunk):
    # Play received audio
    # (Implementation same as above)
    pass

async def main():
    # Set up client and stream audio from microphone
    # (Implementation same as above)
    pass

if __name__ == "__main__":
    asyncio.run(main())

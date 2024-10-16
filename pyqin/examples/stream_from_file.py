# examples/stream_from_file.py

import asyncio
from ws_audio_client.client import WebsocketAudioClient
from ws_audio_client.audio_streams import file_audio_stream
import pyaudio
import numpy as np

def play_audio(audio_chunk):
    # Play received audio
    # (Implementation same as above)
    pass

async def main():
    API_KEY = "YOUR_API_KEY"
    WS_URL = "ws://localhost:8000/ws"

    client = WebsocketAudioClient(
        api_key=API_KEY,
        ws_url=WS_URL,
        language="en-US",
        voice_id="your_voice_id",
        speed="normal",
        on_audio_received=play_audio
    )

    await client.connect()

    # Stream audio from a file
    FILE_PATH = "path/to/your/audiofile.wav"
    audio_generator = file_audio_stream(FILE_PATH)

    await client.stream_audio(audio_generator)

if __name__ == "__main__":
    asyncio.run(main())

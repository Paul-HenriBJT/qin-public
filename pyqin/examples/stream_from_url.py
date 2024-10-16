# examples/stream_from_url.py

import asyncio
from ws_audio_client.client import WebsocketAudioClient
from ws_audio_client.audio_streams import url_audio_stream
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

    # Stream audio from a URL
    STREAM_URL = "https://example.com/audio_stream.mp3"
    audio_generator = url_audio_stream(STREAM_URL)

    await client.stream_audio(audio_generator)

if __name__ == "__main__":
    asyncio.run(main())

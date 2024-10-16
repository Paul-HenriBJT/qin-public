# File: examples/stream_from_microphone.py

import asyncio
from pyqin.client import WebsocketAudioClient
from pyqin.audio_streams import microphone_audio_stream

async def main():
    # Replace with your actual API key
    API_KEY = "YOUR_API_KEY"


    client = WebsocketAudioClient(
        api_key=API_KEY,
        language="en-US",
        voice_id="default_voice_id",
        speed="normal"
    )

    await client.connect()

    # Start the audio player

    # Create an asynchronous generator for microphone audio
    audio_generator = microphone_audio_stream(
        chunk_size=1024,
        sample_rate=44100,
        channels=1
    )

    try:
        streaming_task = asyncio.create_task(client.stream_audio(audio_generator))
        await asyncio.gather(streaming_task, client.receive_task)
    except asyncio.CancelledError:
        print("Streaming cancelled")
    finally:
        # Close the client and stop the audio player
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())

# File: examples/stream_from_file.py

import asyncio
from pyqin.client import WebsocketAudioClient
from pyqin.audio_streams import file_audio_stream


async def main():
    # Replace with your actual API key
    API_KEY = "YOUR_API_KEY"

    # Path to your audio file (WAV format)
    AUDIO_FILE_PATH = "path/to/your/audiofile.wav"


    client = WebsocketAudioClient(
        api_key=API_KEY,
        language="en-US",
        voice_id="default_voice_id",
        speed="normal"
    )

    await client.connect()

    # Create an asynchronous generator for file audio
    audio_generator = file_audio_stream(
        file_path=AUDIO_FILE_PATH,
        chunk_size=1024
    )

    try:
        # Start streaming audio
        streaming_task = asyncio.create_task(client.stream_audio(audio_generator))
        await asyncio.gather(streaming_task, client.receive_task)
    except asyncio.CancelledError:
        print("Streaming cancelled")
    finally:
        # Close the client and stop the audio player
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())

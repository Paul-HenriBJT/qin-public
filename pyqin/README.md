# WebSocket Client Package

A Python client package to interact seamlessly with the custom WebSocket server.

## Features

- **Authentication**: Authenticate with the server using API keys.
- **Configuration**: Set and update session parameters like language, voice, and speed.
- **Audio Handling**: Send audio data and receive transcriptions and audio responses.
- **Callbacks**: Handle events via asynchronous callbacks.

## Installation

```bash
pip install websocket_client_package
```

## Usage 

import asyncio
from pyqin import WebSocketClient, AuthenticationError, ConfigurationError

async def on_auth_success():
    print("Authenticated successfully!")

async def on_auth_failure(reason):
    print(f"Authentication failed: {reason}")

async def on_config_success():
    print("Configuration set successfully!")

async def on_config_failure(reason):
    print(f"Configuration failed: {reason}")

async def on_audio_received(audio_bytes):
    with open("received_audio.raw", "wb") as f:
        f.write(audio_bytes)
    print("Received audio data")

async def on_transcription_received(transcription):
    print(f"Received transcription: {transcription}")

async def main():
    client = WebSocketClient(
        url="ws://localhost:8000/ws",
        api_key="YOUR_API_KEY",
        on_auth_success=on_auth_success,
        on_auth_failure=on_auth_failure,
        on_config_success=on_config_success,
        on_config_failure=on_config_failure,
        on_audio_received=on_audio_received,
        on_transcription_received=on_transcription_received,
    )

    async with client:
        # Set initial configuration
        await client.set_params(
            language="zh",
            voice_id="e3827ec5-697a-4b7c-9704-1a23041bbc51",
            speed="normal",
            context="General context here"
        )

        # Send audio data
        with open("audio_sample.raw", "rb") as f:
            audio_bytes = f.read()
        timestamp = asyncio.get_event_loop().time()
        await client.send_audio(audio_bytes, timestamp)

        # Keep the client running to listen for messages
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())

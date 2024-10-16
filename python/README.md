# Pyqin

A Python client package to interact seamlessly with a websocket audio processing server. This package handles authentication, configuration, audio streaming, and receiving processed audio data, making it easy to integrate with the server's API.

## Features

- **Easy Authentication**: Simplify the process of connecting and authenticating with the server.
- **Dynamic Configuration**: Update session parameters like language, voice ID, and speed on the fly.
- **Audio Streaming**: Stream audio from various sources (microphone, URL, or file) to the server.
- **Receive Processed Audio**: Receive and handle processed audio data from the server with customizable callbacks.
- **Asynchronous Design**: Built using `asyncio` for efficient IO-bound operations.

## Installation

```bash
pip install pyqin
```

Alternatively, clone the repository and install locally:

```bash
git clone https://github.com/Paul-HenriBJT/qin-public.git
cd pyquin
pip install .
```

## Requirements

- Python 3.6 or higher
- See [requirements.txt](https://github.com/Paul-HenriBJT/qin-public/blob/main/pyqin/requirements.txt) for package dependencies.

## Usage

### Basic Example

```python
import asyncio
from pyqin.client import WebsocketAudioClient
from pyqin.audio_streams import microphone_audio_stream
import pyaudio
import numpy as np

def play_audio(audio_chunk):
    # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # Convert bytes to numpy array
    audio_data = np.frombuffer(audio_chunk, dtype=np.float32)

    # Play audio
    stream.write(audio_data.tobytes())

    # Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

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

    # Stream audio from the microphone
    audio_generator = microphone_audio_stream()

    # Start streaming audio
    await client.stream_audio(audio_generator)

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples

Additional examples are available in the [/examples](https://github.com/Paul-HenriBJT/qin-public/tree/main/pyqin/examples) directory:

- Stream Audio from Microphone
- Stream Audio from URL
- Stream Audio from Audio File

## API Reference

### WebsocketAudioClient

#### Initialization

```python
client = WebsocketAudioClient(
    api_key: str,
    ws_url: str = "ws://localhost:8000/ws",
    language: str = "en-US",
    voice_id: str = "default_voice_id",
    speed: str = "normal",
    on_audio_received: Optional[Callable[[bytes], None]] = None,
)
```

- `api_key`: Your API key for authentication.
- `ws_url`: WebSocket server URL.
- `language`: Language code for the session.
- `voice_id`: Voice ID for text-to-speech.
- `speed`: Speed of the speech ("slowest", "slow", "normal", "fast", "fastest").
- `on_audio_received`: Callback function to handle received audio data.

#### Methods

- `await connect()`: Establishes a connection and authenticates with the server.
- `await stream_audio(audio_generator: AsyncGenerator[bytes, None])`: Streams audio data to the server.
- `await update_configuration(**kwargs)`: Updates session parameters dynamically.
- `await close()`: Closes the connection and cleans up resources.

### Audio Stream Utilities

- `microphone_audio_stream(chunk_size=1024, sample_rate=44100, channels=1)`: Captures audio from the microphone.
- `file_audio_stream(file_path, chunk_size=1024)`: Reads audio data from a file.
- `url_audio_stream(url, chunk_size=1024)`: Streams audio data from a URL.

## Error Handling

Custom exceptions are defined in `pyqin.exceptions`:

- `WebsocketAudioClientError`: Base exception class.
- `AuthenticationError`: Raised when authentication fails.
- `ConfigurationError`: Raised when configuration fails.
- `StreamingError`: Raised when streaming encounters an error.

## Logging

Logging is implemented using Python's built-in logging module. You can configure logging as needed in your application:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Paul-HenriBJT/qin-public/blob/main/LICENSE) file for details.
# File: examples/stream_from_url.py

import asyncio
from pyqin.client import WebsocketAudioClient
from pyqin.audio_streams import url_audio_stream

async def main():
    API_KEY = "dZ5TKxDardtOBHf0IFYefpkFVZbSz2kWJ1wdFCFMPMc"
    WS_URL = "ws://localhost:8000/ws"

    client = WebsocketAudioClient(
        api_key=API_KEY,
        ws_url=WS_URL,
        language="fr-FR",
        speed="normal",
        voice_id="tavIIPLplRB883FzWU0V"
    )

    await client.connect()

    STREAM_URL = "https://audio.bfmtv.com/rmcradio_128.mp3?aw_0_1st.playerId=tunein&aw_0_1st.aggregator=tunein"
    audio_generator = url_audio_stream(STREAM_URL)

    try:
        streaming_task = asyncio.create_task(client.stream_audio(audio_generator))
        await asyncio.gather(streaming_task, client.receive_task)
    except asyncio.CancelledError:
        print("Streaming cancelled")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
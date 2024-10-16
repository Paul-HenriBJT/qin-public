import asyncio
import pyaudio

async def microphone_audio_stream(chunk_size=1024, sample_rate=44100, channels=1):
    """
    Asynchronous generator that yields audio chunks from the microphone.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            yield data
            await asyncio.sleep(0)  # Yield control to the event loop
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def file_audio_stream(file_path, chunk_size=1024):
    """
    Asynchronous generator that yields audio chunks from an audio file.
    """
    import wave
    with wave.open(file_path, 'rb') as wf:
        data = wf.readframes(chunk_size)
        while data:
            yield data
            data = wf.readframes(chunk_size)
            await asyncio.sleep(0)

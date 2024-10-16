import pyaudio
import asyncio

class AudioPlayer:
    def __init__(self, channels=1, rate=44100, chunk_size=1024, buffer_size=100, format=pyaudio.paFloat32):
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.buffer = asyncio.Queue(maxsize=buffer_size)
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.play_task = None
        self.format = format

    async def start(self):
        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk_size
        )
        # Start the playback task
        self.play_task = asyncio.create_task(self._play_audio())

    async def stop(self):
        # Signal the playback task to stop
        if self.play_task:
            self.play_task.cancel()
            try:
                await self.play_task
            except asyncio.CancelledError:
                pass
        if self.stream:
            await asyncio.to_thread(self.stream.stop_stream)
            await asyncio.to_thread(self.stream.close)
        await asyncio.to_thread(self.pyaudio_instance.terminate)

    async def play_audio(self, audio_chunk):
        await self.buffer.put(audio_chunk)

    async def _play_audio(self):
        try:
            while True:
                chunk = await self.buffer.get()
                await asyncio.to_thread(self.stream.write, chunk)
        except asyncio.CancelledError:
            pass

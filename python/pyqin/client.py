import asyncio
import base64
import json
import time
import websockets
import pyaudio
import logging
from .audio_player import AudioPlayer
from typing import Optional, Callable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Adjust as needed

class WebsocketAudioClient:
    def __init__(
        self,
        api_key: str,
        ws_url: str = "ws://localhost:8000/ws",
        language: str = "fr-FR",
        voice_id: str = "3b554273-4299-48b9-9aaf-eefd438e3941",
        speed: str = "normal",
        on_audio_received: Optional[Callable[[bytes], None]] = None,
        audio_player: Optional[AudioPlayer] = None,
    ):
        self.api_key = api_key
        self.ws_url = ws_url
        self.language = language
        self.voice_id = voice_id
        self.speed = speed

        # Initialize AudioPlayer if not provided
        self.audio_player = audio_player or AudioPlayer(
            channels=1, rate=44100, format=pyaudio.paFloat32
        )

        # Set the on_audio_received callback
        self.on_audio_received = on_audio_received or self.audio_player.play_audio

        self.websocket = None
        self.receive_task = None
        self.connected = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.ws_url)
            logger.info("WebSocket connection established.")
            await self.authenticate()
            await self.send_configuration()
            self.connected = True
            # Start the audio player if using the default callback
            if self.on_audio_received == self.audio_player.play_audio:
                await self.audio_player.start()
            # Start the receive task
            self.receive_task = asyncio.create_task(self.receive_audio())
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise

    async def authenticate(self):
        auth_message = {
            "action": "authenticate",
            "api_key": self.api_key
        }
        await self.websocket.send(json.dumps(auth_message))
        logger.info("Sent authentication message.")

        response = await self.websocket.recv()
        response_data = json.loads(response)
        if response_data.get("action") == "authentication":
            if response_data.get("status") == "success":
                logger.info("Authentication successful.")
            else:
                reason = response_data.get("reason", "No reason provided.")
                logger.error(f"Authentication failed: {reason}")
                await self.websocket.close()
                raise Exception(f"Authentication failed: {reason}")
        else:
            logger.error("Unexpected response during authentication.")
            await self.websocket.close()
            raise Exception("Unexpected response during authentication.")

    async def send_configuration(self):
        config_message = {
            "action": "set_params",
            "language": self.language,
            "voice_id": self.voice_id,
            "speed": self.speed
        }
        await self.websocket.send(json.dumps(config_message))
        logger.info("Sent configuration parameters.")

        response = await self.websocket.recv()
        response_data = json.loads(response)
        if response_data.get("action") == "set_params" and response_data.get("status") == "success":
            logger.info("Configuration successful.")
        else:
            reason = response_data.get("reason", "Unknown error")
            logger.error(f"Configuration failed: {reason}")
            await self.websocket.close()
            raise Exception(f"Configuration failed: {reason}")

    async def stream_audio(self, audio_generator):
        if not self.connected:
            await self.connect()

        try:
            async for audio_chunk in audio_generator:
                base64_chunk = base64.b64encode(audio_chunk).decode('utf-8')
                audio_message = {
                    "audio": base64_chunk,
                    "timestamp": time.time()
                }
                await self.websocket.send(json.dumps(audio_message))
                logger.debug("Sent audio chunk.")
        except asyncio.CancelledError:
            logger.info("Audio streaming cancelled.")
        except Exception as e:
            logger.error(f"Error during audio streaming: {e}")
            raise

    async def receive_audio(self):
        try:
            while True:
                audio_chunk = await self.websocket.recv()
                if isinstance(audio_chunk, bytes):
                    if self.on_audio_received:
                        await self.on_audio_received(audio_chunk)
                    else:
                        logger.warning("No handler for received audio.")
                else:
                    logger.warning("Received non-bytes message from server.")
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed during audio reception.")
        except Exception as e:
            logger.error(f"Error in receive_audio: {e}")
            raise

    async def update_configuration(self, **kwargs):
        config_message = {
            "action": "update_params",
        }
        allowed_params = ['language', 'voice_id', 'speed', 'context']
        for key, value in kwargs.items():
            if key in allowed_params:
                config_message[key] = value
                setattr(self, key, value)  # Update the instance variable
            else:
                logger.warning(f"Ignoring invalid configuration parameter: {key}")

        await self.websocket.send(json.dumps(config_message))
        logger.info("Sent update configuration parameters.")

        response = await self.websocket.recv()
        response_data = json.loads(response)
        if response_data.get("action") == "update_params" and response_data.get("status") == "success":
            logger.info("Configuration updated successfully.")
        else:
            reason = response_data.get("reason", "Unknown error")
            logger.error(f"Configuration update failed: {reason}")
            raise Exception(f"Configuration update failed: {reason}")

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logger.info("WebSocket connection closed.")
        if self.receive_task:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                pass
        self.connected = False
        logger.info("Client closed.")

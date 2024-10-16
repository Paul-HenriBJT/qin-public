# websocket_client/utils.py

import base64

def encode_audio(audio_bytes: bytes) -> str:
    return base64.b64encode(audio_bytes).decode('utf-8')

def decode_audio(audio_str: str) -> bytes:
    return base64.b64decode(audio_str)

# websocket_client/models.py

from pydantic import BaseModel
from typing import Optional

class AudioMessage(BaseModel):
    audio: str  # Base64 encoded audio data
    timestamp: float

class AuthMessage(BaseModel):
    action: str
    api_key: str

class ConfigMessage(BaseModel):
    action: str
    language: Optional[str] = None
    voice_id: Optional[str] = None
    speed: Optional[str] = None
    context: Optional[str] = None

class UpdateParamsMessage(BaseModel):
    action: str
    voice_id: Optional[str] = None
    speed: Optional[str] = None

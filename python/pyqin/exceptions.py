class WebsocketAudioClientError(Exception):
    """Base exception class for WebsocketAudioClient errors."""
    pass

class AuthenticationError(WebsocketAudioClientError):
    """Raised when authentication fails."""
    pass

class ConfigurationError(WebsocketAudioClientError):
    """Raised when configuration fails."""
    pass

class StreamingError(WebsocketAudioClientError):
    """Raised when streaming encounters an error."""
    pass

class ConnectionError(WebsocketAudioClientError):
    """Raised when connection fails."""
    pass
# src/youtube_processor/exceptions.py
from typing import Any, Dict, Optional


class YouTubeProcessorError(Exception):
    """Base exception for all YouTube processor errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class ConfigurationError(YouTubeProcessorError):
    """Raised when there are issues with configuration or environment setup."""

    pass


class CredentialsError(YouTubeProcessorError):
    """Raised when there are issues with API credentials or authentication."""

    def __init__(self, message: str, credentials_path: Optional[str] = None) -> None:
        details = {"credentials_path": credentials_path} if credentials_path else {}
        super().__init__(message, details)


class APIError(YouTubeProcessorError):
    """Base class for API-related errors."""

    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None) -> None:
        details = {"response": response} if response else {}
        super().__init__(message, details)


class VideoDownloadError(YouTubeProcessorError):
    """Raised when video download fails."""

    def __init__(
        self, message: str, url: str, error_details: Optional[Dict[str, Any]] = None
    ) -> None:
        details = {"url": url, **error_details} if error_details else {"url": url}
        super().__init__(message, details)


class VideoProcessingError(YouTubeProcessorError):
    """Raised when video processing operations fail."""

    def __init__(
        self,
        message: str,
        file_path: str,
        error_details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = (
            {"file_path": file_path, **error_details}
            if error_details
            else {"file_path": file_path}
        )
        super().__init__(message, details)


class VideoUploadError(YouTubeProcessorError):
    """Raised when video upload to YouTube fails."""

    def __init__(
        self,
        message: str,
        file_path: str,
        error_details: Optional[Dict[str, Any]] = None,
    ) -> None:
        details = (
            {"file_path": file_path, **error_details}
            if error_details
            else {"file_path": file_path}
        )
        super().__init__(message, details)


class RetryableError(YouTubeProcessorError):
    """Base class for errors that can be retried."""

    def __init__(
        self, message: str, retry_after: int = 0, max_retries: Optional[int] = None
    ) -> None:
        details = {"retry_after": retry_after, "max_retries": max_retries}
        super().__init__(message, details)


class QuotaExceededError(RetryableError):
    """Raised when YouTube API quota is exceeded."""

    def __init__(self, message: str, quota_reset_time: Optional[str] = None) -> None:
        details = {"quota_reset_time": quota_reset_time} if quota_reset_time else {}
        super().__init__(message, details=details)


class RateLimitError(RetryableError):
    """Raised when rate limits are hit."""

    pass


class NetworkError(RetryableError):
    """Raised when network-related issues occur."""

    pass


class ValidationError(YouTubeProcessorError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str, value: Any) -> None:
        details = {"field": field, "value": value}
        super().__init__(message, details)


class FFmpegError(VideoProcessingError):
    """Raised when FFmpeg operations fail."""

    def __init__(
        self, message: str, command: str, output: Optional[str] = None
    ) -> None:
        details = (
            {"command": command, "output": output} if output else {"command": command}
        )
        super().__init__(message, details)


class ResourceNotFoundError(YouTubeProcessorError):
    """Raised when a required resource is not found."""

    def __init__(self, message: str, resource_type: str, resource_id: str) -> None:
        details = {"resource_type": resource_type, "resource_id": resource_id}
        super().__init__(message, details)


class StorageError(YouTubeProcessorError):
    """Raised when there are issues with file storage operations."""

    def __init__(self, message: str, path: str, operation: str) -> None:
        details = {"path": path, "operation": operation}
        super().__init__(message, details)


class OAuth2Error(CredentialsError):
    """Raised when OAuth2 authentication fails."""

    def __init__(
        self,
        message: str,
        error_type: Optional[str] = None,
        error_description: Optional[str] = None,
    ) -> None:
        details = {"error_type": error_type, "error_description": error_description}
        super().__init__(message, details)


# Error mapping for YouTube API errors
YOUTUBE_API_ERROR_CODES = {
    "quotaExceeded": (QuotaExceededError, "API quota exceeded"),
    "rateLimitExceeded": (RateLimitError, "Rate limit exceeded"),
    "authError": (OAuth2Error, "Authentication failed"),
    "invalidCredentials": (CredentialsError, "Invalid credentials"),
    "accessNotConfigured": (ConfigurationError, "YouTube API not enabled"),
    "notFound": (ResourceNotFoundError, "Resource not found"),
    "invalidRequest": (ValidationError, "Invalid request"),
}


def map_youtube_error(
    error_code: str, message: str, **kwargs: Any
) -> YouTubeProcessorError:
    """Map YouTube API error codes to custom exceptions."""
    error_class, default_message = YOUTUBE_API_ERROR_CODES.get(
        error_code, (YouTubeProcessorError, "Unknown error")
    )
    return error_class(message or default_message, **kwargs)

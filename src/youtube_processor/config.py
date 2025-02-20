# src/youtube_processor/config.py
import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
CONFIG_DIR = PROJECT_ROOT / "config"


class Settings(BaseSettings):
    """Application settings using Pydantic for validation."""

    # Paths Configuration
    CONFIG_DIR: Path = CONFIG_DIR
    WORK_DIR: Path = PROJECT_ROOT / "work"
    OUTPUT_DIR: Path = PROJECT_ROOT / "downloads"

    # API Credentials
    CREDENTIALS_PATH: Path = CONFIG_DIR / "client_secrets.json"
    TOKEN_PATH: Path = CONFIG_DIR / "token.json"  # Will be generated during OAuth flow

    # Processing Configuration
    MAX_CONCURRENT_DOWNLOADS: int = 3
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5  # seconds
    UPLOAD_CHUNK_SIZE: int = 1024 * 1024 * 5  # 5MB chunks for upload

    # Video Processing
    BLACK_SCREEN_DURATION: int = 2  # seconds
    VIDEO_QUALITY: str = "best"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[Path] = PROJECT_ROOT / "logs" / "youtube_processor.log"

    model_config = SettingsConfigDict(
        env_file=CONFIG_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in the environment
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_directories()
        self._validate_paths()

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [self.CONFIG_DIR, self.WORK_DIR, self.OUTPUT_DIR]

        if self.LOG_FILE:
            directories.append(self.LOG_FILE.parent)

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _validate_paths(self) -> None:
        """Validate critical paths and files."""
        # Don't validate credentials during initial setup
        if "configure" not in os.sys.argv:
            if not self.CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"YouTube API credentials not found at {self.CREDENTIALS_PATH}. "
                    "Please follow these steps:\n"
                    "1. Go to Google Cloud Console (https://console.cloud.google.com)\n"
                    "2. Create a project or select an existing one\n"
                    "3. Enable the YouTube Data API v3\n"
                    "4. Go to Credentials and create an OAuth 2.0 Client ID\n"
                    "5. Download the client secrets file\n"
                    "6. Save it as 'client_secrets.json' in the config directory\n"
                    "Then run 'youtube-processor configure' to complete setup."
                )

    @property
    def credentials_exist(self) -> bool:
        """Check if API credentials exist."""
        return self.CREDENTIALS_PATH.exists()

    @property
    def token_exists(self) -> bool:
        """Check if auth token exists."""
        return self.TOKEN_PATH.exists()


# Create global settings instance
settings = Settings()

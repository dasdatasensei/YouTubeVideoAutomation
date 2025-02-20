# src/youtube_processor/models.py
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class PrivacyStatus(str, Enum):
    """Video privacy status."""

    PRIVATE = "private"
    UNLISTED = "unlisted"
    PUBLIC = "public"


class VideoLicense(str, Enum):
    """Video license type."""

    YOUTUBE = "youtube"
    CREATIVE_COMMONS = "creativeCommons"


class VideoMetadata(BaseModel):
    """Data model for video metadata."""

    title: str
    description: str
    tags: List[str] = Field(default_factory=list)
    thumbnail_path: Optional[Path] = None
    duration: Optional[int] = None
    original_url: Optional[str] = None

    # Additional metadata
    category_id: str = "22"  # Default: People & Blogs
    privacy_status: PrivacyStatus = PrivacyStatus.PRIVATE
    made_for_kids: bool = False
    language: str = "en"
    license: VideoLicense = VideoLicense.YOUTUBE
    embeddable: bool = True
    public_stats_viewable: bool = True
    notify_subscribers: bool = True

    # Recording details
    recording_date: Optional[datetime] = None
    location: Optional[dict] = None

    # Playlists
    playlist_ids: List[str] = Field(default_factory=list)

    class Config:
        use_enum_values = True


class BatchProcessingJob(BaseModel):
    """Data model for batch processing configuration."""

    input_file: Path
    output_dir: Optional[Path] = None
    default_privacy: PrivacyStatus = PrivacyStatus.PRIVATE
    default_category: str = "22"
    scheduling_interval: int = 24  # hours between uploads

    class Config:
        use_enum_values = True

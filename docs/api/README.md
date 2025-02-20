# API Documentation

## Table of Contents
- [API Reference](#api-reference)
- [Class Documentation](#class-documentation)
- [CLI Commands](#cli-commands)

## API Reference

### Core Components

#### YouTubeProcessor
```python
class YouTubeProcessor:
    """Main class for handling YouTube video processing operations."""

    def __init__(
        self,
        client_secrets_file: str,
        work_dir: str = "work",
        output_dir: str = "downloads"
    ) -> None:
        """
        Initialize YouTube processor.

        Args:
            client_secrets_file: Path to OAuth 2.0 client secrets file
            work_dir: Directory for temporary files
            output_dir: Directory for downloaded videos
        """
        pass

    def process_video(
        self,
        url: str,
        publish_time: Optional[datetime] = None
    ) -> str:
        """
        Process a single video through the pipeline.

        Args:
            url: YouTube video URL or local file path
            publish_time: Optional scheduled publish time

        Returns:
            str: Uploaded video ID

        Raises:
            VideoProcessingError: If processing fails
            VideoUploadError: If upload fails
        """
        pass

    def batch_process(
        self,
        csv_file: str,
        continue_on_error: bool = True
    ) -> List[str]:
        """
        Process multiple videos from CSV file.

        Args:
            csv_file: Path to CSV file with video information
            continue_on_error: Whether to continue processing on errors

        Returns:
            List[str]: List of processed video IDs
        """
        pass
```

#### VideoDownloader
```python
class VideoDownloader:
    """Handle video downloading operations."""

    def download(
        self,
        url: str
    ) -> Tuple[Path, VideoMetadata]:
        """
        Download video and extract metadata.

        Args:
            url: YouTube video URL

        Returns:
            Tuple containing:
                - Path to downloaded video
                - VideoMetadata object
        """
        pass
```

#### VideoProcessor
```python
class VideoProcessor:
    """Handle video processing operations."""

    def process_video(
        self,
        input_path: Path
    ) -> Path:
        """
        Process video file.

        Args:
            input_path: Path to input video

        Returns:
            Path: Path to processed video
        """
        pass
```

### Data Models

#### VideoMetadata
```python
class VideoMetadata(BaseModel):
    """Video metadata model."""

    title: str
    description: str
    tags: List[str] = Field(default_factory=list)
    thumbnail_url: Optional[HttpUrl] = None
    duration: int
    original_url: str
```

### Exceptions
```python
class YouTubeProcessorError(Exception):
    """Base exception for all processor errors."""
    pass

class VideoDownloadError(YouTubeProcessorError):
    """Raised when video download fails."""
    pass

class VideoProcessingError(YouTubeProcessorError):
    """Raised when video processing fails."""
    pass

class VideoUploadError(YouTubeProcessorError):
    """Raised when video upload fails."""
    pass
```

## Class Documentation

### Core Classes

#### YouTubeAPI
```python
from typing import Optional
from datetime import datetime
from pathlib import Path

class YouTubeAPI:
    """
    Handles all YouTube API operations.

    This class manages authentication, video uploads,
    and other YouTube API interactions.

    Attributes:
        credentials_path (Path): Path to credentials file
        token_path (Path): Path to token file
        youtube: Authenticated YouTube API service

    Example:
        ```python
        api = YouTubeAPI()
        video_id = api.upload_video(
            video_path='video.mp4',
            metadata=metadata,
            publish_time=datetime.now()
        )
        ```
    """

    def __init__(self):
        """Initialize YouTube API client."""
        pass

    def upload_video(
        self,
        video_path: Path,
        metadata: VideoMetadata,
        publish_time: Optional[datetime] = None
    ) -> str:
        """
        Upload video to YouTube.

        Args:
            video_path: Path to video file
            metadata: Video metadata
            publish_time: Optional scheduled publish time

        Returns:
            str: YouTube video ID

        Raises:
            VideoUploadError: If upload fails
        """
        pass
```

### Utility Classes

#### ThumbnailProcessor
```python
class ThumbnailProcessor:
    """
    Process and generate video thumbnails.

    This class handles thumbnail creation, including
    text overlay and image processing operations.

    Example:
        ```python
        processor = ThumbnailProcessor()
        processor.create_thumbnail(
            image_path='input.jpg',
            output_path='thumbnail.jpg',
            text='Epic Video!'
        )
        ```
    """
    pass
```

## CLI Commands

### Basic Commands

#### Process Single Video
```bash
# Process YouTube video
youtube-processor process VIDEO_URL [OPTIONS]

Options:
  --publish-time TEXT  Scheduled publish time
  --private           Upload as private (default)
  --public            Upload as public
  --help             Show help message

Example:
  youtube-processor process https://youtu.be/xxx \
      --publish-time "2024-02-20T15:00:00"
```

#### Batch Processing
```bash
# Process multiple videos
youtube-processor batch CSV_FILE [OPTIONS]

Options:
  --continue-on-error  Continue processing if a video fails
  --help              Show help message

Example:
  youtube-processor batch videos.csv --continue-on-error
```

### Configuration Commands

#### Setup
```bash
# Initial setup and configuration
youtube-processor configure [OPTIONS]

Options:
  --credentials-path PATH  Path to client secrets file
  --help                  Show help message

Example:
  youtube-processor configure --credentials-path config/client_secrets.json
```

#### Verify Setup
```bash
# Verify configuration and credentials
youtube-processor verify [OPTIONS]

Options:
  --check-credentials  Verify API credentials
  --check-ffmpeg      Verify FFmpeg installation
  --help              Show help message

Example:
  youtube-processor verify --check-credentials --check-ffmpeg
```

### Utility Commands

#### Clean
```bash
# Clean working directories
youtube-processor clean [OPTIONS]

Options:
  --all               Remove all temporary files
  --older-than DAYS   Remove files older than specified days
  --help             Show help message

Example:
  youtube-processor clean --older-than 7
```

#### Status
```bash
# Check processing status
youtube-processor status [OPTIONS]

Options:
  --video-id TEXT    Check specific video status
  --all             Check all recent uploads
  --help            Show help message

Example:
  youtube-processor status --video-id xxx
```

### Environment Variables

```bash
# Configuration
YOUTUBE_CLIENT_SECRETS_FILE=config/client_secrets.json
YOUTUBE_WORK_DIR=work
YOUTUBE_OUTPUT_DIR=downloads

# Processing
YOUTUBE_MAX_RETRIES=3
YOUTUBE_RETRY_DELAY=5
YOUTUBE_MAX_CONCURRENT=3

# Logging
YOUTUBE_LOG_LEVEL=INFO
YOUTUBE_LOG_FILE=youtube_processor.log
```

## Additional Resources

### Code Examples
- [Basic Usage Examples](examples/basic.md)
- [Advanced Usage Examples](examples/advanced.md)
- [Integration Examples](examples/integration.md)

### Reference
- [Error Codes](reference/errors.md)
- [Configuration Options](reference/config.md)
- [Best Practices](reference/best_practices.md)

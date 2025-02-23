#!/usr/bin/env python3
"""
YouTube Video Automation - Main Module
Author: Dr. Jody-Ann S. Jones
Website: www.thedatasensei.com
Year: 2025
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer

from src.youtube_processor.core.downloader import VideoDownloader
from src.youtube_processor.core.processor import VideoProcessor
from src.youtube_processor.core.youtube_api import YouTubeAPI
from src.youtube_processor.logging_config import setup_logging
from src.youtube_processor.models import VideoMetadata

# Initialize logger
setup_logging()
logger = logging.getLogger(__name__)


def process_video(
    input_path: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    publish_time: Optional[str] = None,
    is_youtube_url: bool = False,
) -> Optional[str]:
    """
    Main pipeline for video processing and uploading.

    Args:
        input_path: Path to local video or YouTube URL
        title: Video title (optional)
        description: Video description (optional)
        tags: List of video tags (optional)
        publish_time: Scheduled publish time in ISO format (optional)
        is_youtube_url: Whether the input is a YouTube URL

    Returns:
        Optional[str]: Path to the processed video file if successful, None otherwise
    """
    processed_file_path = None
    try:
        # Initialize components
        downloader = VideoDownloader()
        processor = VideoProcessor()
        youtube_api = YouTubeAPI()

        # Download video if it's a YouTube URL
        if is_youtube_url:
            logger.info("Downloading video from YouTube...")
            video_path, metadata = downloader.download(input_path)
            input_path = str(video_path)
            # Use metadata if no title provided
            if not title:
                title = metadata.title
            if not description:
                description = metadata.description
            if not tags:
                tags = metadata.tags

        # Process video
        logger.info("Processing video...")
        processed_file_path = processor.process_video(Path(input_path))

        # Upload to YouTube
        logger.info("Uploading to YouTube...")
        video_id = youtube_api.upload_video(
            Path(processed_file_path),
            VideoMetadata(
                title=title or Path(input_path).stem,
                description=description or "",
                tags=tags or [],
            ),
            datetime.fromisoformat(publish_time) if publish_time else None,
        )

        logger.info("Successfully uploaded video with ID: %s", video_id)
        return str(processed_file_path)

    except Exception as e:
        logger.error("Error during video processing: %s", str(e))
        raise

    finally:
        # Cleanup temporary files
        try:
            if processed_file_path and Path(processed_file_path).exists():
                Path(processed_file_path).unlink()
                logger.debug("Cleaned up processed file")
        except Exception as e:
            logger.warning("Error during cleanup: %s", e)


def verify_auth() -> bool:
    """
    Verify authentication with YouTube API.

    Returns:
        bool: True if authentication is valid, False otherwise
    """
    try:
        api = YouTubeAPI()
        return api.check_auth()
    except Exception as e:
        logger.error("Authentication verification failed: %s", e)
        return False


def main() -> None:
    """Main entry point for the CLI application."""
    app = typer.Typer()
    app()


if __name__ == "__main__":
    main()

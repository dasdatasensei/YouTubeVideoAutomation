#!/usr/bin/env python3
"""Test script to verify core functionality of YouTube Video Automation."""

import logging
from pathlib import Path

from src.youtube_processor.core.downloader import VideoDownloader
from src.youtube_processor.core.processor import VideoProcessor
from src.youtube_processor.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def test_download_and_process():
    """Test downloading and processing a video."""
    try:
        # Initialize components
        downloader = VideoDownloader()
        processor = VideoProcessor()

        # Use a short, public domain video for testing
        test_url = "https://www.youtube.com/watch?v=EngW7tLk6R8"

        logger.info("Starting download test...")
        video_path, metadata = downloader.download(test_url)
        logger.info(f"Download successful: {video_path}")

        logger.info("Starting video processing test...")
        processed_path = processor.process_video(video_path)
        logger.info(f"Processing successful: {processed_path}")

        # Verify files exist
        assert video_path.exists(), "Downloaded video file not found"
        assert processed_path.exists(), "Processed video file not found"

        # Clean up
        video_path.unlink(missing_ok=True)
        processed_path.unlink(missing_ok=True)
        logger.info("Test completed successfully!")

        return True

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_download_and_process()
    print("✅ All tests passed!" if success else "❌ Test failed!")

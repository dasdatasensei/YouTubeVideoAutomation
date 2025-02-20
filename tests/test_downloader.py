# tests/test_downloader.py
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from youtube_processor.core.downloader import VideoDownloader
from youtube_processor.exceptions import VideoDownloadError


def test_downloader_initialization(test_settings):
    """Test VideoDownloader initialization."""
    downloader = VideoDownloader()
    assert Path(test_settings.OUTPUT_DIR).exists()


@pytest.mark.vcr
def test_download_video(test_settings):
    """Test video download with VCR.py cassette."""
    downloader = VideoDownloader()
    url = "https://www.youtube.com/watch?v=test_video"

    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        # Mock the video info
        mock_info = {
            "id": "test_video",
            "ext": "mp4",
            "title": "Test Video",
            "description": "Test Description",
            "duration": 100,
            "thumbnail": "https://example.com/thumb.jpg",
        }
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
            mock_info
        )

        # Test download
        video_path, metadata = downloader.download(url)

        assert video_path.exists()
        assert metadata.title == "Test Video"
        assert metadata.duration == 100


def test_download_error(test_settings):
    """Test download error handling."""
    downloader = VideoDownloader()
    url = "https://www.youtube.com/watch?v=invalid"

    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = (
            Exception("Download failed")
        )

        with pytest.raises(VideoDownloadError):
            downloader.download(url)

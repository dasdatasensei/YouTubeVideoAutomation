# tests/test_processor.py
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from youtube_processor.core.processor import VideoProcessor
from youtube_processor.exceptions import VideoProcessingError


def test_processor_initialization(test_settings):
    """Test VideoProcessor initialization."""
    processor = VideoProcessor()
    assert Path(test_settings.WORK_DIR).exists()


def test_process_video(test_settings, tmp_path):
    """Test video processing."""
    processor = VideoProcessor()

    # Create dummy input video
    input_path = tmp_path / "input.mp4"
    input_path.touch()

    # Mock ffmpeg probe result
    probe_result = {
        "streams": [
            {
                "codec_type": "video",
                "width": 1920,
                "height": 1080,
                "r_frame_rate": "30/1",
            }
        ]
    }

    with patch("ffmpeg.probe") as mock_probe, patch("ffmpeg.input") as mock_input:
        mock_probe.return_value = probe_result
        mock_input.return_value = MagicMock()

        output_path = processor.process_video(input_path)
        assert output_path.exists()

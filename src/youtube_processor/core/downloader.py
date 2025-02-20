# src/youtube_processor/core/downloader.py
import logging
from pathlib import Path
from typing import Tuple

import yt_dlp

from ..config import settings
from ..exceptions import VideoDownloadError
from ..models import VideoMetadata

logger = logging.getLogger(__name__)


class VideoDownloader:
    """Handles video downloading using yt-dlp."""

    def __init__(self) -> None:
        self.output_path = Path(settings.OUTPUT_DIR)
        self._ensure_output_directory()

    def _ensure_output_directory(self) -> None:
        """Ensure output directory exists."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory ready: {self.output_path}")

    def download(self, url: str) -> Tuple[Path, VideoMetadata]:
        """
        Download video and extract metadata.

        Args:
            url: YouTube video URL

        Returns:
            Tuple containing:
                - Path to downloaded video
                - VideoMetadata object with video information

        Raises:
            VideoDownloadError: If download fails
        """
        ydl_opts = {
            "format": settings.VIDEO_QUALITY,
            "outtmpl": str(self.output_path / "%(id)s.%(ext)s"),
            "writethumbnail": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Starting download: {url}")
                info = ydl.extract_info(url, download=True)

                video_path = self.output_path / f"{info['id']}.{info['ext']}"

                metadata = VideoMetadata(
                    title=info["title"],
                    description=info["description"],
                    tags=info.get("tags", []),
                    thumbnail_url=info.get("thumbnail", ""),
                    duration=info["duration"],
                    original_url=url,
                )

                logger.info(f"Download complete: {video_path}")
                return video_path, metadata

        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise VideoDownloadError(f"Failed to download {url}: {str(e)}")

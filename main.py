#!/usr/bin/env python3
"""
YouTube Video Automation - Main Entry Point
Author: Dr. Jody-Ann S. Jones
Website: www.thedatasensei.com
Year: 2025
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

from src.youtube_processor.core.downloader import VideoDownloader
from src.youtube_processor.core.processor import VideoProcessor
from src.youtube_processor.core.youtube_api import YouTubeAPI
from src.youtube_processor.logging_config import setup_logging
from src.youtube_processor.models import VideoMetadata

# Initialize Rich console and logging
console = Console()
setup_logging()
logger = logging.getLogger(__name__)


def process_video(
    input_path: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    publish_time: Optional[str] = None,
    is_youtube_url: bool = False,
) -> None:
    """
    Main pipeline for video processing and uploading.

    Args:
        input_path: Path to local video or YouTube URL
        title: Video title (optional)
        description: Video description (optional)
        tags: List of video tags (optional)
        publish_time: Scheduled publish time in ISO format (optional)
        is_youtube_url: Whether the input is a YouTube URL
    """
    try:
        # Initialize components
        downloader = VideoDownloader()
        processor = VideoProcessor()
        youtube_api = YouTubeAPI()

        with console.status("[bold green]Processing video...") as status:
            # Download if YouTube URL
            if is_youtube_url:
                status.update("[bold yellow]Downloading video...")
                video_path, metadata = downloader.download(input_path)
                # Use downloaded metadata if not provided
                title = title or metadata.title
                description = description or metadata.description
                tags = tags or metadata.tags
            else:
                video_path = Path(input_path)
                if not video_path.exists():
                    raise FileNotFoundError(f"Video file not found: {input_path}")

            # Process video
            status.update("[bold yellow]Processing video...")
            processed_path = processor.process_video(video_path)

            # Prepare metadata
            metadata = VideoMetadata(
                title=title or video_path.stem,
                description=description or "",
                tags=tags or [],
                thumbnail_url=None,
                duration=0,
                original_url=str(video_path),
            )

            # Upload to YouTube
            status.update("[bold yellow]Uploading to YouTube...")
            video_id = youtube_api.upload_video(processed_path, metadata, publish_time)

            # Cleanup
            if is_youtube_url:
                video_path.unlink(missing_ok=True)
            processed_path.unlink(missing_ok=True)

            console.print(f"\n✅ [bold green]Success![/] Video ID: {video_id}")
            if publish_time:
                console.print(f"📅 Scheduled for: {publish_time}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        console.print(f"\n❌ [bold red]Error:[/] {str(e)}")
        sys.exit(1)


def main():
    """Main entry point with command line interface."""
    app = typer.Typer(help="YouTube Video Automation Pipeline")

    @app.command()
    def local(
        video_path: str = typer.Argument(..., help="Path to local video file"),
        title: str = typer.Option(None, help="Video title"),
        description: str = typer.Option(None, help="Video description"),
        tags: str = typer.Option(None, help="Comma-separated tags"),
        publish_time: str = typer.Option(None, help="Publish time (ISO format)"),
    ):
        """Process and upload a local video file."""
        tag_list = tags.split(",") if tags else None
        process_video(video_path, title, description, tag_list, publish_time)

    @app.command()
    def youtube(
        url: str = typer.Argument(..., help="YouTube video URL"),
        title: str = typer.Option(None, help="Override video title"),
        description: str = typer.Option(None, help="Override video description"),
        tags: str = typer.Option(None, help="Override comma-separated tags"),
        publish_time: str = typer.Option(None, help="Publish time (ISO format)"),
    ):
        """Download, process, and reupload a YouTube video."""
        tag_list = tags.split(",") if tags else None
        process_video(
            url, title, description, tag_list, publish_time, is_youtube_url=True
        )

    app()

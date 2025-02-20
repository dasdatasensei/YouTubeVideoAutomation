# src/youtube_processor/cli.py
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.traceback import install

from .config import settings
from .core.downloader import VideoDownloader
from .core.processor import VideoProcessor
from .core.youtube_api import YouTubeAPI
from .exceptions import OAuth2Error, YouTubeProcessorError
from .logging_config import setup_logging
from .models import VideoMetadata

# Initialize Typer app and Rich console
app = typer.Typer(help="YouTube Video Processing CLI")
console = Console()
install()  # Install rich traceback handler

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@app.command()
def process_local(
    file_path: Path = typer.Argument(
        ...,
        help="Path to local video file",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    title: str = typer.Option(
        None, help="Video title. If not provided, uses filename."
    ),
    description: str = typer.Option("", help="Video description"),
    tags: list[str] = typer.Option([], help="Video tags (comma-separated)"),
    publish_time: Optional[datetime] = typer.Option(
        None, help="Scheduled publish time (ISO format)", formats=["%Y-%m-%dT%H:%M:%S"]
    ),
):
    """Process a local video file and upload it to YouTube."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Initialize components
            progress.add_task("Initializing YouTube API...", total=None)
            youtube_api = YouTubeAPI()
            processor = VideoProcessor()

            # Create metadata
            metadata = VideoMetadata(
                title=title or file_path.stem,
                description=description,
                tags=tags,
                thumbnail_url=None,
                duration=0,  # Will be updated after processing
                original_url=str(file_path),
            )

            # Process video
            progress.add_task("Processing video...", total=None)
            processed_path = processor.process_video(file_path)

            # Upload video
            progress.add_task("Uploading to YouTube...", total=None)
            video_id = youtube_api.upload_video(processed_path, metadata, publish_time)

            # Cleanup
            processed_path.unlink(missing_ok=True)

            console.print(
                f"✅ Video processed and uploaded successfully! ID: {video_id}"
            )
            if publish_time:
                console.print(f"📅 Scheduled for publication at: {publish_time}")
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        console.print(f"❌ Processing failed: {str(e)}", style="bold red")
        raise typer.Exit(code=1)


@app.command()
def process_youtube(
    url: str = typer.Argument(..., help="YouTube video URL to process"),
    publish_time: Optional[datetime] = typer.Option(
        None, help="Scheduled publish time (ISO format)", formats=["%Y-%m-%dT%H:%M:%S"]
    ),
):
    """Process an existing YouTube video: download, modify, and re-upload."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Initialize components
            progress.add_task("Initializing YouTube API...", total=None)
            youtube_api = YouTubeAPI()
            downloader = VideoDownloader()
            processor = VideoProcessor()

            # Download video
            progress.add_task("Downloading video...", total=None)
            video_path, metadata = downloader.download(url)

            # Process video
            progress.add_task("Processing video...", total=None)
            processed_path = processor.process_video(video_path)

            # Upload video
            progress.add_task("Uploading to YouTube...", total=None)
            video_id = youtube_api.upload_video(processed_path, metadata, publish_time)

            # Cleanup
            video_path.unlink(missing_ok=True)
            processed_path.unlink(missing_ok=True)

            console.print(
                f"✅ Video processed and uploaded successfully! ID: {video_id}"
            )
            if publish_time:
                console.print(f"📅 Scheduled for publication at: {publish_time}")
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        console.print(f"❌ Processing failed: {str(e)}", style="bold red")
        raise typer.Exit(code=1)


@app.command()
def batch_process(
    input_csv: Path = typer.Argument(
        ..., help="CSV file containing video information", exists=True
    )
):
    """Process multiple videos from a CSV file."""
    import csv
    from datetime import datetime

    try:
        with open(input_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Handle both local and YouTube videos
                if "file_path" in row:
                    process_local(
                        Path(row["file_path"]),
                        title=row.get("title"),
                        description=row.get("description", ""),
                        tags=row.get("tags", "").split(","),
                        publish_time=(
                            datetime.fromisoformat(row["publish_time"])
                            if "publish_time" in row
                            else None
                        ),
                    )
                elif "url" in row:
                    process_youtube(
                        row["url"],
                        publish_time=(
                            datetime.fromisoformat(row["publish_time"])
                            if "publish_time" in row
                            else None
                        ),
                    )

    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        console.print(f"❌ Batch processing failed: {str(e)}", style="bold red")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

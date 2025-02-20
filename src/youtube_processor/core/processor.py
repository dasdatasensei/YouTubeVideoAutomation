# src/youtube_processor/core/processor.py
import logging
from pathlib import Path

import ffmpeg

from ..config import settings
from ..exceptions import VideoProcessingError

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handles video processing using FFmpeg."""

    def __init__(self) -> None:
        self.work_dir = Path(settings.WORK_DIR)
        self._ensure_work_directory()

    def _ensure_work_directory(self) -> None:
        """Ensure work directory exists."""
        self.work_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Work directory ready: {self.work_dir}")

    def _run_ffmpeg_command(self, stream, output_path: Path, desc: str) -> None:
        """Run FFmpeg command with error handling."""
        try:
            # Get the ffmpeg command for logging
            cmd = ffmpeg.get_args(stream)
            logger.debug(f"Running FFmpeg command: {' '.join(cmd)}")

            # Run the command
            out, err = stream.run(capture_stdout=True, capture_stderr=True)

            if err:
                logger.debug(f"FFmpeg output: {err.decode()}")

        except ffmpeg.Error as e:
            logger.error(f"FFmpeg {desc} failed:")
            logger.error(f"FFmpeg stdout: {e.stdout.decode() if e.stdout else ''}")
            logger.error(f"FFmpeg stderr: {e.stderr.decode() if e.stderr else ''}")
            raise

    def process_video(self, input_path: Path) -> Path:
        """
        Add black screen to video end.

        Args:
            input_path: Path to input video file

        Returns:
            Path to processed video file

        Raises:
            VideoProcessingError: If processing fails
        """
        try:
            logger.info(f"Starting video processing for: {input_path}")

            # Verify input file exists
            if not input_path.exists():
                raise VideoProcessingError(
                    message=f"Input file does not exist", file_path=str(input_path)
                )

            # Get video information
            try:
                probe = ffmpeg.probe(str(input_path))
                logger.debug(f"Video probe result: {probe}")

                video_info = next(
                    s for s in probe["streams"] if s["codec_type"] == "video"
                )

                width = int(video_info["width"])
                height = int(video_info["height"])
                fps = eval(video_info["r_frame_rate"])

                logger.info(f"Video specs: {width}x{height} @ {fps}fps")

            except ffmpeg.Error as e:
                logger.error(f"FFmpeg probe failed: {e.stderr.decode()}")
                raise VideoProcessingError(
                    message=f"Failed to probe video: {e.stderr.decode()}",
                    file_path=str(input_path),
                )

            # Generate black screen
            black_screen_path = self.work_dir / "black_screen.mp4"
            logger.info("Generating black screen clip")

            black_screen = (
                ffmpeg.input(f"color=c=black:s={width}x{height}:r={fps}", f="lavfi")
                .output(str(black_screen_path), t=settings.BLACK_SCREEN_DURATION)
                .overwrite_output()
            )

            self._run_ffmpeg_command(
                black_screen, black_screen_path, "black screen generation"
            )

            # Prepare output path
            output_path = self.work_dir / f"processed_{input_path.name}"

            # Create concat file
            concat_list = self.work_dir / "concat_list.txt"
            with open(concat_list, "w") as f:
                f.write(f"file '{input_path.absolute()}'\n")
                f.write(f"file '{black_screen_path.absolute()}'\n")

            logger.info(f"Created concat list at: {concat_list}")

            # Concatenate videos
            logger.info("Concatenating videos")
            concat = (
                ffmpeg.input(str(concat_list), f="concat", safe=0)
                .output(str(output_path), c="copy")
                .overwrite_output()
            )

            self._run_ffmpeg_command(concat, output_path, "video concatenation")

            if not output_path.exists():
                raise VideoProcessingError(
                    message="Output file was not created", file_path=str(output_path)
                )

            logger.info(f"Processing complete: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise VideoProcessingError(
                message=f"Failed to process video: {str(e)}", file_path=str(input_path)
            )

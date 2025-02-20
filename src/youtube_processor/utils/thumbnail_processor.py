# src/youtube_processor/utils/thumbnail_processor.py
import logging
import textwrap
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class ThumbnailProcessor:
    """Utility for processing video thumbnails."""

    YOUTUBE_THUMBNAIL_SIZE = (1280, 720)  # 16:9 aspect ratio
    DEFAULT_FONT_SIZE = 72

    def __init__(self, fonts_dir: Optional[Path] = None):
        """Initialize thumbnail processor."""
        self.fonts_dir = fonts_dir or Path(__file__).parent / "fonts"

    def process_thumbnail(
        self,
        image_path: Path,
        output_path: Optional[Path] = None,
        text: Optional[str] = None,
        resize: bool = True,
    ) -> Path:
        """
        Process an image to be used as a YouTube thumbnail.

        Args:
            image_path: Path to input image
            output_path: Path for processed thumbnail (optional)
            text: Text to overlay on thumbnail (optional)
            resize: Whether to resize to YouTube dimensions

        Returns:
            Path to processed thumbnail
        """
        try:
            # Open and convert image to RGB
            with Image.open(image_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Resize if needed
                if resize:
                    img = self._resize_image(img)

                # Add text if provided
                if text:
                    img = self._add_text(img, text)

                # Determine output path
                if not output_path:
                    output_path = (
                        image_path.parent
                        / f"{image_path.stem}_thumb{image_path.suffix}"
                    )

                # Save processed thumbnail
                img.save(output_path, quality=95, optimize=True)
                logger.info(f"Thumbnail processed and saved to: {output_path}")

                return output_path

        except Exception as e:
            logger.error(f"Failed to process thumbnail: {str(e)}")
            raise

    def _resize_image(self, img: Image.Image) -> Image.Image:
        """Resize image to YouTube thumbnail dimensions."""
        # Calculate aspect ratios
        target_ratio = self.YOUTUBE_THUMBNAIL_SIZE[0] / self.YOUTUBE_THUMBNAIL_SIZE[1]
        img_ratio = img.width / img.height

        if img_ratio > target_ratio:
            # Image is wider than 16:9
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            # Image is taller than 16:9
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))

        # Resize to final dimensions
        return img.resize(self.YOUTUBE_THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

    def _add_text(
        self,
        img: Image.Image,
        text: str,
        position: Tuple[float, float] = (0.5, 0.8),  # Center, bottom
    ) -> Image.Image:
        """Add text overlay to image."""
        draw = ImageDraw.Draw(img)

        # Try to load font, fall back to default
        try:
            font = ImageFont.truetype(
                str(self.fonts_dir / "OpenSans-Bold.ttf"), self.DEFAULT_FONT_SIZE
            )
        except Exception:
            font = ImageFont.load_default()

        # Wrap text
        max_width = int(img.width * 0.9)  # 90% of image width
        avg_char_width = (
            sum(font.getsize(c)[0] for c in "abcdefghijklmnopqrstuvwxyz") / 26
        )
        max_chars = int(max_width / avg_char_width)
        lines = textwrap.wrap(text, width=max_chars)

        # Calculate text size and position
        line_height = font.getsize("hg")[1] * 1.5
        total_height = line_height * len(lines)
        x = img.width * position[0]
        y = img.height * position[1] - total_height

        # Add text shadow/outline for better visibility
        shadow_offset = 3
        shadow_color = "black"

        for line in lines:
            w, h = draw.textsize(line, font=font)
            x_centered = x - w / 2

            # Draw shadow/outline
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                draw.text(
                    (x_centered + dx * shadow_offset, y + dy * shadow_offset),
                    line,
                    font=font,
                    fill=shadow_color,
                )

            # Draw main text
            draw.text((x_centered, y), line, font=font, fill="white")
            y += line_height

        return img


# Example usage
if __name__ == "__main__":
    processor = ThumbnailProcessor()
    processor.process_thumbnail(
        Path("input.jpg"), text="Epic Gaming Moment!", output_path=Path("output.jpg")
    )

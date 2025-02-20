# tests/conftest.py
from pathlib import Path

import pytest

from youtube_processor.config import Settings


@pytest.fixture
def test_settings():
    """Provide test settings."""
    return Settings(
        WORK_DIR="test_work",
        OUTPUT_DIR="test_downloads",
        MAX_CONCURRENT_DOWNLOADS=1,
        MAX_RETRIES=1,
    )


@pytest.fixture(autouse=True)
def setup_test_dirs(test_settings):
    """Create and clean up test directories."""
    # Setup
    Path(test_settings.WORK_DIR).mkdir(parents=True, exist_ok=True)
    Path(test_settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    yield

    # Cleanup
    for path in [test_settings.WORK_DIR, test_settings.OUTPUT_DIR]:
        if Path(path).exists():
            for file in Path(path).glob("*"):
                file.unlink()
            Path(path).rmdir()

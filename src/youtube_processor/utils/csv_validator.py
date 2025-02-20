# src/youtube_processor/utils/csv_validator.py
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from ..exceptions import ValidationError
from ..models import PrivacyStatus, VideoLicense

logger = logging.getLogger(__name__)


class CSVValidator:
    """Validator for batch processing CSV files."""

    REQUIRED_COLUMNS = ["file_path", "title"]
    OPTIONAL_COLUMNS = [
        "description",
        "tags",
        "category",
        "privacy_status",
        "made_for_kids",
        "thumbnail_path",
        "publish_time",
        "language",
        "license",
        "embeddable",
        "public_stats",
        "notify_subscribers",
    ]

    VALID_CATEGORIES = [
        "1",
        "2",
        "10",
        "15",
        "17",
        "19",
        "20",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
    ]

    def __init__(self, csv_path: Path):
        """Initialize validator with CSV file path."""
        self.csv_path = csv_path

    def validate(self) -> List[Dict[str, Any]]:
        """
        Validate CSV file and return processed data.

        Returns:
            List of validated row dictionaries

        Raises:
            ValidationError: If validation fails
        """
        try:
            # Read CSV using pandas for better error handling
            df = pd.read_csv(self.csv_path)

            # Check required columns
            missing_columns = [
                col for col in self.REQUIRED_COLUMNS if col not in df.columns
            ]
            if missing_columns:
                raise ValidationError(
                    f"Missing required columns: {', '.join(missing_columns)}"
                )

            # Process each row
            validated_rows = []
            for index, row in df.iterrows():
                try:
                    validated_row = self._validate_row(row.to_dict(), index + 2)
                    validated_rows.append(validated_row)
                except Exception as e:
                    logger.error(f"Error in row {index + 2}: {str(e)}")
                    raise ValidationError(f"Row {index + 2}: {str(e)}")

            return validated_rows

        except Exception as e:
            logger.error(f"CSV validation failed: {str(e)}")
            raise ValidationError(f"CSV validation failed: {str(e)}")

    def _validate_row(self, row: Dict[str, Any], row_num: int) -> Dict[str, Any]:
        """Validate and process a single row."""
        validated = {}

        # Validate file_path or URL
        if "file_path" in row and row["file_path"]:
            path = Path(row["file_path"])
            if not path.is_file() and not path.as_posix().startswith("http"):
                raise ValidationError(f"File not found: {path}")
            validated["file_path"] = str(path)

        # Validate title
        if not row.get("title"):
            raise ValidationError("Title is required")
        validated["title"] = row["title"]

        # Validate description
        validated["description"] = row.get("description", "")

        # Validate tags
        if "tags" in row and row["tags"]:
            tags = [tag.strip() for tag in str(row["tags"]).split(",")]
            validated["tags"] = tags

        # Validate category
        if "category" in row:
            category = str(row["category"])
            if category not in self.VALID_CATEGORIES:
                raise ValidationError(f"Invalid category ID: {category}")
            validated["category"] = category

        # Validate privacy status
        if "privacy_status" in row:
            try:
                status = PrivacyStatus(row["privacy_status"].lower())
                validated["privacy_status"] = status.value
            except ValueError:
                raise ValidationError(
                    f"Invalid privacy status: {row['privacy_status']}"
                )

        # Validate publish time
        if "publish_time" in row and row["publish_time"]:
            try:
                publish_time = datetime.fromisoformat(row["publish_time"])
                validated["publish_time"] = publish_time
            except ValueError:
                raise ValidationError(
                    f"Invalid publish time format: {row['publish_time']}"
                )

        # Validate thumbnail path
        if "thumbnail_path" in row and row["thumbnail_path"]:
            thumb_path = Path(row["thumbnail_path"])
            if not thumb_path.is_file():
                raise ValidationError(f"Thumbnail not found: {thumb_path}")
            validated["thumbnail_path"] = str(thumb_path)

        # Validate boolean fields
        for field in [
            "made_for_kids",
            "embeddable",
            "public_stats",
            "notify_subscribers",
        ]:
            if field in row:
                validated[field] = str(row[field]).lower() == "true"

        # Validate license
        if "license" in row:
            try:
                license = VideoLicense(row["license"].lower())
                validated["license"] = license.value
            except ValueError:
                raise ValidationError(f"Invalid license: {row['license']}")

        return validated

    @classmethod
    def generate_template(cls, output_path: Path) -> None:
        """Generate a template CSV file."""
        headers = cls.REQUIRED_COLUMNS + cls.OPTIONAL_COLUMNS
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            # Add example row
            writer.writerow(
                [
                    "path/to/video.mp4",  # file_path
                    "Video Title",  # title
                    "Description here",  # description
                    "tag1,tag2,tag3",  # tags
                    "22",  # category
                    "private",  # privacy_status
                    "false",  # made_for_kids
                    "path/to/thumb.jpg",  # thumbnail_path
                    "2024-02-20T15:00:00",  # publish_time
                    "en",  # language
                    "youtube",  # license
                    "true",  # embeddable
                    "true",  # public_stats
                    "true",  # notify_subscribers
                ]
            )


# Example usage
if __name__ == "__main__":
    validator = CSVValidator(Path("batch_upload.csv"))
    try:
        validated_data = validator.validate()
        print(f"Validated: {len(validated_data)}")
    except Exception as e:
        logger.error(f"CSV validation failed: {str(e)}")
        raise ValidationError(f"CSV validation failed: {str(e)}")
    else:
        print(f"Validated: {len(validated_data)}")

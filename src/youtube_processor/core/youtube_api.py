# src/youtube_processor/core/youtube_api.py
import json
import logging
import socket
from datetime import datetime
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from ..config import settings
from ..exceptions import OAuth2Error, VideoUploadError
from ..models import VideoMetadata

logger = logging.getLogger(__name__)


class YouTubeAPI:
    """Handles all YouTube API operations."""

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl",
    ]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self) -> None:
        """Initialize YouTube API client."""
        self.credentials_path = settings.CREDENTIALS_PATH
        self.token_path = settings.TOKEN_PATH

        # Enable OAuth2.0 debug logging
        logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)
        logging.getLogger("googleapiclient.discovery").setLevel(logging.DEBUG)
        logging.getLogger("google_auth_oauthlib.flow").setLevel(logging.DEBUG)

        try:
            self.youtube = self._get_authenticated_service()
            logger.info("YouTube API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube API client: {str(e)}")
            raise OAuth2Error(f"YouTube API initialization failed: {str(e)}")

    def _find_available_port(self) -> int:
        """Find an available port for the OAuth callback server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

    def _get_authenticated_service(self):
        """Get authenticated YouTube API service."""
        credentials = None

        # Load existing token if available
        if self.token_path.exists():
            try:
                logger.debug(f"Loading existing token from {self.token_path}")
                with open(self.token_path, "r") as token:
                    token_data = token.read()
                    logger.debug(f"Token data: {token_data}")
                    credentials = Credentials.from_authorized_user_json(
                        token_data, self.SCOPES
                    )
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding token file: {str(e)}")
                self.token_path.unlink(missing_ok=True)  # Delete invalid token
            except Exception as e:
                logger.error(f"Error loading token: {str(e)}")
                self.token_path.unlink(missing_ok=True)  # Delete invalid token

        # If no valid credentials available, get new ones
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                logger.info("Refreshing expired token")
                try:
                    credentials.refresh(Request())
                except Exception as e:
                    logger.error(f"Token refresh failed: {str(e)}")
                    credentials = None

            if not credentials:
                logger.info("Getting new credentials")
                try:
                    # Find an available port
                    port = self._find_available_port()
                    redirect_uri = f"http://localhost:{port}"
                    logger.info(f"Using redirect URI: {redirect_uri}")

                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES, redirect_uri=redirect_uri
                    )
                    credentials = flow.run_local_server(
                        port=port, access_type="offline", include_granted_scopes="true"
                    )

                    # Save the credentials for future use
                    with open(self.token_path, "w") as token:
                        token.write(credentials.to_json())
                    logger.info(f"New credentials saved to {self.token_path}")
                except Exception as e:
                    logger.error(f"Failed to get new credentials: {str(e)}")
                    raise OAuth2Error(
                        f"Authentication failed: {str(e)}. "
                        f"Please ensure {redirect_uri} is added to the authorized "
                        "redirect URIs in your Google Cloud Console."
                    )

        try:
            return build(
                self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials
            )
        except Exception as e:
            logger.error(f"Failed to build YouTube service: {str(e)}")
            raise OAuth2Error(f"YouTube API service creation failed: {str(e)}")

    def upload_video(
        self,
        video_path: Path,
        metadata: VideoMetadata,
        publish_time: Optional[datetime] = None,
    ) -> str:
        """
        Upload video to YouTube with scheduling.

        Args:
            video_path: Path to video file
            metadata: Video metadata
            publish_time: Optional scheduled publish time

        Returns:
            YouTube video ID

        Raises:
            VideoUploadError: If upload fails
        """
        try:
            body = {
                "snippet": {
                    "title": metadata.title,
                    "description": metadata.description,
                    "tags": metadata.tags,
                    "categoryId": "22",  # People & Blogs category
                },
                "status": {
                    "privacyStatus": "private",
                    "publishAt": (
                        publish_time.isoformat() + "Z" if publish_time else None
                    ),
                    "selfDeclaredMadeForKids": False,
                },
            }

            # Create upload request
            insert_request = self.youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=MediaFileUpload(
                    str(video_path),
                    chunksize=settings.UPLOAD_CHUNK_SIZE,
                    resumable=True,
                ),
            )

            # Execute upload with progress monitoring
            response = None
            while response is None:
                try:
                    _, response = insert_request.next_chunk()
                    if response:
                        logger.info("Upload completed successfully")
                        return response["id"]
                except Exception as e:
                    logger.error(f"Upload chunk failed: {str(e)}")
                    raise VideoUploadError(f"Upload failed: {str(e)}")

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            raise VideoUploadError(f"Failed to upload video: {str(e)}")

    def set_thumbnail(self, video_id: str, thumbnail_path: Path) -> None:
        """Set video thumbnail."""
        try:
            self.youtube.thumbnails().set(
                videoId=video_id, media_body=MediaFileUpload(str(thumbnail_path))
            ).execute()
            logger.info(f"Thumbnail set for video {video_id}")
        except Exception as e:
            logger.error(f"Failed to set thumbnail: {str(e)}")
            # Non-critical error, don't raise exception

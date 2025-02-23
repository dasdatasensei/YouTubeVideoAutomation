#!/usr/bin/env python3
"""
YouTube Video Automation - Streamlit Frontend
Author: Dr. Jody-Ann S. Jones
Website: www.thedatasensei.com
Year: 2025
"""

import datetime
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import streamlit as st
from rich.logging import RichHandler

from main import process_video
from src.youtube_processor.logging_config import setup_logging
from src.youtube_processor.models import BatchProcessingJob

# Configure page
st.set_page_config(
    page_title="YouTube Video Automation",
    page_icon="🎥",
    layout="wide",
)

# Custom CSS
st.markdown(
    """
<style>
    /* Main font sizes */
    .stMarkdown, .stText {
        font-size: 20px !important;
    }

    /* Headers */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }
    h2 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
    }

    /* Form labels and inputs */
    .stTextInput label, .stTextArea label, .stDateInput label, .stTimeInput label {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }
    .stTextInput input, .stTextArea textarea {
        font-size: 1.2rem !important;
    }

    /* Buttons */
    .stButton button {
        font-size: 1.2rem !important;
        padding: 0.75rem 1.5rem !important;
    }

    /* File uploader */
    .stUploader {
        font-size: 1.2rem !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        font-size: 1.1rem !important;
    }

    /* Dataframe */
    .dataframe {
        font-size: 1.1rem !important;
    }

    /* Code blocks */
    code {
        font-size: 1.1rem !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
    }

    /* Sidebar */
    .css-1d391kg {  /* Sidebar title */
        font-size: 1.3rem !important;
    }

    /* Radio buttons */
    .stRadio label {
        font-size: 1.2rem !important;
    }

    /* Help text */
    .stMarkdown a {
        font-size: 1.1rem !important;
    }

    /* Modern About section */
    .about-section {
        background: linear-gradient(145deg, #1e1e1e, #2d2d2d);
        padding: 1.8rem;
        border-radius: 12px;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .about-section:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .about-section h4 {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.3rem !important;
        margin-bottom: 1.2rem !important;
        letter-spacing: 0.5px;
    }

    .about-content {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .about-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem !important;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
    }

    .about-item:hover {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        transform: translateX(4px);
    }

    .about-item a {
        color: #64b5f6;
        text-decoration: none;
        transition: all 0.2s ease;
        position: relative;
    }

    .about-item a:hover {
        color: #90caf9;
        text-decoration: none;
    }

    .about-item a::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 1px;
        bottom: -2px;
        left: 0;
        background: linear-gradient(90deg, #64b5f6, transparent);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }

    .about-item a:hover::after {
        transform: scaleX(1);
    }

    .copyright {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem !important;
        text-align: center;
        letter-spacing: 0.5px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize session state for batch processing
if "batch_progress" not in st.session_state:
    st.session_state.batch_progress = {"current": 0, "total": 0, "status": {}}


def process_batch_videos(csv_data: pd.DataFrame) -> Dict[str, str]:
    """
    Process multiple videos from CSV data.

    Args:
        csv_data: DataFrame containing video metadata

    Returns:
        Dict[str, str]: Dictionary of video paths and their processing status
    """
    results = {}
    total_videos = len(csv_data)
    st.session_state.batch_progress["total"] = total_videos

    for idx, row in csv_data.iterrows():
        st.session_state.batch_progress["current"] = idx + 1
        try:
            # Extract data from CSV row
            input_path = row["input_path"]
            title = row.get("title", Path(input_path).stem)
            description = row.get("description", "")
            tags = row.get("tags", "").split(",") if row.get("tags") else None
            publish_time = row.get("publish_time")
            is_youtube_url = row.get("is_youtube_url", False)

            # Process video
            success, processed_path = process_with_progress(
                input_path=input_path,
                title=title,
                description=description,
                tags=tags,
                publish_time=publish_time,
                is_youtube_url=is_youtube_url,
                file_size_mb=100,  # Default estimate
            )

            results[input_path] = "Success" if success else "Failed"
            st.session_state.batch_progress["status"][input_path] = results[input_path]

        except Exception as e:
            logger.error("Error processing %s: %s", input_path, str(e))
            results[input_path] = f"Error: {str(e)}"
            st.session_state.batch_progress["status"][input_path] = results[input_path]

    return results


def estimate_processing_time(
    file_size_mb: float, is_youtube_url: bool = False
) -> float:
    """
    Estimate processing time in seconds based on file size and type.

    Args:
        file_size_mb: Size of the video file in megabytes
        is_youtube_url: Whether the input is a YouTube URL

    Returns:
        float: Estimated processing time in seconds
    """
    # Base processing rate (MB/s) - adjust these based on actual performance
    BASE_DOWNLOAD_RATE = 2.0  # MB/s for YouTube downloads
    BASE_PROCESSING_RATE = 5.0  # MB/s for video processing

    estimated_time = 0.0
    if is_youtube_url:
        # Add download time for YouTube videos
        estimated_time = file_size_mb / BASE_DOWNLOAD_RATE
        # Add processing time
        estimated_time += file_size_mb / BASE_PROCESSING_RATE
    else:
        # Only processing time for local files
        estimated_time = file_size_mb / BASE_PROCESSING_RATE

    # Add buffer for initialization and upload
    return estimated_time + 10  # Add 10 seconds buffer


def get_file_size_mb(file: Any) -> float:
    """
    Get file size in megabytes.

    Args:
        file: File object with size attribute

    Returns:
        float: File size in megabytes
    """
    if hasattr(file, "size"):
        return file.size / (1024 * 1024)
    return 100  # Default estimate for YouTube videos


def process_with_progress(
    input_path: str,
    title: str,
    description: str,
    tags: Optional[List[str]],
    publish_time: str,
    is_youtube_url: bool,
    file_size_mb: float,
) -> Tuple[bool, Optional[str]]:
    """
    Process video with progress tracking.

    Args:
        input_path: Path to video file or YouTube URL
        title: Video title
        description: Video description
        tags: List of video tags
        publish_time: Scheduled publish time
        is_youtube_url: Whether the input is a YouTube URL
        file_size_mb: Size of the video file in megabytes

    Returns:
        Tuple[bool, Optional[str]]: Success status and processed file path
    """
    processed_file_path = None
    try:
        # Estimate total processing time
        total_time = estimate_processing_time(file_size_mb, is_youtube_url)

        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_remaining = st.empty()

        # Processing stages and their relative weights
        stages = {
            "Initializing": 0.1,
            "Downloading" if is_youtube_url else "Reading": 0.3,
            "Processing": 0.4,
            "Uploading": 0.2,
        }

        current_progress = 0.0
        start_time = time.time()

        # Update progress for each stage
        for stage, weight in stages.items():
            status_text.text(f"📋 Status: {stage}...")

            # Simulate progress within each stage
            stage_steps = 10
            for i in range(stage_steps):
                # Calculate progress
                progress = current_progress + (weight * (i + 1) / stage_steps)
                progress_bar.progress(min(progress, 1.0))

                # Calculate and display estimated time remaining
                elapsed_time = time.time() - start_time
                if progress > 0:
                    estimated_total = elapsed_time / progress
                    remaining_time = max(0, estimated_total - elapsed_time)
                    time_remaining.text(
                        f"⏱️ Estimated time remaining: {remaining_time:.1f} seconds"
                    )

                # Actually process the video at the appropriate stage
                if stage == "Processing" and i == 0:
                    # Process the video and get the processed file path
                    processed_file_path = process_video(
                        input_path=input_path,
                        title=title,
                        description=description,
                        tags=tags,
                        publish_time=publish_time,
                        is_youtube_url=is_youtube_url,
                    )

                time.sleep(
                    total_time * weight / stage_steps / 2
                )  # Simulate stage processing

            current_progress += weight

        # Complete the progress bar
        progress_bar.progress(1.0)
        status_text.text("✅ Status: Complete!")
        time_remaining.text(
            f"⏱️ Total processing time: {time.time() - start_time:.1f} seconds"
        )

        # Show success message
        st.success("✅ Video processed and uploaded successfully!")
        st.balloons()

        return True, processed_file_path

    except Exception as e:
        logger.error("Error during processing: %s", str(e))
        st.error(f"❌ Error: {str(e)}")
        return False, processed_file_path


def main() -> None:
    """Main Streamlit application."""
    # Header
    st.title("🎥 YouTube Video Automation")
    st.markdown(
        """
    Process, enhance, and upload your videos to YouTube with ease.
    Choose between processing a local video file or downloading and processing a YouTube video.
    """
    )

    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    process_type = st.sidebar.radio(
        "Select Process Type",
        ["Single Video", "Batch Processing"],
        help="Choose whether to process a single video or multiple videos via CSV",
    )

    if process_type == "Single Video":
        video_source = st.radio(
            "Select Video Source",
            ["Local Video", "YouTube Video"],
            help="Choose whether to process a local video file or a YouTube video",
        )

        # Main form for single video processing
        with st.form("video_process_form"):
            if video_source == "Local Video":
                # Local video upload
                uploaded_file = st.file_uploader(
                    "Upload Video File",
                    type=["mp4", "mov", "avi", "mkv"],
                    help="Select a video file to process",
                )
                input_path = None
                if uploaded_file:
                    # Save uploaded file temporarily
                    temp_path = Path("temp") / uploaded_file.name
                    temp_path.parent.mkdir(exist_ok=True)
                    temp_path.write_bytes(uploaded_file.read())
                    input_path = str(temp_path)
                    file_size_mb = get_file_size_mb(uploaded_file)
            else:
                # YouTube URL input
                input_path = st.text_input(
                    "YouTube Video URL",
                    help="Enter the URL of the YouTube video you want to process",
                )
                file_size_mb = 100  # Default estimate for YouTube videos

            # Common metadata inputs
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input(
                    "Video Title", help="Enter the title for your video"
                )
                tags = st.text_input(
                    "Tags (comma-separated)", help="Enter tags separated by commas"
                )

            with col2:
                description = st.text_area(
                    "Video Description", help="Enter a description for your video"
                )
                publish_date = st.date_input(
                    "Publish Date",
                    min_value=datetime.date.today(),
                    help="Select the date to publish the video",
                )
                publish_time = st.time_input(
                    "Publish Time", help="Select the time to publish the video"
                )

            # Process button
            submit_button = st.form_submit_button("🚀 Process Video")

            if submit_button:
                if not input_path:
                    st.error("Please provide a video file or YouTube URL")
                    return

                processed_file_path = None
                try:
                    # Prepare parameters
                    tag_list = (
                        [tag.strip() for tag in tags.split(",")] if tags else None
                    )
                    publish_datetime = datetime.datetime.combine(
                        publish_date, publish_time
                    ).isoformat()

                    # Process video with progress tracking
                    success, processed_file_path = process_with_progress(
                        input_path=input_path,
                        title=title,
                        description=description,
                        tags=tag_list,
                        publish_time=publish_datetime,
                        is_youtube_url=(video_source == "YouTube Video"),
                        file_size_mb=file_size_mb,
                    )

                finally:
                    # Cleanup temporary files
                    try:
                        if video_source == "Local Video" and input_path:
                            Path(input_path).unlink(missing_ok=True)
                        if processed_file_path:
                            Path(processed_file_path).unlink(missing_ok=True)
                    except Exception as e:
                        logger.error(f"Error during cleanup: {str(e)}")

    else:  # Batch Processing
        st.markdown(
            """
        ## 📦 Batch Processing
        Upload a CSV file containing multiple videos to process. The CSV should include the following columns:
        - `input_path`: Local file path or YouTube URL
        - `title`: Video title (optional)
        - `description`: Video description (optional)
        - `tags`: Comma-separated tags (optional)
        - `publish_time`: Publication time in ISO format (optional)
        - `is_youtube_url`: true/false (optional, defaults to false)
        """
        )

        # Template download section
        st.markdown("### 📥 Get Started")
        template_col1, template_col2 = st.columns([2, 1])
        with template_col1:
            st.markdown(
                """
                1. Download the template CSV file
                2. Fill in your video details
                3. Upload the completed CSV
                """
            )
        with template_col2:
            if st.button("📄 Download Template"):
                template_path = Path("templates/batch_upload_template.csv")
                if template_path.exists():
                    with open(template_path, "r") as f:
                        template_content = f.read()
                        st.download_button(
                            "📥 Click to Download",
                            template_content,
                            file_name="batch_upload_template.csv",
                            mime="text/csv",
                        )
                else:
                    st.error("Template file not found. Please contact support.")

        st.markdown("### 📤 Upload Your CSV")
        # CSV file upload
        uploaded_csv = st.file_uploader(
            "Upload CSV File",
            type=["csv"],
            help="Upload your completed CSV file containing video metadata",
        )

        if uploaded_csv:
            try:
                # Read and validate CSV
                df = pd.read_csv(uploaded_csv)
                st.write("Preview of CSV data:")
                st.dataframe(df.head())

                # Process batch button
                if st.button("🚀 Process Batch"):
                    with st.spinner("Processing videos..."):
                        results = process_batch_videos(df)

                        # Display results
                        st.success("Batch processing complete!")
                        st.write("Processing Results:")
                        results_df = pd.DataFrame(
                            list(results.items()), columns=["Video", "Status"]
                        )
                        st.dataframe(results_df)

                        # Show progress
                        progress_container = st.empty()
                        progress_container.progress(
                            st.session_state.batch_progress["current"]
                            / st.session_state.batch_progress["total"]
                        )

            except Exception as e:
                st.error(f"Error processing CSV: {str(e)}")
                logger.error(f"CSV processing error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
    ### 📖 Help & Documentation
    - Upload a video file or provide a YouTube URL
    - Fill in the video details
    - Click "Process Video" to start
    - Wait for the processing to complete
    - For batch processing, upload a CSV file with video details

    For more information, visit our [documentation](https://github.com/dasdatasensei/YouTubeVideoAutomation/tree/main/docs).

    <div class="about-section">
        <h4>✨ About</h4>
        <div class="about-content">
            <div class="about-item">
                👩‍💻 Created by <a href="https://www.thedatasensei.com">Dr. Jody-Ann S. Jones</a>
            </div>
            <div class="about-item">
                🏢 <a href="https://www.thedatasensei.com">The Data Sensei</a> - Professional Data Science Solutions
            </div>
            <div class="about-item">
                📧 <a href="mailto:jody@thedatasensei.com">jody@thedatasensei.com</a>
            </div>
            <div class="about-item">
                <img src="https://github.com/favicon.ico" width="16" height="16" style="margin-right: 4px;">
                <a href="https://github.com/dasdatasensei">@dasdatasensei</a>
            </div>
        </div>
        <div class="copyright">
            © 2025 The Data Sensei. All rights reserved.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

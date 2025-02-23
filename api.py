#!/usr/bin/env python3
"""
YouTube Video Automation - FastAPI Backend
Author: Dr. Jody-Ann S. Jones
Website: www.thedatasensei.com
Year: 2025
"""

import csv
import io
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from main import process_video
from src.youtube_processor.models import BatchProcessingJob

app = FastAPI(
    title="YouTube Video Automation API",
    description="Process, enhance, and upload videos to YouTube with ease.",
    version="1.0.0",
    contact={
        "name": "Dr. Jody-Ann S. Jones",
        "url": "https://www.thedatasensei.com",
        "email": "jody@thedatasensei.com",
    },
)


# Constants
TEMPLATE_PATH = Path("templates/batch_upload_template.csv")


# Models for request/response
class VideoMetadata(BaseModel):
    title: str
    description: str
    tags: Optional[List[str]] = None
    publish_time: Optional[str] = None


class BatchVideoRequest(BaseModel):
    input_path: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    publish_time: Optional[str] = None
    is_youtube_url: bool = False


class BatchProcessingResponse(BaseModel):
    job_id: str
    status: str
    total_videos: int
    processed_videos: int = 0
    failed_videos: int = 0
    errors: List[str] = []


# Store batch processing jobs
batch_jobs = {}


async def process_batch(
    job_id: str, videos: List[BatchVideoRequest], background_tasks: BackgroundTasks
) -> None:
    """Process a batch of videos in the background."""
    job = batch_jobs[job_id]

    for video in videos:
        try:
            # Process video
            process_video(
                input_path=video.input_path,
                title=video.title,
                description=video.description,
                tags=video.tags,
                publish_time=video.publish_time,
                is_youtube_url=video.is_youtube_url,
            )
            job.processed_videos += 1
        except Exception as e:
            job.failed_videos += 1
            job.errors.append(f"Error processing {video.input_path}: {str(e)}")

    job.status = "completed"


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with user-friendly HTML interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Video Automation API</title>
        <style>
            :root {
                --primary-color: #2d3748;
                --secondary-color: #4299e1;
                --background-color: #f5f5f5;
                --container-background: white;
                --text-color: #2d3748;
                --border-color: #e2e8f0;
            }

            body {
                font-family: system-ui, -apple-system, sans-serif;
                line-height: 1.8;
                max-width: 1000px;
                margin: 0 auto;
                padding: 2rem;
                background: var(--background-color);
                font-size: 18px;
                color: var(--text-color);
            }

            .container {
                background: var(--container-background);
                padding: 3rem;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }

            h1 {
                color: var(--primary-color);
                margin-bottom: 1.5rem;
                font-size: 2.5rem;
                font-weight: 700;
            }

            h2 {
                font-size: 1.8rem;
                margin-top: 2rem;
                margin-bottom: 1rem;
                color: var(--primary-color);
            }

            p {
                font-size: 1.2rem;
                margin-bottom: 1.5rem;
                line-height: 1.8;
            }

            .badge {
                display: inline-block;
                padding: 0.5rem 1rem;
                background: var(--border-color);
                border-radius: 9999px;
                font-size: 1.1rem;
                margin: 0.5rem;
                font-weight: 500;
            }

            .endpoints {
                background: #f7fafc;
                padding: 1.5rem;
                border-radius: 8px;
                margin: 1.5rem 0;
            }

            .endpoint {
                margin: 1rem 0;
                padding: 1.2rem;
                border-left: 4px solid var(--primary-color);
                background: white;
                border-radius: 0 8px 8px 0;
            }

            .endpoint p {
                margin: 0.5rem 0;
                font-size: 1.2rem;
            }

            .method {
                font-weight: 600;
                color: var(--primary-color);
                font-size: 1.2rem;
            }

            code {
                background: #edf2f7;
                padding: 0.2rem 0.4rem;
                border-radius: 4px;
                font-size: 1.2rem;
                font-family: 'Monaco', 'Menlo', monospace;
            }

            a {
                color: var(--secondary-color);
                text-decoration: none;
                font-weight: 500;
                font-size: 1.2rem;
            }

            a:hover {
                text-decoration: underline;
            }

            ul {
                list-style-type: none;
                padding: 0;
            }

            ul li {
                margin: 1rem 0;
                font-size: 1.2rem;
                line-height: 1.8;
            }

            .footer {
                margin-top: 3rem;
                padding-top: 1.5rem;
                border-top: 1px solid var(--border-color);
                font-size: 1.1rem;
                color: #718096;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎥 YouTube Video Automation API</h1>

            <div>
                <span class="badge">Version 1.0.0</span>
                <span class="badge">FastAPI</span>
                <span class="badge">Python 3.9+</span>
            </div>

            <p class="description">Process, enhance, and upload videos to YouTube with ease.</p>

            <h2>📚 Documentation & Resources</h2>
            <ul>
                <li>📖 <a href="/docs">Interactive API Documentation (Swagger UI)</a></li>
                <li>📘 <a href="/redoc">Alternative Documentation (ReDoc)</a></li>
                <li>🖥️ <a href="http://localhost:8501">Streamlit Interface</a></li>
                <li>📚 <a href="https://github.com/dasdatasensei/YouTubeVideoAutomation/tree/main/docs">Full Documentation</a></li>
            </ul>

            <h2>🛠️ Available Endpoints</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <span class="method">GET</span> <code>/</code>
                    <p>This page - API overview and documentation</p>
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <code>/process</code>
                    <p>Process and upload a single video</p>
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <code>/batch/process</code>
                    <p>Process multiple videos in batch</p>
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <code>/batch/csv</code>
                    <p>Process videos from CSV file</p>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <code>/batch/status/{job_id}</code>
                    <p>Check batch processing status</p>
                </div>
            </div>

            <h2>🚀 Quick Start</h2>
            <p>Choose your preferred interface:</p>
            <ul>
                <li>🖥️ <a href="http://localhost:8501">Streamlit Interface</a> - User-friendly web interface</li>
                <li>🔧 <a href="/docs">API Documentation</a> - Direct API access</li>
            </ul>

            <div class="footer">
                <p>
                    Created by <a href="https://www.thedatasensei.com">Dr. Jody-Ann S. Jones</a> |
                    <a href="https://www.thedatasensei.com">The Data Sensei</a>
                </p>
                <p>
                    Contact: <a href="mailto:jody@thedatasensei.com">jody@thedatasensei.com</a> |
                    GitHub: <a href="https://github.com/dasdatasensei">@dasdatasensei</a>
                </p>
                <p>© 2025 The Data Sensei. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """


@app.post("/process")
async def process_video_endpoint(
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form(...),
    publish_time: str = Form(...),
    file: Optional[UploadFile] = None,
    youtube_url: Optional[str] = Form(None),
):
    """Process and upload a single video."""
    try:
        # Handle file upload
        if file:
            temp_path = f"temp/{file.filename}"
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)
            input_path = temp_path
            is_youtube_url = False
        elif youtube_url:
            input_path = youtube_url
            is_youtube_url = True
        else:
            raise HTTPException(
                status_code=400, detail="Either file or youtube_url must be provided"
            )

        # Convert tags string to list
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else None

        # Process video
        process_video(
            input_path=input_path,
            title=title,
            description=description,
            tags=tag_list,
            publish_time=publish_time,
            is_youtube_url=is_youtube_url,
        )

        return {"status": "success", "message": "Video processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch/process")
async def batch_process_videos(
    videos: List[BatchVideoRequest], background_tasks: BackgroundTasks
) -> BatchProcessingResponse:
    """Process multiple videos in batch."""
    job_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Initialize job status
    batch_jobs[job_id] = BatchProcessingResponse(
        job_id=job_id, status="processing", total_videos=len(videos)
    )

    # Start background processing
    background_tasks.add_task(process_batch, job_id, videos, background_tasks)

    return batch_jobs[job_id]


@app.post("/batch/csv")
async def batch_process_from_csv(
    background_tasks: BackgroundTasks, csv_file: UploadFile = File(...)
) -> BatchProcessingResponse:
    """Process multiple videos from a CSV file."""
    try:
        # Read CSV file
        content = await csv_file.read()
        csv_text = content.decode()
        csv_io = io.StringIO(csv_text)
        reader = csv.DictReader(csv_io)

        # Convert CSV rows to BatchVideoRequest objects
        videos = []
        for row in reader:
            video = BatchVideoRequest(
                input_path=row["input_path"],
                title=row.get("title"),
                description=row.get("description", ""),
                tags=row.get("tags", "").split(",") if row.get("tags") else None,
                publish_time=row.get("publish_time"),
                is_youtube_url=row.get("is_youtube_url", "").lower() == "true",
            )
            videos.append(video)

        # Start batch processing
        return await batch_process_videos(videos, background_tasks)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing CSV file: {str(e)}"
        )


@app.get("/batch/status/{job_id}")
async def get_batch_status(job_id: str) -> BatchProcessingResponse:
    """Get the status of a batch processing job."""
    if job_id not in batch_jobs:
        raise HTTPException(status_code=404, detail=f"Batch job {job_id} not found")

    return batch_jobs[job_id]


@app.get("/batch/template")
async def get_batch_template():
    """Download the batch processing CSV template."""
    if not TEMPLATE_PATH.exists():
        raise HTTPException(
            status_code=404, detail="Template file not found. Please contact support."
        )

    return FileResponse(
        TEMPLATE_PATH,
        media_type="text/csv",
        filename="batch_upload_template.csv",
        headers={"Content-Disposition": "attachment"},
    )

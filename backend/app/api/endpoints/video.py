"""
Video processing endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import uuid
from datetime import datetime
from loguru import logger

from app.core.config import settings
from app.services.video.video_processor import VideoProcessor
from app.services.ai.svd_service import SVDService

router = APIRouter()


class VideoTransformRequest(BaseModel):
    """Request model for video transformation"""
    prompt: str
    conditions: List[str] = []
    style_preset: Optional[str] = None
    quality: str = "high"  # low, medium, high


class VideoTransformResponse(BaseModel):
    """Response model for video transformation"""
    job_id: str
    status: str
    message: str
    estimated_time: Optional[int] = None


class VideoStatusResponse(BaseModel):
    """Response model for video status"""
    job_id: str
    status: str  # pending, processing, completed, failed
    progress: float  # 0-100
    message: str
    output_url: Optional[str] = None
    created_at: str
    updated_at: str


# In-memory storage for job status (replace with Redis/database in production)
job_status = {}


@router.post("/upload", response_model=dict)
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload a video file for processing"""
    
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {settings.ALLOWED_VIDEO_EXTENSIONS}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Generate unique filename
    job_id = str(uuid.uuid4())
    filename = f"{job_id}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Initialize job status
        job_status[job_id] = {
            "status": "uploaded",
            "progress": 0,
            "message": "Video uploaded successfully",
            "input_file": file_path,
            "output_file": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Video uploaded successfully: {filename}")
        
        return {
            "job_id": job_id,
            "filename": filename,
            "message": "Video uploaded successfully",
            "status": "uploaded"
        }
        
    except Exception as e:
        logger.error(f"Error uploading video: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload video")


@router.post("/transform", response_model=VideoTransformResponse)
async def transform_video(
    background_tasks: BackgroundTasks,
    request: VideoTransformRequest,
    job_id: str
):
    """Transform video with AI-generated atmospheric effects"""
    
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job_status[job_id]["status"] != "uploaded":
        raise HTTPException(status_code=400, detail="Video not ready for transformation")
    
    try:
        # Update job status
        job_status[job_id].update({
            "status": "processing",
            "progress": 10,
            "message": "Starting video transformation...",
            "updated_at": datetime.utcnow().isoformat()
        })
        
        # Start background processing
        background_tasks.add_task(
            process_video_transformation,
            job_id,
            request.prompt,
            request.conditions,
            request.style_preset,
            request.quality
        )
        
        return VideoTransformResponse(
            job_id=job_id,
            status="processing",
            message="Video transformation started",
            estimated_time=300  # 5 minutes estimate
        )
        
    except Exception as e:
        logger.error(f"Error starting video transformation: {e}")
        job_status[job_id].update({
            "status": "failed",
            "message": f"Failed to start transformation: {str(e)}",
            "updated_at": datetime.utcnow().isoformat()
        })
        raise HTTPException(status_code=500, detail="Failed to start video transformation")


@router.get("/status/{job_id}", response_model=VideoStatusResponse)
async def get_video_status(job_id: str):
    """Get the status of a video transformation job"""
    
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_status[job_id]
    
    # Generate output URL if completed
    output_url = None
    if job["status"] == "completed" and job["output_file"]:
        output_url = f"/outputs/{os.path.basename(job['output_file'])}"
    
    return VideoStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        output_url=output_url,
        created_at=job["created_at"],
        updated_at=job["updated_at"]
    )


@router.get("/download/{job_id}")
async def download_video(job_id: str):
    """Download the transformed video"""
    
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_status[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video transformation not completed")
    
    if not job["output_file"] or not os.path.exists(job["output_file"]):
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        job["output_file"],
        media_type="video/mp4",
        filename=f"aura_transformed_{job_id}.mp4"
    )


async def process_video_transformation(
    job_id: str,
    prompt: str,
    conditions: List[str],
    style_preset: Optional[str],
    quality: str
):
    """Background task for video transformation using Stable Video Diffusion"""
    try:
        job = job_status[job_id]
        input_file = job["input_file"]

        # Initialize services
        video_processor = VideoProcessor()
        svd_service = SVDService()

        # Update progress
        job_status[job_id].update({
            "progress": 20,
            "message": "Processing video frames...",
            "updated_at": datetime.utcnow().isoformat()
        })

        # Process video frames (extract first frame for SVD conditioning)
        frames = await video_processor.extract_frames(input_file)

        job_status[job_id].update({
            "progress": 40,
            "message": "Applying Stable Video Diffusion...",
            "updated_at": datetime.utcnow().isoformat()
        })

        # Apply SVD transformation (video-to-video)
        transformed_frames = await svd_service.transform_video(
            frames, prompt, conditions, style_preset, quality
        )

        job_status[job_id].update({
            "progress": 80,
            "message": "Generating final video...",
            "updated_at": datetime.utcnow().isoformat()
        })

        # Generate output video
        output_filename = f"aura_{job_id}.mp4"
        output_path = os.path.join(settings.OUTPUT_DIR, output_filename)

        await video_processor.create_video(transformed_frames, output_path)

        # Update job status to completed
        job_status[job_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Video transformation completed successfully",
            "output_file": output_path,
            "updated_at": datetime.utcnow().isoformat()
        })

        logger.info(f"Video transformation completed: {job_id}")

    except Exception as e:
        logger.error(f"Error in video transformation: {e}")
        job_status[job_id].update({
            "status": "failed",
            "message": f"Transformation failed: {str(e)}",
            "updated_at": datetime.utcnow().isoformat()
        })


@router.get("/test-models")
async def test_models():
    """Test if AI models can be loaded"""
    try:
        from app.services.ai.diffusion_service import DiffusionService
        
        # Try to initialize the diffusion service
        diffusion_service = DiffusionService()
        
        return {
            "status": "success",
            "message": "AI models loaded successfully",
            "device": diffusion_service.device
        }
    except Exception as e:
        logger.error(f"Model test failed: {e}")
        return {
            "status": "error",
            "message": f"Failed to load models: {str(e)}"
        }


@router.get("/jobs", response_model=List[VideoStatusResponse])
async def list_jobs():
    """List all video transformation jobs"""
    
    jobs = []
    for job_id, job in job_status.items():
        output_url = None
        if job["status"] == "completed" and job["output_file"]:
            output_url = f"/outputs/{os.path.basename(job['output_file'])}"
        
        jobs.append(VideoStatusResponse(
            job_id=job_id,
            status=job["status"],
            progress=job["progress"],
            message=job["message"],
            output_url=output_url,
            created_at=job["created_at"],
            updated_at=job["updated_at"]
        ))
    
    return jobs 
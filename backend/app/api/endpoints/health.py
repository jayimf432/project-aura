"""
Health check endpoints
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
import psutil
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "project-aura-api",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    try:
        # Get system information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check if required directories exist
        upload_dir_exists = os.path.exists("uploads")
        output_dir_exists = os.path.exists("outputs")
        temp_dir_exists = os.path.exists("temp")
        
        return {
            "status": "healthy",
            "service": "project-aura-api",
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2)
            },
            "directories": {
                "uploads": upload_dir_exists,
                "outputs": output_dir_exists,
                "temp": temp_dir_exists
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/health/ready")
async def readiness_check():
    """Readiness check for Kubernetes/container orchestration"""
    # Add any startup checks here
    return {
        "status": "ready",
        "service": "project-aura-api"
    }


@router.get("/health/live")
async def liveness_check():
    """Liveness check for Kubernetes/container orchestration"""
    return {
        "status": "alive",
        "service": "project-aura-api"
    } 
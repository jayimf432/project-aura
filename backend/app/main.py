"""
Project Aura - Main FastAPI Application
AI-Powered Cinematic Video Transformation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from loguru import logger

from app.core.config import settings
from app.api.endpoints import video, ai_director, health
from app.api.endpoints import image


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting Project Aura Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    
    logger.info("✅ Project Aura Backend started successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Project Aura Backend...")


# Create FastAPI application
app = FastAPI(
    title="Project Aura API",
    description="AI-Powered Cinematic Video Transformation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(video.router, prefix="/api/v1/video", tags=["video"])
app.include_router(ai_director.router, prefix="/api/v1/ai-director", tags=["ai-director"])
app.include_router(image.router, prefix="/api/v1/image", tags=["image"])

# Mount static files for serving generated videos
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Project Aura API",
        "version": "1.0.0",
        "docs": "/docs",
        "description": "AI-Powered Cinematic Video Transformation"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "project-aura-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    ) 